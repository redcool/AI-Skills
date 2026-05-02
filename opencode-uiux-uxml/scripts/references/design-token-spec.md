# Design Token 完整规范

设计 Token 是框架无关的设计决策集合。本文档定义 Token 的完整结构、所有可选值、以及扩展规范。

## 1. Token 完整结构

```json
{
  "meta": {
    "preset": "string — 预设ID",
    "name": "string — 预设中文名",
    "description": "string — 描述",
    "version": "string — Token 版本（语义化版本）",
    "author": "string — 作者"
  },
  "colors": { /* 见 §2 */ },
  "typography": { /* 见 §3 */ },
  "spacing": { /* 见 §4 */ },
  "radius": { /* 见 §5 */ },
  "shadow": { /* 见 §6 */ },
  "animation": { /* 见 §7 */ },
  "components": { /* 见 §8 */ }
}
```

## 2. 颜色 Token

### 2.1 必需字段

| Token | 说明 | 示例 |
|-------|------|------|
| `primary` | 主色调（按钮/重点） | `#6366F1` |
| `primary_variant` | 主色深色变体（hover/pressed） | `#4F46E5` |
| `secondary` | 辅助色 | `#8B5CF6` |
| `background` | 页面背景 | `#0B0F1A` |
| `surface` | 卡片/面板背景 | `#151B2E` |
| `card` | 卡片专用背景 | `#1A2038` |
| `error` | 错误/危险 | `#EF4444` |
| `success` | 成功/确认 | `#10B981` |
| `warning` | 警告 | `#F59E0B` |
| `info` | 信息提示 | `#3B82F6` |
| `on_primary` | 主色上的文字 | `#FFFFFF` |
| `on_background` | 背景上的文字 | `#E2E8F0` |
| `on_surface` | Surface 上的文字 | `#CBD5E1` |
| `border` | 默认边框色 | `#2D3A5C` |
| `border_focus` | 焦点边框色 | `#6366F1` |

### 2.2 可选字段

| Token | 说明 | 示例 |
|-------|------|------|
| `secondary_variant` | 辅助色深色变体 | `#7C3AED` |
| `surface_variant` | 区别于 surface 的变体 | `#1E2642` |
| `on_surface_variant` | 次要文字 | `#94A3B8` |
| `disabled` | 禁用态文字/图标 | `#475569` |
| `disabled_bg` | 禁用态背景 | `#1E293B` |
| `overlay` | 遮罩层 | `rgba(0,0,0,0.6)` |
| `scrim` | 全屏遮罩 | `rgba(0,0,0,0.85)` |

### 2.3 颜色值格式

USS 支持的颜色格式：
- `#RRGGBB` — 六位十六进制
- `#RRGGBBAA` — 含透明度
- `rgba(r, g, b, a)` — 函数式（USS 2023.1+）

❌ 不支持：`hsl()`, `hsla()`, `rgb()`, CSS 颜色关键字（`red`, `blue` 等）

## 3. 字体 Token

```json
{
  "heading": {
    "family": "字体族名",
    "weight": "bold | normal",
    "sizes": {
      "h1": 32, "h2": 24, "h3": 20,
      "h4": 18, "h5": 16, "h6": 14
    }
  },
  "body": {
    "family": "字体族名",
    "weight": "bold | normal",
    "sizes": {
      "lg": 16, "md": 14, "sm": 12, "xs": 10
    }
  },
  "mono": {
    "family": "等宽字体族名",
    "weight": "normal",
    "sizes": {
      "md": 13, "sm": 11
    }
  },
  "line_height": 1.5,
  "letter_spacing": {
    "heading": -0.02,
    "body": 0,
    "mono": 0.05
  }
}
```

### 可用字体族

| 类别 | 推荐字体 | 说明 |
|------|---------|------|
| 中文无衬线 | Noto Sans SC | 通用中文 UI 字体 |
| 中文衬线 | Noto Serif SC | 文学/古典风格 |
| 中文艺术 | ZCOOL QingKe HuangYou | 奇幻/标题 |
| 英文无衬线 | Inter / Roboto / Rajdhani | 现代科技 |
| 英文衬线 | Merriweather / Playfair Display | 优雅古典 |
| 等宽 | JetBrains Mono / Fira Code / Source Code Pro | 代码/数字 |
| 游戏像素 | Press Start 2P | 复古像素 |
| 游戏科幻 | Orbitron / Rajdhani | 科技风标题 |
| 游戏 Gothic | UnifrakturMaguntia | 恐怖/哥特 |

## 4. 间距 Token

```json
{
  "xs": 4,
  "sm": 8,
  "md": 12,
  "lg": 16,
  "xl": 24,
  "2xl": 32,
  "3xl": 48
}
```

**规则**：基于 4px 网格，每个层级 ≥ 上一层级 × 1.5。

### 间距预设

| 预设 | 风格 | xs→3xl |
|------|------|--------|
| compact | 紧凑 | 2,4,8,12,16,20,24 |
| standard | 标准 | 4,8,12,16,24,32,48 |
| comfortable | 宽松 | 6,12,16,24,32,48,64 |
| game_dense | 游戏密集 | 2,4,6,8,12,16,20 |
| game_spacious | 游戏宽松 | 6,10,14,20,28,40,56 |

## 5. 圆角 Token

```json
{
  "none": 0,
  "xs": 2,
  "sm": 4,
  "md": 6,
  "lg": 8,
  "xl": 12,
  "full": 999
}
```

### 圆角预设

| 预设 | 风格 | 适用场景 |
|------|------|---------|
| sharp | 直角 | 硬核科幻/军事 |
| standard | 标准圆角 | 通用 UI |
| rounded | 大圆角 | 友好/儿童/黏土 |
| pill | 胶囊 | 标签/开关 |
| game_hard | 游戏硬朗 | 策略/军事游戏 |
| game_fantasy | 游戏奇幻 | RPG/奇幻 |

## 6. 阴影 Token

```json
{
  "sm": "0 1px 2px rgba(0,0,0,0.1)",
  "md": "0 2px 4px rgba(0,0,0,0.12)",
  "lg": "0 4px 8px rgba(0,0,0,0.14)",
  "xl": "0 8px 16px rgba(0,0,0,0.16)"
}
```

USS 阴影格式：`offset-x offset-y blur color`

### 游戏风格发光阴影

游戏 UI 常用发光效果代替传统阴影：

```json
{
  "sm": "0 0 6px rgba(0,191,255,0.3)",
  "md": "0 0 10px rgba(0,191,255,0.4)",
  "lg": "0 0 14px rgba(0,191,255,0.5)",
  "xl": "0 0 20px rgba(0,191,255,0.6)"
}
```

颜色选择：
- 科幻蓝光：`rgba(0,191,255,0.x)`
- 奇幻金光：`rgba(212,164,76,0.x)`
- 恐怖红光：`rgba(139,0,0,0.x)`
- 霓虹绿光：`rgba(0,255,136,0.x)`

## 7. 动画 Token

```json
{
  "duration_ms": 200,
  "easing": "ease-out"
}
```

### 预设

| 预设 | 时长 | 缓动 | 适用 |
|------|------|------|------|
| none | 0 | linear | 无动画 |
| fast | 100ms | ease-out | 微交互 |
| standard | 200ms | ease-out | 通用 |
| smooth | 300ms | ease-in-out | 强调 |
| game_snappy | 80ms | ease-out | 游戏即时反馈 |
| game_dramatic | 500ms | ease-in-out | 游戏大动作 |

USS 支持的缓动函数：`linear`, `ease-in`, `ease-out`, `ease-in-out`, `ease`

## 8. 组件尺寸 Token

```json
{
  "input": {
    "height": 36,
    "padding_h": 12,
    "padding_v": 8,
    "gap": 8,
    "icon_size": 18
  },
  "button": {
    "height": 36,
    "padding_h": 16,
    "padding_v": 8,
    "min_width": 80,
    "gap": 6,
    "icon_size": 18
  },
  "card": {
    "padding": 16,
    "gap": 12,
    "header_height": 40
  },
  "list_item": {
    "height": 48,
    "padding_h": 16,
    "gap": 12,
    "avatar_size": 32
  },
  "toolbar": {
    "height": 48,
    "padding_h": 12,
    "gap": 8,
    "icon_size": 22
  },
  "tab": {
    "height": 40,
    "padding_h": 16,
    "gap": 0,
    "indicator_height": 3
  },
  "dialog": {
    "padding": 24,
    "gap": 16,
    "min_width": 320,
    "max_width": 560
  },
  "tooltip": {
    "padding_h": 8,
    "padding_v": 4,
    "max_width": 240
  },
  "hud": {
    "padding": 8,
    "gap": 6,
    "icon_size": 20,
    "bar_height": 8
  }
}
```

## 9. Token 扩展指南

### 9.1 添加新色板

```python
# 在 design_tokens.py 的 COLOR_PALETTES 中添加：
COLOR_PALETTES["my_custom"] = {
    "primary": "#FF6B6B",
    "primary_variant": "#E05555",
    # ... 填写所有必需字段
}
```

### 9.2 添加新预设组合

```python
PRESETS["my_preset"] = {
    "name": "我的预设",
    "description": "描述",
    "palette": "my_custom",
    "typography": "modern_sans",
    "spacing": "standard",
    "radius": "rounded",
    "shadow": "subtle",
    "animation": "smooth",
}
```

### 9.3 从 ui-ux-pro-max 提取 Token

ui-ux-pro-max 的 161 色板和 57 字体搭配可以直接映射为 Token：
1. 选取色板中的 5-7 个核心色
2. 映射到 Token 的 primary/secondary/background/surface/on_*/border 体系
3. 选取字体搭配
4. 根据风格选择 spacing/radius/shadow/animation 预设

### 9.4 Token 版本管理

```json
{
  "meta": {
    "version": "1.0.0",
    "changelog": [
      {"1.0.0": "初始版本"},
      {"1.1.0": "增加 game_horror 预设"}
    ]
  }
}
```
