#!/usr/bin/env python3
"""
opencode-uiux-uxml 示例集合
=============================
6 个常见界面，涵盖不同预设和架构模式
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from design_tokens import DesignTokenManager
from uxml_generator import UIParser, UXMLGenerator


def example_login():
    """登录界面 — 暗色毛玻璃 + MVVM"""
    tokens = DesignTokenManager().load_preset("dark_glassmorphism")
    parser = UIParser(tokens)
    components = parser.parse("标题:用户登录, 用户名输入框, 密码输入框, 登录按钮, 注册按钮")
    gen = UXMLGenerator(tokens, pattern="mvvm")
    return gen.generate("Login", components, layout="vertical")


def example_inventory():
    """背包界面 — 奇幻游戏 + MVP"""
    tokens = DesignTokenManager().load_preset("game_fantasy")
    parser = UIParser(tokens)
    components = parser.parse("标题:背包, 搜索框, 滚动区域, 物品格子, 详情面板, 使用按钮, 删除按钮")
    gen = UXMLGenerator(tokens, pattern="mvp")
    return gen.generate("Inventory", components, layout="horizontal")


def example_settings():
    """设置界面 — 午夜极光 + MVVM"""
    tokens = DesignTokenManager().load_preset("midnight_aurora")
    parser = UIParser(tokens)
    components = parser.parse("标题:设置, 音量滑块, 音乐音量滑块, 画质下拉框, 全屏开关, 语言下拉框, 保存按钮, 取消按钮")
    gen = UXMLGenerator(tokens, pattern="mvvm")
    return gen.generate("Settings", components, layout="vertical")


def example_hud():
    """玩家 HUD — 科幻游戏 + MVP"""
    tokens = DesignTokenManager().load_preset("game_scifi")
    parser = UIParser(tokens)
    components = parser.parse("血条, 魔法条, 经验条, 小地图, 技能栏, 快捷栏, 伤害数字, 任务追踪")
    gen = UXMLGenerator(tokens, pattern="mvp")
    return gen.generate("PlayerHUD", components, layout="vertical")


def example_dialog():
    """对话框 — 暖色暗调 + MVP"""
    tokens = DesignTokenManager().load_preset("warm_dark")
    parser = UIParser(tokens)
    components = parser.parse("标题:确认操作, 说明文字:确定要删除这个存档吗？此操作无法撤销。, 确认按钮, 取消按钮")
    gen = UXMLGenerator(tokens, pattern="mvp")
    return gen.generate("ConfirmDialog", components, layout="vertical")


def example_shop():
    """商店界面 — 赛博霓虹 + MVVM"""
    tokens = DesignTokenManager().load_preset("cyber_neon")
    parser = UIParser(tokens)
    components = parser.parse("标题:数据商店, 搜索框, 滚动区域, 物品格子, 金币, 钻石, 购买按钮, 刷新按钮")
    gen = UXMLGenerator(tokens, pattern="mvvm")
    return gen.generate("CyberShop", components, layout="vertical")


def example_horror_hud():
    """恐怖游戏 HUD — 恐怖暗色 + MVP"""
    tokens = DesignTokenManager().load_preset("game_horror")
    parser = UIParser(tokens)
    components = parser.parse("血条, 体力条, 提示文字, 小地图, 战斗日志")
    gen = UXMLGenerator(tokens, pattern="mvp")
    return gen.generate("HorrorHUD", components, layout="vertical")


# ============================================================
# 批量生成
# ============================================================

if __name__ == "__main__":
    examples = [
        ("Login", example_login),
        ("Inventory", example_inventory),
        ("Settings", example_settings),
        ("PlayerHUD", example_hud),
        ("ConfirmDialog", example_dialog),
        ("CyberShop", example_shop),
        ("HorrorHUD", example_horror_hud),
    ]

    base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "Output")
    base_dir = os.path.normpath(base_dir)

    for name, func in examples:
        print(f"\n{'='*50}")
        print(f"  Generating: {name}")
        print(f"{'='*50}")
        files = func()
        out_dir = os.path.join(base_dir, name)
        os.makedirs(out_dir, exist_ok=True)
        for filename, content in files.items():
            if not content:
                continue
            path = os.path.join(out_dir, filename)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  ✓ {path}")

    print(f"\n✅ All {len(examples)} examples generated → {base_dir}")
