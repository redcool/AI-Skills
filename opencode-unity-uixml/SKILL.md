---
name: opencode-unity-uixml
description: |
  Unity UI Toolkit 界面生成器。从自然语言描述或YAML规格生成完整的UXML+USS+C#界面组件，支持MVVM/MVP模式。
  
  触发场景：
  - 用户提到"Unity界面"、"UXML"、"UI Toolkit"
  - 用户想要生成游戏UI（登录、背包、设置、HUD等）
  - 用户提到MVVM、MVP、数据绑定
  
keywords: [Unity, UXML, USS, UI Toolkit, MVVM, MVP, 界面, 数据绑定]
---

# Unity UI Toolkit 界面生成器

AI驱动的Unity界面生成工具，自动生成UXML结构、USS样式、C#事件代码和数据绑定。

## 快速开始

```bash
# 自然语言描述
python unity_uixml_generator.py --name Login --desc "用户名输入框、密码输入框、登录按钮" --out ./Output/Login

# 使用YAML规格文件
python unity_uixml_generator.py --name Inventory --yaml inventory.yaml --style game_fantasy --out ./Output/Inventory

# MVP模式
python unity_uixml_generator.py --name Settings --desc "音量滑块、画质下拉框、保存按钮" --pattern mvp
```

## 输出文件

每个界面生成3-4个文件：

| 文件 | 说明 |
|------|------|
| `{Name}.uxml` | UXML界面结构 |
| `{Name}.uss` | USS样式表 |
| `{Name}ViewModel.cs` | ViewModel/Presenter代码 |
| `{Name}Model.cs` | 数据模型（仅MVVM） |

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--name` | ✅ | UI名称（如Login、Inventory） |
| `--desc` | ❌ | 自然语言描述（中文/英文） |
| `--yaml` | ❌ | YAML规格文件路径 |
| `--out` | ❌ | 输出目录，默认 `./Output` |
| `--pattern` | ❌ | 设计模式：`mvvm`/`mvp`，默认 `mvvm` |
| `--style` | ❌ | 样式预设：`dark`/`light`/`game_fantasy`/`game_sci-fi` |
| `--namespace` | ❌ | C#命名空间，默认 `Game.UI` |

## 样式预设

| 预设 | 适用场景 | 主色调 |
|------|---------|--------|
| `dark` | 编辑器工具、设置界面 | 深灰 #1E1E1E |
| `light` | 移动端、休闲游戏 | 浅灰 #F5F5F5 |
| `game_fantasy` | 奇幻RPG、东方风格 | 深紫 #1A1A2E + 金色 #D4AF37 |
| `game_sci-fi` | 科幻、赛博朋克 | 深蓝 #0A1015 + 青色 #00FFFF |

## 工作流程

### 阶段1：界面生成

```
用户描述 → 解析组件 → 生成UXML → 生成USS → 生成C#
```

输入示例：
```
登录界面：用户名输入框、密码输入框、登录按钮、注册链接
```

生成：
- `Login.uxml` - 界面结构
- `Login.uss` - 暗色主题样式
- `LoginViewModel.cs` - 包含Username、Password绑定属性和OnLoginClicked事件

### 阶段2：事件代码生成

在界面生成后，用户可进一步描述交互逻辑：

```
点击登录按钮时：
1. 验证用户名不为空
2. 验证密码长度>=6
3. 调用LoginAPI
4. 成功后跳转主界面
```

生成的事件处理代码：
```csharp
private void OnLoginClicked()
{
    if (string.IsNullOrEmpty(Username))
    {
        ShowError("请输入用户名");
        return;
    }
    
    if (Password.Length < 6)
    {
        ShowError("密码长度至少6位");
        return;
    }
    
    LoginAPI.Login(Username, Password, OnLoginSuccess, OnLoginFailed);
}

private void OnLoginSuccess()
{
    SceneManager.LoadScene("MainScene");
}
```

## 组件映射

支持中文描述自动识别：

| 中文 | UXML组件 |
|------|---------|
| 输入框/文本框 | TextField |
| 密码框 | TextField (is-password) |
| 按钮 | Button |
| 文本/标签 | Label |
| 图片/图标 | Image |
| 滑块/滑动条 | Slider |
| 开关/复选框 | Toggle |
| 下拉框 | DropdownField |
| 列表 | ListView |
| 滚动视图 | ScrollView |
| 进度条/血条 | ProgressBar |

## 文件结构

```
Output/
└── {UIName}/
    ├── {UIName}.uxml
    ├── {UIName}.uss
    ├── {UIName}ViewModel.cs   # MVVM模式
    └── {UIName}Model.cs       # MVVM模式
```

或

```
Output/
└── {UIName}/
    ├── {UIName}.uxml
    ├── {UIName}.uss
    └── {UIName}Presenter.cs   # MVP模式
```

## 注意事项

1. **Unity版本要求**: Unity 2023.2+（数据绑定需要）
2. **命名空间**: 确保与项目命名空间一致
3. **样式文件**: 需要放到 `Assets/UI/Styles/` 目录
4. **UXML引用**: 需要修正UXML中的Style GUID

## 后续集成

生成的文件需要：
1. 将UXML/USS放入Unity项目的 `Assets/UI/` 目录
2. 将C#脚本放入 `Assets/Scripts/` 目录
3. 在场景中创建UIDocument，引用UXML
4. 将ViewModel/Presenter挂载到UIDocument所在的GameObject

## 参考文档

- `references/uxml-components.md` - UI Toolkit组件完整参考
- `references/mvvm-pattern.md` - MVVM/MVP模式实现指南
- `references/yaml-spec-examples.md` - YAML规格文件示例
