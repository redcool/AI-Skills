# 界面规格示例

## 示例1：登录界面

```yaml
name: Login
description: |
  登录界面：用户名输入框、密码输入框、登录按钮、注册链接、忘记密码链接
namespace: Game.UI
pattern: mvvm
style: dark

elements:
  - type: VisualElement
    name: login-container
    class: panel
    
  - type: Label
    name: title
    text: "用户登录"
    parent: login-container
    
  - type: TextField
    name: username
    label: "用户名"
    placeholder: "请输入用户名"
    parent: login-container
    binding: Username
    
  - type: TextField
    name: password
    label: "密码"
    is-password: true
    placeholder: "请输入密码"
    parent: login-container
    binding: Password
    
  - type: Button
    name: login-btn
    text: "登录"
    parent: login-container
    event: OnLoginClicked
    
  - type: VisualElement
    name: links-container
    parent: login-container
    
  - type: Label
    name: register-link
    text: "注册账号"
    parent: links-container
    event: OnRegisterClicked
    
  - type: Label
    name: forgot-link
    text: "忘记密码"
    parent: links-container
    event: OnForgotPasswordClicked
```

---

## 示例2：背包界面

```yaml
name: Inventory
description: |
  背包界面：标题栏、64格网格、物品详情面板、使用/丢弃按钮
namespace: Game.UI
pattern: mvp
style: game_fantasy

elements:
  - type: VisualElement
    name: inventory-container
    class: panel
    
  - type: Label
    name: title
    text: "背包"
    parent: inventory-container
    
  - type: ScrollView
    name: item-grid-scroll
    parent: inventory-container
    
  - type: VisualElement
    name: item-grid
    class: grid-container
    parent: item-grid-scroll
    # 8x8 grid, 64 slots
    
  - type: VisualElement
    name: detail-panel
    class: detail-panel
    parent: inventory-container
    
  - type: Image
    name: item-icon
    parent: detail-panel
    
  - type: Label
    name: item-name
    parent: detail-panel
    binding: SelectedItemName
    
  - type: Label
    name: item-desc
    parent: detail-panel
    binding: SelectedItemDesc
    
  - type: VisualElement
    name: item-stats
    parent: detail-panel
    
  - type: Button
    name: use-btn
    text: "使用"
    parent: detail-panel
    event: OnUseItemClicked
    
  - type: Button
    name: drop-btn
    text: "丢弃"
    parent: detail-panel
    event: OnDropItemClicked
```

---

## 示例3：设置界面

```yaml
name: Settings
description: |
  设置界面：音量滑块、画质下拉、全屏开关、保存/取消按钮
namespace: Game.UI
pattern: mvvm
style: dark

elements:
  - type: VisualElement
    name: settings-container
    
  - type: Label
    name: title
    text: "游戏设置"
    
  - type: Label
    name: audio-label
    text: "音效设置"
    
  - type: Slider
    name: master-volume
    label: "主音量"
    low-value: 0
    high-value: 100
    value: 80
    binding: MasterVolume
    
  - type: Slider
    name: music-volume
    label: "音乐"
    low-value: 0
    high-value: 100
    value: 70
    binding: MusicVolume
    
  - type: Slider
    name: sfx-volume
    label: "音效"
    low-value: 0
    high-value: 100
    value: 90
    binding: SfxVolume
    
  - type: Label
    name: video-label
    text: "画面设置"
    
  - type: DropdownField
    name: quality
    label: "画质"
    choices: "低,中,高,超高"
    index: 2
    binding: QualityLevel
    
  - type: Toggle
    name: fullscreen
    label: "全屏"
    value: true
    binding: IsFullscreen
    
  - type: Toggle
    name: vsync
    label: "垂直同步"
    value: true
    binding: VSyncEnabled
    
  - type: VisualElement
    name: button-row
    
  - type: Button
    name: save-btn
    text: "保存"
    event: OnSaveClicked
    
  - type: Button
    name: cancel-btn
    text: "取消"
    event: OnCancelClicked
```

---

## 示例4：玩家HUD

```yaml
name: PlayerHUD
description: |
  玩家HUD：头像、血条、蓝条、经验条、金币、等级
namespace: Game.UI
pattern: mvp
style: game_fantasy

elements:
  - type: VisualElement
    name: hud-container
    
  - type: VisualElement
    name: player-info
    
  - type: Image
    name: avatar
    
  - type: VisualElement
    name: bars-container
    
  - type: Label
    name: hp-label
    binding: HpText
    
  - type: ProgressBar
    name: hp-bar
    binding: HpPercent
    
  - type: Label
    name: mp-label
    binding: MpText
    
  - type: ProgressBar
    name: mp-bar
    binding: MpPercent
    
  - type: Label
    name: exp-label
    binding: ExpText
    
  - type: ProgressBar
    name: exp-bar
    binding: ExpPercent
    
  - type: VisualElement
    name: stats-row
    
  - type: Label
    name: level-text
    binding: LevelText
    
  - type: Label
    name: gold-text
    binding: GoldText
```

---

## YAML字段说明

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | ✅ | UI名称（用于文件命名） |
| `description` | ✅ | 界面功能描述 |
| `namespace` | ❌ | C#命名空间，默认 `Game.UI` |
| `pattern` | ❌ | 设计模式：`mvvm` 或 `mvp`，默认 `mvvm` |
| `style` | ❌ | 样式预设，默认 `dark` |
| `elements` | ✅ | UI元素列表 |

### 元素字段

| 字段 | 说明 |
|------|------|
| `type` | UI Toolkit组件类型 |
| `name` | 元素名称（用于C#查询） |
| `text` | 默认文本 |
| `parent` | 父元素名称 |
| `class` | CSS类名 |
| `binding` | 数据绑定路径 |
| `event` | 事件处理方法名 |
