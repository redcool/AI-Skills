# opencode-uiux-uxml — Skill 说明

> 将 UI/UX 设计规范（Design Token）直接转化为 Unity UI Toolkit 界面代码
> 设计 Token 驱动 → 不经过 React 中转 → 零翻译损耗

## 何时使用

- 用户需要创建 Unity 界面（UXML/USS/C#）
- 用户关心界面美观度和设计一致性
- 用户需要数据与界面代码分离（MVVM/MVP）
- 用户想用特定设计风格（暗色毛玻璃/赛博霓虹/奇幻游戏等）

## 核心文件

| 文件 | 说明 |
|------|------|
| `design_tokens.py` | 设计 Token 系统（10 预设 + 161 色板 + 57 字体 + 5 间距 + 6 圆角 + 6 阴影） |
| `uxml_generator.py` | UXML/USS/C# 生成器（Token 驱动） |

## 使用方式

### 方式一：预设 + 自然语言

```bash
python uxml_generator.py --tokens <预设名> --name <界面名> --desc "<中文描述>"
```

预设名：`dark_glassmorphism` | `midnight_aurora` | `cyber_neon` | `warm_dark` | `light_minimal` | `light_claymorphism` | `game_fantasy` | `game_scifi` | `game_horror` | `game_pixel_retro`

### 方式二：自定义 Token JSON

```bash
# 导出预设为 JSON
python design_tokens.py export --preset <预设名> -o my_theme.json

# 用自定义 Token 生成
python uxml_generator.py --tokens my_theme.json --name <界面名> --desc "<描述>"
```

### 方式三：覆盖单个 Token

```bash
python uxml_generator.py --tokens dark_glassmorphism --name Login --desc "输入框、按钮" --override colors.primary=#FF6B6B --override spacing.md=16
```

### 方式四：YAML 规格

```bash
python uxml_generator.py --tokens game_fantasy --yaml spec.yaml
```

## 架构模式

- `--pattern mvvm`（默认）：数据绑定 `[CreateProperty]` + `BindProperty`，适合表单/数据展示
- `--pattern mvp`：Presenter 事件驱动，适合复杂交互/游戏 HUD

## 输出

每次生成输出到 `--out` 目录（默认 `./Output/<界面名>/`）：

- `{Name}.uxml` — 界面结构
- `{Name}.uss` — 样式表（Token 驱动）
- `{Name}ViewModel.cs` 或 `{Name}Presenter.cs` — 逻辑层
- `{Name}Model.cs` — 数据模型（仅 MVVM）
- `design_tokens.json` — 使用的设计 Token（可用于后续修改/复用）

## 设计 Token 查询

```bash
# 列出所有预设
python design_tokens.py list

# 列出色板
python design_tokens.py list --type palettes

# 列出字体搭配
python design_tokens.py list --type typographies
```

## 关键设计决策

1. **不经过 React 中转**：CSS → USS 翻译有损（无 backdrop-filter、无 CSS Grid、动画受限），直接用 USS 能力上限做最好效果
2. **Token 是框架无关的**：色板/字体/间距/圆角是设计语言，不是 React 代码
3. **组件尺寸标准化**：9 类组件（input/button/card/list_item/toolbar/tab/dialog/tooltip/hud）有统一的尺寸规范
4. **USS 降级策略**：毛玻璃 → 半透明色块，CSS Grid → Flex 嵌套，复杂渐变 → 单色

## 中文组件映射

支持 80+ 中文组件名自动映射到 UI Toolkit 组件类型：

- 容器类：容器/面板/卡片/滚动区域/模态框 → VisualElement / ScrollView
- 输入类：输入框/密码框/搜索框/滑块/下拉框/开关 → TextField / Slider / DropdownField / Toggle
- 按钮类：按钮/登录按钮/删除按钮/图标按钮 → Button
- 显示类：标题/文字/图标/图片/进度条/血条 → Label / Image / ProgressBar
- 复合类：列表/折叠面板/标签页/工具栏 → ListView / Foldout / TabView / Toolbar
- 游戏类：血条/技能栏/背包格子/小地图/伤害数字 → ProgressBar / VisualElement / Image / Label
