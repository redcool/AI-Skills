#!/usr/bin/env python3
"""
Design Token System for Unity UI Toolkit (UXML/USS)
=====================================================
将 ui-ux 设计知识转化为结构化的设计 Token，供 UXML 生成器消费。

设计 Token 是框架无关的：色板、字体、间距、圆角、阴影。
这些 Token 可以从 ui-ux-pro-max 的 161 色板 / 57 字体搭配中选取，
也可以由用户自定义。

用法：
  from design_tokens import DesignTokenManager, PRESETS
  mgr = DesignTokenManager()
  tokens = mgr.load_preset("dark_glassmorphism")
  tokens = mgr.merge(tokens, {"colors": {"primary": "#FF6B6B"}})  # 覆盖主色
  mgr.save(tokens, "my_theme.json")
"""

import json
import os
import copy
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any


# ============================================================
# 161 色板精选（从 ui-ux-pro-max 提取的高质量色板）
# ============================================================

COLOR_PALETTES = {
    # --- 暗色系 ---
    "midnight_aurora": {
        "primary": "#6366F1",
        "primary_variant": "#4F46E5",
        "secondary": "#8B5CF6",
        "secondary_variant": "#7C3AED",
        "background": "#0B0F1A",
        "surface": "#151B2E",
        "surface_variant": "#1E2642",
        "card": "#1A2038",
        "error": "#EF4444",
        "success": "#10B981",
        "warning": "#F59E0B",
        "info": "#3B82F6",
        "on_primary": "#FFFFFF",
        "on_background": "#E2E8F0",
        "on_surface": "#CBD5E1",
        "on_surface_variant": "#94A3B8",
        "border": "#2D3A5C",
        "border_focus": "#6366F1",
        "disabled": "#475569",
        "disabled_bg": "#1E293B",
        "overlay": "rgba(0,0,0,0.6)",
        "scrim": "rgba(0,0,0,0.85)",
    },
    "dark_glassmorphism": {
        "primary": "#A78BFA",
        "primary_variant": "#8B5CF6",
        "secondary": "#67E8F9",
        "secondary_variant": "#22D3EE",
        "background": "#0F0F1A",
        "surface": "rgba(30,30,50,0.7)",
        "surface_variant": "rgba(50,50,80,0.5)",
        "card": "rgba(25,25,45,0.6)",
        "error": "#FB7185",
        "success": "#34D399",
        "warning": "#FBBF24",
        "info": "#60A5FA",
        "on_primary": "#FFFFFF",
        "on_background": "#F1F5F9",
        "on_surface": "#E2E8F0",
        "on_surface_variant": "#94A3B8",
        "border": "rgba(139,92,246,0.3)",
        "border_focus": "#A78BFA",
        "disabled": "#475569",
        "disabled_bg": "rgba(30,30,50,0.3)",
        "overlay": "rgba(0,0,0,0.5)",
        "scrim": "rgba(0,0,0,0.8)",
    },
    "cyber_neon": {
        "primary": "#00FF88",
        "primary_variant": "#00CC6A",
        "secondary": "#00D4FF",
        "secondary_variant": "#00A8CC",
        "background": "#0A0A0F",
        "surface": "#12121A",
        "surface_variant": "#1A1A28",
        "card": "#15151F",
        "error": "#FF3366",
        "success": "#00FF88",
        "warning": "#FFAA00",
        "info": "#00D4FF",
        "on_primary": "#0A0A0F",
        "on_background": "#E0FFE0",
        "on_surface": "#B0D0B0",
        "on_surface_variant": "#709070",
        "border": "#00FF8844",
        "border_focus": "#00FF88",
        "disabled": "#334433",
        "disabled_bg": "#0F0F14",
        "overlay": "rgba(0,10,0,0.6)",
        "scrim": "rgba(0,0,0,0.85)",
    },
    "warm_dark": {
        "primary": "#F97316",
        "primary_variant": "#EA580C",
        "secondary": "#FB923C",
        "secondary_variant": "#FDBA74",
        "background": "#1A1210",
        "surface": "#251A15",
        "surface_variant": "#30221B",
        "card": "#2A1D16",
        "error": "#EF4444",
        "success": "#22C55E",
        "warning": "#F59E0B",
        "info": "#3B82F6",
        "on_primary": "#FFFFFF",
        "on_background": "#FDE8D8",
        "on_surface": "#D4B8A0",
        "on_surface_variant": "#A08060",
        "border": "#3D2A1E",
        "border_focus": "#F97316",
        "disabled": "#5C4033",
        "disabled_bg": "#1E1510",
        "overlay": "rgba(0,0,0,0.6)",
        "scrim": "rgba(0,0,0,0.85)",
    },

    # --- 亮色系 ---
    "light_minimal": {
        "primary": "#2563EB",
        "primary_variant": "#1D4ED8",
        "secondary": "#7C3AED",
        "secondary_variant": "#6D28D9",
        "background": "#FFFFFF",
        "surface": "#F8FAFC",
        "surface_variant": "#F1F5F9",
        "card": "#FFFFFF",
        "error": "#DC2626",
        "success": "#16A34A",
        "warning": "#D97706",
        "info": "#2563EB",
        "on_primary": "#FFFFFF",
        "on_background": "#0F172A",
        "on_surface": "#1E293B",
        "on_surface_variant": "#475569",
        "border": "#E2E8F0",
        "border_focus": "#2563EB",
        "disabled": "#94A3B8",
        "disabled_bg": "#F1F5F9",
        "overlay": "rgba(0,0,0,0.3)",
        "scrim": "rgba(0,0,0,0.5)",
    },
    "light_claymorphism": {
        "primary": "#8B5CF6",
        "primary_variant": "#7C3AED",
        "secondary": "#EC4899",
        "secondary_variant": "#DB2777",
        "background": "#F0EDE8",
        "surface": "#F7F5F2",
        "surface_variant": "#EEEAE4",
        "card": "#FFFFFF",
        "error": "#EF4444",
        "success": "#22C55E",
        "warning": "#F59E0B",
        "info": "#3B82F6",
        "on_primary": "#FFFFFF",
        "on_background": "#1F2937",
        "on_surface": "#374151",
        "on_surface_variant": "#6B7280",
        "border": "#D1CCC4",
        "border_focus": "#8B5CF6",
        "disabled": "#9CA3AF",
        "disabled_bg": "#E5E1DB",
        "overlay": "rgba(0,0,0,0.15)",
        "scrim": "rgba(0,0,0,0.4)",
    },

    # --- 游戏风格 ---
    "game_fantasy": {
        "primary": "#D4A44C",
        "primary_variant": "#B8860B",
        "secondary": "#8B0000",
        "secondary_variant": "#6B0000",
        "background": "#1A1208",
        "surface": "#2A1F0E",
        "surface_variant": "#3A2C14",
        "card": "#2E2210",
        "error": "#FF4444",
        "success": "#4CAF50",
        "warning": "#FFC107",
        "info": "#64B5F6",
        "on_primary": "#1A1208",
        "on_background": "#E8D5A8",
        "on_surface": "#C4A868",
        "on_surface_variant": "#8B7340",
        "border": "#4A3820",
        "border_focus": "#D4A44C",
        "disabled": "#5C4A28",
        "disabled_bg": "#1E1608",
        "overlay": "rgba(0,0,0,0.7)",
        "scrim": "rgba(0,0,0,0.9)",
    },
    "game_scifi": {
        "primary": "#00BFFF",
        "primary_variant": "#0099CC",
        "secondary": "#FF6B35",
        "secondary_variant": "#CC5529",
        "background": "#080C12",
        "surface": "#0E1520",
        "surface_variant": "#141E2C",
        "card": "#101A24",
        "error": "#FF3333",
        "success": "#00FF7F",
        "warning": "#FFD700",
        "info": "#00BFFF",
        "on_primary": "#080C12",
        "on_background": "#C0D8E8",
        "on_surface": "#8CAABE",
        "on_surface_variant": "#5A7A8F",
        "border": "#1A2E40",
        "border_focus": "#00BFFF",
        "disabled": "#2A4050",
        "disabled_bg": "#0A1018",
        "overlay": "rgba(0,5,15,0.6)",
        "scrim": "rgba(0,0,0,0.85)",
    },
    "game_horror": {
        "primary": "#8B0000",
        "primary_variant": "#660000",
        "secondary": "#4A0E4E",
        "secondary_variant": "#360A3A",
        "background": "#0A0A0A",
        "surface": "#141414",
        "surface_variant": "#1E1E1E",
        "card": "#181818",
        "error": "#CC0000",
        "success": "#2E7D32",
        "warning": "#BF360C",
        "info": "#4A148C",
        "on_primary": "#FFFFFF",
        "on_background": "#B0A090",
        "on_surface": "#8A7A6A",
        "on_surface_variant": "#5A4A3A",
        "border": "#2A2020",
        "border_focus": "#8B0000",
        "disabled": "#3A3030",
        "disabled_bg": "#0F0F0F",
        "overlay": "rgba(0,0,0,0.75)",
        "scrim": "rgba(0,0,0,0.95)",
    },
    "game_pixel_retro": {
        "primary": "#FFD700",
        "primary_variant": "#DAA520",
        "secondary": "#FF6347",
        "secondary_variant": "#CD5C5C",
        "background": "#2C2C2C",
        "surface": "#3A3A3A",
        "surface_variant": "#484848",
        "card": "#404040",
        "error": "#FF0000",
        "success": "#00FF00",
        "warning": "#FFFF00",
        "info": "#00BFFF",
        "on_primary": "#2C2C2C",
        "on_background": "#E0E0E0",
        "on_surface": "#C0C0C0",
        "on_surface_variant": "#808080",
        "border": "#555555",
        "border_focus": "#FFD700",
        "disabled": "#666666",
        "disabled_bg": "#333333",
        "overlay": "rgba(0,0,0,0.65)",
        "scrim": "rgba(0,0,0,0.85)",
    },
}


# ============================================================
# 57 字体搭配精选
# ============================================================

TYPOGRAPHY_PRESETS = {
    "modern_sans": {
        "heading": {"family": "Noto Sans SC", "weight": "bold", "sizes": {"h1": 32, "h2": 24, "h3": 20, "h4": 18, "h5": 16, "h6": 14}},
        "body": {"family": "Noto Sans SC", "weight": "normal", "sizes": {"lg": 16, "md": 14, "sm": 12, "xs": 10}},
        "mono": {"family": "JetBrains Mono", "weight": "normal", "sizes": {"md": 13, "sm": 11}},
        "line_height": 1.5,
        "letter_spacing": {"heading": -0.02, "body": 0, "mono": 0.05},
    },
    "elegant_serif": {
        "heading": {"family": "Noto Serif SC", "weight": "bold", "sizes": {"h1": 36, "h2": 28, "h3": 22, "h4": 18, "h5": 16, "h6": 14}},
        "body": {"family": "Noto Serif SC", "weight": "normal", "sizes": {"lg": 17, "md": 15, "sm": 13, "xs": 11}},
        "mono": {"family": "Source Code Pro", "weight": "normal", "sizes": {"md": 13, "sm": 11}},
        "line_height": 1.6,
        "letter_spacing": {"heading": -0.01, "body": 0.01, "mono": 0.03},
    },
    "game_fantasy": {
        "heading": {"family": "ZCOOL QingKe HuangYou", "weight": "bold", "sizes": {"h1": 36, "h2": 28, "h3": 22, "h4": 18, "h5": 16, "h6": 14}},
        "body": {"family": "Noto Sans SC", "weight": "normal", "sizes": {"lg": 16, "md": 14, "sm": 12, "xs": 10}},
        "mono": {"family": "Press Start 2P", "weight": "normal", "sizes": {"md": 12, "sm": 10}},
        "line_height": 1.5,
        "letter_spacing": {"heading": 0.05, "body": 0.02, "mono": 0.08},
    },
    "cyber_tech": {
        "heading": {"family": "Orbitron", "weight": "bold", "sizes": {"h1": 34, "h2": 26, "h3": 20, "h4": 17, "h5": 15, "h6": 13}},
        "body": {"family": "Rajdhani", "weight": "normal", "sizes": {"lg": 16, "md": 14, "sm": 12, "xs": 10}},
        "mono": {"family": "Share Tech Mono", "weight": "normal", "sizes": {"md": 13, "sm": 11}},
        "line_height": 1.4,
        "letter_spacing": {"heading": 0.08, "body": 0.03, "mono": 0.1},
    },
    "pixel_retro": {
        "heading": {"family": "Press Start 2P", "weight": "normal", "sizes": {"h1": 24, "h2": 18, "h3": 14, "h4": 12, "h5": 10, "h6": 8}},
        "body": {"family": "Press Start 2P", "weight": "normal", "sizes": {"lg": 12, "md": 10, "sm": 8, "xs": 6}},
        "mono": {"family": "Press Start 2P", "weight": "normal", "sizes": {"md": 10, "sm": 8}},
        "line_height": 1.8,
        "letter_spacing": {"heading": 0, "body": 0, "mono": 0},
    },
    "horror_gothic": {
        "heading": {"family": "UnifrakturMaguntia", "weight": "bold", "sizes": {"h1": 38, "h2": 30, "h3": 24, "h4": 20, "h5": 16, "h6": 14}},
        "body": {"family": "Noto Sans SC", "weight": "normal", "sizes": {"lg": 16, "md": 14, "sm": 12, "xs": 10}},
        "mono": {"family": "Special Elite", "weight": "normal", "sizes": {"md": 13, "sm": 11}},
        "line_height": 1.6,
        "letter_spacing": {"heading": 0.02, "body": 0.01, "mono": 0.05},
    },
}


# ============================================================
# 间距系统（4px 基准网格）
# ============================================================

SPACING_PRESETS = {
    "compact": {"xs": 2, "sm": 4, "md": 8, "lg": 12, "xl": 16, "2xl": 20, "3xl": 24},
    "standard": {"xs": 4, "sm": 8, "md": 12, "lg": 16, "xl": 24, "2xl": 32, "3xl": 48},
    "comfortable": {"xs": 6, "sm": 12, "md": 16, "lg": 24, "xl": 32, "2xl": 48, "3xl": 64},
    "game_dense": {"xs": 2, "sm": 4, "md": 6, "lg": 8, "xl": 12, "2xl": 16, "3xl": 20},
    "game_spacious": {"xs": 6, "sm": 10, "md": 14, "lg": 20, "xl": 28, "2xl": 40, "3xl": 56},
}


# ============================================================
# 圆角系统
# ============================================================

RADIUS_PRESETS = {
    "sharp": {"none": 0, "xs": 1, "sm": 2, "md": 3, "lg": 4, "xl": 6, "full": 999},
    "standard": {"none": 0, "xs": 2, "sm": 4, "md": 6, "lg": 8, "xl": 12, "full": 999},
    "rounded": {"none": 0, "xs": 4, "sm": 8, "md": 12, "lg": 16, "xl": 24, "full": 999},
    "pill": {"none": 0, "xs": 8, "sm": 12, "md": 16, "lg": 20, "xl": 28, "full": 999},
    "game_hard": {"none": 0, "xs": 0, "sm": 1, "md": 2, "lg": 2, "xl": 3, "full": 999},
    "game_fantasy": {"none": 0, "xs": 2, "sm": 4, "md": 8, "lg": 12, "xl": 16, "full": 999},
}


# ============================================================
# 阴影系统（USS 能力范围内的简化版）
# ============================================================

SHADOW_PRESETS = {
    "none": {
        "sm": "none",
        "md": "none",
        "lg": "none",
        "xl": "none",
    },
    "subtle": {
        "sm": "0 1px 2px rgba(0,0,0,0.1)",
        "md": "0 2px 4px rgba(0,0,0,0.12)",
        "lg": "0 4px 8px rgba(0,0,0,0.14)",
        "xl": "0 8px 16px rgba(0,0,0,0.16)",
    },
    "elevated": {
        "sm": "0 2px 4px rgba(0,0,0,0.2)",
        "md": "0 4px 8px rgba(0,0,0,0.25)",
        "lg": "0 8px 16px rgba(0,0,0,0.3)",
        "xl": "0 16px 32px rgba(0,0,0,0.35)",
    },
    "game_fantasy": {
        "sm": "0 0 6px rgba(212,164,76,0.3)",
        "md": "0 0 10px rgba(212,164,76,0.4)",
        "lg": "0 0 16px rgba(212,164,76,0.5)",
        "xl": "0 0 24px rgba(212,164,76,0.6)",
    },
    "game_scifi": {
        "sm": "0 0 4px rgba(0,191,255,0.3)",
        "md": "0 0 8px rgba(0,191,255,0.4)",
        "lg": "0 0 14px rgba(0,191,255,0.5)",
        "xl": "0 0 20px rgba(0,191,255,0.6)",
    },
    "game_horror": {
        "sm": "0 0 4px rgba(139,0,0,0.3)",
        "md": "0 0 8px rgba(139,0,0,0.4)",
        "lg": "0 0 14px rgba(74,14,78,0.5)",
        "xl": "0 0 20px rgba(74,14,78,0.6)",
    },
}


# ============================================================
# 组件间距规范
# ============================================================

COMPONENT_SPACING = {
    "input": {
        "height": 36,
        "padding_h": 12,
        "padding_v": 8,
        "gap": 8,
        "icon_size": 18,
    },
    "button": {
        "height": 36,
        "padding_h": 16,
        "padding_v": 8,
        "min_width": 80,
        "gap": 6,
        "icon_size": 18,
    },
    "card": {
        "padding": 16,
        "gap": 12,
        "header_height": 40,
    },
    "list_item": {
        "height": 48,
        "padding_h": 16,
        "gap": 12,
        "avatar_size": 32,
    },
    "toolbar": {
        "height": 48,
        "padding_h": 12,
        "gap": 8,
        "icon_size": 22,
    },
    "tab": {
        "height": 40,
        "padding_h": 16,
        "gap": 0,
        "indicator_height": 3,
    },
    "dialog": {
        "padding": 24,
        "gap": 16,
        "min_width": 320,
        "max_width": 560,
    },
    "tooltip": {
        "padding_h": 8,
        "padding_v": 4,
        "max_width": 240,
    },
    "hud": {
        "padding": 8,
        "gap": 6,
        "icon_size": 20,
        "bar_height": 8,
    },
}


# ============================================================
# 动画/过渡参数
# ============================================================

ANIMATION_PRESETS = {
    "none": {
        "duration_ms": 0,
        "easing": "linear",
    },
    "fast": {
        "duration_ms": 100,
        "easing": "ease-out",
    },
    "standard": {
        "duration_ms": 200,
        "easing": "ease-out",
    },
    "smooth": {
        "duration_ms": 300,
        "easing": "ease-in-out",
    },
    "game_snappy": {
        "duration_ms": 80,
        "easing": "ease-out",
    },
    "game_dramatic": {
        "duration_ms": 500,
        "easing": "ease-in-out",
    },
}


# ============================================================
# 预设组合（完整设计系统）
# ============================================================

PRESETS = {
    "dark_glassmorphism": {
        "name": "暗色毛玻璃",
        "description": "半透明背景 + 柔和光晕，适合现代暗色UI",
        "palette": "dark_glassmorphism",
        "typography": "modern_sans",
        "spacing": "standard",
        "radius": "standard",
        "shadow": "subtle",
        "animation": "smooth",
    },
    "midnight_aurora": {
        "name": "午夜极光",
        "description": "深蓝背景 + 紫色渐变，科技感暗色主题",
        "palette": "midnight_aurora",
        "typography": "modern_sans",
        "spacing": "standard",
        "radius": "rounded",
        "shadow": "elevated",
        "animation": "standard",
    },
    "cyber_neon": {
        "name": "赛博霓虹",
        "description": "纯黑底 + 霓虹绿/蓝发光边框，赛博朋克风格",
        "palette": "cyber_neon",
        "typography": "cyber_tech",
        "spacing": "compact",
        "radius": "sharp",
        "shadow": "game_scifi",
        "animation": "game_snappy",
    },
    "warm_dark": {
        "name": "暖色暗调",
        "description": "深棕暖色背景，适合温馨/叙事类界面",
        "palette": "warm_dark",
        "typography": "elegant_serif",
        "spacing": "comfortable",
        "radius": "standard",
        "shadow": "subtle",
        "animation": "smooth",
    },
    "light_minimal": {
        "name": "亮色极简",
        "description": "白底蓝调，干净专业",
        "palette": "light_minimal",
        "typography": "modern_sans",
        "spacing": "standard",
        "radius": "standard",
        "shadow": "subtle",
        "animation": "standard",
    },
    "light_claymorphism": {
        "name": "亮色黏土",
        "description": "奶油底 + 柔和内阴影 + 圆润边角",
        "palette": "light_claymorphism",
        "typography": "modern_sans",
        "spacing": "comfortable",
        "radius": "rounded",
        "shadow": "subtle",
        "animation": "smooth",
    },
    "game_fantasy": {
        "name": "奇幻游戏",
        "description": "暗金色调 + 发光边框，RPG/奇幻游戏界面",
        "palette": "game_fantasy",
        "typography": "game_fantasy",
        "spacing": "game_spacious",
        "radius": "game_fantasy",
        "shadow": "game_fantasy",
        "animation": "game_dramatic",
    },
    "game_scifi": {
        "name": "科幻游戏",
        "description": "深蓝底 + 蓝橙配色 + 发光效果，科幻/太空游戏",
        "palette": "game_scifi",
        "typography": "cyber_tech",
        "spacing": "game_dense",
        "radius": "sharp",
        "shadow": "game_scifi",
        "animation": "game_snappy",
    },
    "game_horror": {
        "name": "恐怖游戏",
        "description": "极暗底色 + 血红/暗紫 + 不规则阴影，恐怖游戏界面",
        "palette": "game_horror",
        "typography": "horror_gothic",
        "spacing": "game_spacious",
        "radius": "sharp",
        "shadow": "game_horror",
        "animation": "game_dramatic",
    },
    "game_pixel_retro": {
        "name": "像素复古",
        "description": "灰底 + 高饱和色彩 + 像素字体，8-bit 风格",
        "palette": "game_pixel_retro",
        "typography": "pixel_retro",
        "spacing": "game_dense",
        "radius": "game_hard",
        "shadow": "none",
        "animation": "game_snappy",
    },
}


# ============================================================
# DesignTokenManager — 核心 Token 管理器
# ============================================================

class DesignTokenManager:
    """管理设计 Token 的加载、合并、导出。"""

    def __init__(self):
        self.palettes = COLOR_PALETTES
        self.typographies = TYPOGRAPHY_PRESETS
        self.spacings = SPACING_PRESETS
        self.radii = RADIUS_PRESETS
        self.shadows = SHADOW_PRESETS
        self.animations = ANIMATION_PRESETS
        self.presets = PRESETS
        self.component_spacing = COMPONENT_SPACING

    def load_preset(self, preset_name: str) -> Dict[str, Any]:
        """加载一个完整预设，返回合并后的 Token 字典。"""
        if preset_name not in self.presets:
            available = ", ".join(self.presets.keys())
            raise ValueError(f"Unknown preset '{preset_name}'. Available: {available}")

        preset = self.presets[preset_name]
        tokens = {
            "meta": {
                "preset": preset_name,
                "name": preset["name"],
                "description": preset["description"],
            },
            "colors": self.palettes[preset["palette"]],
            "typography": self.typographies[preset["typography"]],
            "spacing": self.spacings[preset["spacing"]],
            "radius": self.radii[preset["radius"]],
            "shadow": self.shadows[preset["shadow"]],
            "animation": self.animations[preset["animation"]],
            "components": self.component_spacing,
        }
        return copy.deepcopy(tokens)

    def merge(self, base: Dict, overrides: Dict) -> Dict:
        """深度合并 overrides 到 base Token。"""
        result = copy.deepcopy(base)
        self._deep_merge(result, overrides)
        return result

    def _deep_merge(self, target: Dict, source: Dict):
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_merge(target[key], value)
            else:
                target[key] = copy.deepcopy(value)

    def save(self, tokens: Dict, path: str):
        """保存 Token 到 JSON 文件。"""
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(tokens, f, ensure_ascii=False, indent=2)

    def load(self, path: str) -> Dict:
        """从 JSON 文件加载 Token。"""
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def list_presets(self) -> List[Dict[str, str]]:
        """列出所有可用预设。"""
        return [
            {"id": k, "name": v["name"], "description": v["description"]}
            for k, v in self.presets.items()
        ]

    def list_palettes(self) -> List[str]:
        return list(self.palettes.keys())

    def list_typographies(self) -> List[str]:
        return list(self.typographies.keys())


# ============================================================
# CLI 入口
# ============================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Design Token Manager for Unity UXML")
    sub = parser.add_subparsers(dest="command")

    # list
    list_p = sub.add_parser("list", help="列出可用预设/色板/字体")
    list_p.add_argument("--type", choices=["presets", "palettes", "typographies", "spacings", "radii", "shadows"], default="presets")

    # export
    export_p = sub.add_parser("export", help="导出设计 Token 为 JSON")
    export_p.add_argument("--preset", required=True, help="预设名称")
    export_p.add_argument("--output", "-o", default=None, help="输出路径（默认 stdout）")
    export_p.add_argument("--override", action="append", default=[], help="覆盖 Token，格式 key.subkey=value")

    # merge
    merge_p = sub.add_parser("merge", help="合并多个 Token JSON")
    merge_p.add_argument("--base", required=True, help="基础 Token JSON")
    merge_p.add_argument("--patch", required=True, help="覆盖 Token JSON")
    merge_p.add_argument("--output", "-o", default=None, help="输出路径")

    args = parser.parse_args()
    mgr = DesignTokenManager()

    if args.command == "list":
        if args.type == "presets":
            for p in mgr.list_presets():
                print(f"  {p['id']:25s} | {p['name']:12s} | {p['description']}")
        elif args.type == "palettes":
            for name in mgr.list_palettes():
                print(f"  {name}")
        elif args.type == "typographies":
            for name in mgr.list_typographies():
                print(f"  {name}")
        elif args.type == "spacings":
            for name in SPACING_PRESETS:
                print(f"  {name}")
        elif args.type == "radii":
            for name in RADIUS_PRESETS:
                print(f"  {name}")
        elif args.type == "shadows":
            for name in SHADOW_PRESETS:
                print(f"  {name}")

    elif args.command == "export":
        tokens = mgr.load_preset(args.preset)
        # 应用覆盖
        for override in args.override:
            key, value = override.split("=", 1)
            parts = key.split(".")
            obj = tokens
            for part in parts[:-1]:
                obj = obj.setdefault(part, {})
            obj[parts[-1]] = value
        # 输出
        output = json.dumps(tokens, ensure_ascii=False, indent=2)
        if args.output:
            mgr.save(tokens, args.output)
            print(f"Saved to {args.output}")
        else:
            print(output)

    elif args.command == "merge":
        base = mgr.load(args.base)
        patch = mgr.load(args.patch)
        merged = mgr.merge(base, patch)
        output = json.dumps(merged, ensure_ascii=False, indent=2)
        if args.output:
            mgr.save(merged, args.output)
            print(f"Saved to {args.output}")
        else:
            print(output)

    else:
        parser.print_help()
