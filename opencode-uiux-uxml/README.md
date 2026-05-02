# opencode-uiux-uxml

将 UI/UX 设计知识直接转化为 Unity UI Toolkit 界面代码。

## 核心理念

**设计 Token 驱动**，不是 React 代码翻译。

```
设计 Token（色板/字体/间距/圆角/阴影）
        ↓
UXML 生成器（Token → USS → UXML → C#）
        ↓
UXML + USS + C# ViewModel + Model
```

## 与 opencode-unity-uixml 的区别

| 特性 | opencode-unity-uixml | opencode-uiux-uxml |
|------|---------------------|-------------------|
| 样式来源 | 硬编码 4 种预设 | 设计 Token 系统（10 预设 + 自定义） |
| 色板数量 | ~20 色 | 161 色板精选 |
| 字体搭配 | 1 种 | 57 组精选 |
| 间距系统 | 无 | 5 种预设（4px 基准网格） |
| 圆角系统 | 无 | 6 种预设 |
| 阴影系统 | 无 | 6 种预设 |
| 组件尺寸规范 | 无 | 9 类组件标准化尺寸 |
| 动画/过渡 | 无 | 6 种预设 |
| Token 可导出 | ❌ | ✅ JSON 格式 |
| Token 可合并 | ❌ | ✅ 深度合并 |
| 自定义覆盖 | ❌ | ✅ CLI --override |

## 快速开始

### 使用预设

```bash
python uxml_generator.py --tokens dark_glassmorphism --name Login --desc "用户名输入框、密码输入框、登录按钮"
```

### 使用自定义 Token

```bash
# 先导出 Token JSON
python design_tokens.py export --preset midnight_aurora -o my_theme.json

# 修改 my_theme.json 中的颜色/字体...

# 用自定义 Token 生成
python uxml_generator.py --tokens my_theme.json --name Inventory --desc "背包格子、详情面板、使用按钮"
```

### MVP 模式

```bash
python uxml_generator.py --tokens game_fantasy --name Settings --desc "音量滑块、画质下拉框" --pattern mvp
```

### 覆盖单个 Token

```bash
python uxml_generator.py --tokens dark_glassmorphism --name Login --desc "用户名输入框、登录按钮" --override colors.primary=#FF6B6B
```

## 可用预设

| ID | 名称 | 风格 |
|----|------|------|
| `dark_glassmorphism` | 暗色毛玻璃 | 半透明 + 柔和光晕 |
| `midnight_aurora` | 午夜极光 | 深蓝 + 紫色渐变 |
| `cyber_neon` | 赛博霓虹 | 纯黑 + 霓虹发光边框 |
| `warm_dark` | 暖色暗调 | 深棕暖色 |
| `light_minimal` | 亮色极简 | 白底蓝调 |
| `light_claymorphism` | 亮色黏土 | 奶油底 + 圆润边角 |
| `game_fantasy` | 奇幻游戏 | 暗金 + 发光边框 |
| `game_scifi` | 科幻游戏 | 深蓝 + 蓝橙配色 |
| `game_horror` | 恐怖游戏 | 极暗 + 血红/暗紫 |
| `game_pixel_retro` | 像素复古 | 灰底 + 像素字体 |

## 架构模式选择

| 场景 | 推荐模式 | 理由 |
|------|---------|------|
| 数据展示 | MVVM | 数据绑定自动同步 |
| 复杂交互 | MVP | Presenter 集中处理逻辑 |
| 表单/设置 | MVVM | 双向绑定简化输入 |
| 游戏 HUD | MVP | 性能更优 |

## 输出文件

| 文件 | 说明 | MVVM | MVP |
|------|------|------|-----|
| `{Name}.uxml` | 界面结构 | ✅ | ✅ |
| `{Name}.uss` | 样式表（Token 驱动） | ✅ | ✅ |
| `{Name}ViewModel.cs` | ViewModel | ✅ | - |
| `{Name}Presenter.cs` | Presenter | - | ✅ |
| `{Name}Model.cs` | 数据模型 | ✅ | - |
| `design_tokens.json` | 使用的设计 Token | ✅ | ✅ |

## 设计 Token 结构

```json
{
  "meta": { "preset": "dark_glassmorphism", "name": "暗色毛玻璃" },
  "colors": {
    "primary": "#A78BFA",
    "background": "#0F0F1A",
    "surface": "rgba(30,30,50,0.7)",
    "border": "rgba(139,92,246,0.3)",
    ...
  },
  "typography": {
    "heading": { "family": "Noto Sans SC", "weight": "bold", "sizes": {"h1": 32, ...} },
    "body": { "family": "Noto Sans SC", "weight": "normal", "sizes": {"md": 14, ...} },
    "mono": { "family": "JetBrains Mono", ... },
    "line_height": 1.5,
    "letter_spacing": { "heading": -0.02, "body": 0, "mono": 0.05 }
  },
  "spacing": { "xs": 4, "sm": 8, "md": 12, "lg": 16, "xl": 24, "2xl": 32, "3xl": 48 },
  "radius": { "none": 0, "xs": 2, "sm": 4, "md": 6, "lg": 8, "xl": 12, "full": 999 },
  "shadow": { "sm": "0 1px 2px rgba(0,0,0,0.1)", ... },
  "animation": { "duration_ms": 300, "easing": "ease-in-out" },
  "components": {
    "input": { "height": 36, "padding_h": 12, "gap": 8 },
    "button": { "height": 36, "padding_h": 16, "min_width": 80 },
    "card": { "padding": 16, "gap": 12 },
    ...
  }
}
```

## 依赖

- Python 3.8+
- Unity 2023.2+（数据绑定需要 `[CreateProperty]`）
- PyYAML（可选，YAML 规格模式需要）
