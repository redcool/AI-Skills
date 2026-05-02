# Unity UI Toolkit 界面生成器

AI驱动的Unity界面生成工具，从自然语言描述自动生成完整的UXML+USS+C#界面组件。

## 特性

- 🎨 **自然语言输入**：用中文描述界面，自动识别组件
- 🏗️ **双模式支持**：MVVM数据绑定 / MVP事件驱动
- 🎭 **多种样式预设**：暗色、亮色、奇幻、科幻
- 📦 **完整输出**：UXML + USS + C# ViewModel/Model

## 快速开始

```bash
# 生成登录界面
python unity_uixml_generator.py --name Login --desc "用户名输入框、密码输入框、登录按钮" --out ./Output/Login

# 生成背包界面（奇幻风格）
python unity_uixml_generator.py --name Inventory --desc "64格物品网格、详情面板、使用按钮" --style game_fantasy

# 使用YAML规格文件
python unity_uixml_generator.py --yaml spec.yaml --out ./Output/Inventory
```

## 输出示例

```
Output/
└── Login/
    ├── Login.uxml           # 界面结构
    ├── Login.uss            # 样式表
    ├── LoginViewModel.cs    # ViewModel（MVVM）
    └── LoginModel.cs        # 数据模型（MVVM）
```

## 设计模式

### MVVM（推荐）

```
Model ←── ViewModel ←── View(UXML)
```

- 数据自动同步
- 适合数据展示型界面
- Unity 2023.2+ 原生支持

### MVP

```
Model ←── Presenter ←── View(UXML)
```

- 手动事件处理
- 适合复杂交互界面
- 性能更优

## 样式预设

| 预设 | 风格 | 适用场景 |
|------|------|---------|
| `dark` | 深灰科技风 | 编辑器工具、设置界面 |
| `light` | 浅灰简约风 | 移动端、休闲游戏 |
| `game_fantasy` | 紫金奇幻风 | RPG、东方风格游戏 |
| `game_sci-fi` | 青蓝科幻风 | 科幻、赛博朋克游戏 |

## 中文组件映射

| 描述 | 组件 |
|------|------|
| 输入框、文本框 | TextField |
| 密码框 | TextField (password) |
| 按钮 | Button |
| 文本、标签 | Label |
| 图片、图标 | Image |
| 滑块、滑动条 | Slider |
| 开关、复选框 | Toggle |
| 下拉框 | DropdownField |
| 进度条、血条 | ProgressBar |
| 滚动列表 | ScrollView |

## 工作流程

### 第一步：界面生成

用自然语言描述界面结构：

```
背包界面：标题、64格网格、物品详情、使用/丢弃按钮
```

### 第二步：事件代码生成

界面生成后，进一步描述交互逻辑：

```
点击使用按钮时：
1. 检查是否选中物品
2. 调用UseItem方法
3. 刷新背包列表
```

生成对应的C#事件处理代码。

## 目录结构

```
opencode-unity-uixml/
├── unity_uixml_generator.py   # 主脚本
├── SKILL.md                   # Skill说明
├── README.md                  # 本文件
├── examples/
│   └── examples.py            # 示例脚本
└── scripts/
    └── references/
        ├── uxml-components.md  # 组件参考
        ├── mvvm-pattern.md     # MVVM/MVP指南
        └── yaml-spec-examples.md  # YAML示例
```

## 依赖

- Python 3.8+
- PyYAML（使用YAML规格时）

```bash
pip install pyyaml
```

## 注意事项

1. Unity版本要求2023.2+（数据绑定功能）
2. 生成的UXML样式引用需要手动修正GUID
3. 将生成的文件放入Unity项目对应目录

## 许可证

MIT
