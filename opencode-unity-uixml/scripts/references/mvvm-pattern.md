# MVVM/MVP 模式实现指南

## 架构概述

### MVVM (Model-View-ViewModel)

```
┌─────────────┐       ┌──────────────┐       ┌─────────────┐
│    Model    │◄──────│  ViewModel   │◄──────│    View     │
│  (数据层)   │       │  (绑定层)    │       │  (UI层)     │
└─────────────┘       └──────────────┘       └─────────────┘
     数据实体              数据绑定              UXML/USS
```

- **Model**: 纯数据类，不依赖Unity
- **ViewModel**: 使用 `[CreateProperty]` 暴露绑定属性
- **View**: UXML定义结构，USS定义样式

### MVP (Model-View-Presenter)

```
┌─────────────┐       ┌──────────────┐       ┌─────────────┐
│    Model    │◄──────│   Presenter  │◄──────│    View     │
│  (数据层)   │       │   (逻辑层)   │       │  (UI层)     │
└─────────────┘       └──────────────┘       └─────────────┘
     数据实体              事件处理              UXML/USS
```

- **Model**: 同上
- **Presenter**: 处理事件，手动更新UI
- **View**: 暴露UI元素引用给Presenter

---

## MVVM 完整实现

### 1. Model（数据层）

```csharp
// Scripts/Models/PlayerModel.cs
namespace Game.Models
{
    /// <summary>
    /// 玩家数据模型（纯C#，不依赖Unity）
    /// </summary>
    public class PlayerModel
    {
        public string Name { get; set; }
        public int Level { get; set; }
        public int CurrentHp { get; set; }
        public int MaxHp { get; set; }
        public int Gold { get; set; }
        
        public float HpPercent => MaxHp > 0 ? (float)CurrentHp / MaxHp : 0f;
        public string HpText => $"{CurrentHp}/{MaxHp}";
    }
}
```

### 2. ViewModel（绑定层）

```csharp
// Scripts/ViewModels/PlayerViewModel.cs
using UnityEngine;
using UnityEngine.UIElements;
using Unity.Properties;
using Game.Models;

namespace Game.ViewModels
{
    /// <summary>
    /// 玩家界面ViewModel
    /// </summary>
    public class PlayerViewModel : MonoBehaviour
    {
        [Header("References")]
        [SerializeField] private UIDocument _uiDocument;
        
        private PlayerModel _model;
        
        // ===== 绑定属性 =====
        private string _playerName;
        [CreateProperty]
        public string PlayerName
        {
            get => _playerName;
            set
            {
                if (_playerName != value)
                {
                    _playerName = value;
                    NotifyPropertyChanged(nameof(PlayerName));
                }
            }
        }
        
        private string _hpText;
        [CreateProperty]
        public string HpText
        {
            get => _hpText;
            set
            {
                if (_hpText != value)
                {
                    _hpText = value;
                    NotifyPropertyChanged(nameof(HpText));
                }
            }
        }
        
        private float _hpPercent;
        [CreateProperty]
        public float HpPercent
        {
            get => _hpPercent;
            set
            {
                if (!Mathf.Approximately(_hpPercent, value))
                {
                    _hpPercent = value;
                    NotifyPropertyChanged(nameof(HpPercent));
                }
            }
        }
        
        private string _goldText;
        [CreateProperty]
        public string GoldText
        {
            get => _goldText;
            set
            {
                if (_goldText != value)
                {
                    _goldText = value;
                    NotifyPropertyChanged(nameof(GoldText));
                }
            }
        }
        
        // ===== 初始化 =====
        private void Awake()
        {
            _model = new PlayerModel();
            InitializeBinding();
            SyncFromModel();
        }
        
        private void InitializeBinding()
        {
            var root = _uiDocument.rootVisualElement;
            root.dataSource = this;
        }
        
        private void SyncFromModel()
        {
            PlayerName = _model.Name;
            HpText = _model.HpText;
            HpPercent = _model.HpPercent;
            GoldText = $"💰 {_model.Gold}";
        }
        
        // ===== 公共方法（供外部调用）=====
        public void UpdateHp(int current, int max)
        {
            _model.CurrentHp = current;
            _model.MaxHp = max;
            SyncFromModel();
        }
        
        public void AddGold(int amount)
        {
            _model.Gold += amount;
            SyncFromModel();
        }
    }
}
```

### 3. UXML（视图层）

```xml
<UXML xmlns="UnityEngine.UIElements">
    <Style src="project://database/Assets/UI/Styles/Player.uss" />
    
    <VisualElement class="player-panel">
        <Label name="player-name" binding-path="PlayerName" />
        <Label name="hp-text" binding-path="HpText" />
        <ProgressBar name="hp-bar" binding-path="HpPercent" />
        <Label name="gold-text" binding-path="GoldText" />
    </VisualElement>
</UXML>
```

### 4. USS（样式层）

```css
/* Player.uss */
.player-panel {
    display: flex;
    flex-direction: column;
    background-color: #1A1A2E;
    border-color: #3A3A5E;
    border-width: 2px;
    border-radius: 12px;
    padding: 16px;
    width: 300px;
}

#player-name {
    font-size: 18px;
    color: #D4AF37;
    margin-bottom: 8px;
}

#hp-bar {
    height: 12px;
    margin: 4px 0;
}

#gold-text {
    font-size: 16px;
    color: #FFD700;
}
```

---

## MVP 完整实现

### 1. Model（同上）

### 2. View Interface

```csharp
// Scripts/Views/IPlayerView.cs
namespace Game.Views
{
    public interface IPlayerView
    {
        string PlayerName { set; }
        string HpText { set; }
        float HpPercent { set; }
        string GoldText { set; }
        
        event System.Action OnAddGoldClicked;
        event System.Action OnLevelUpClicked;
    }
}
```

### 3. View Implementation

```csharp
// Scripts/Views/PlayerView.cs
using UnityEngine;
using UnityEngine.UIElements;
using System;

namespace Game.Views
{
    public class PlayerView : MonoBehaviour, IPlayerView
    {
        [SerializeField] private UIDocument _uiDocument;
        
        private Label _playerNameLabel;
        private Label _hpLabel;
        private ProgressBar _hpBar;
        private Label _goldLabel;
        private Button _addGoldBtn;
        private Button _levelUpBtn;
        
        public event Action OnAddGoldClicked;
        public event Action OnLevelUpClicked;
        
        // IPlayerView implementation
        public string PlayerName { set => _playerNameLabel.text = value; }
        public string HpText { set => _hpLabel.text = value; }
        public float HpPercent { set => _hpBar.value = value; }
        public string GoldText { set => _goldLabel.text = value; }
        
        private void Awake()
        {
            InitializeElements();
            BindEvents();
        }
        
        private void InitializeElements()
        {
            var root = _uiDocument.rootVisualElement;
            _playerNameLabel = root.Q<Label>("player-name");
            _hpLabel = root.Q<Label>("hp-text");
            _hpBar = root.Q<ProgressBar>("hp-bar");
            _goldLabel = root.Q<Label>("gold-text");
            _addGoldBtn = root.Q<Button>("add-gold-btn");
            _levelUpBtn = root.Q<Button>("level-up-btn");
        }
        
        private void BindEvents()
        {
            _addGoldBtn.clicked += () => OnAddGoldClicked?.Invoke();
            _levelUpBtn.clicked += () => OnLevelUpClicked?.Invoke();
        }
    }
}
```

### 4. Presenter

```csharp
// Scripts/Presenters/PlayerPresenter.cs
using Game.Models;
using Game.Views;

namespace Game.Presenters
{
    public class PlayerPresenter
    {
        private readonly PlayerModel _model;
        private readonly IPlayerView _view;
        
        public PlayerPresenter(IPlayerView view, PlayerModel model)
        {
            _view = view;
            _model = model;
            
            // 订阅View事件
            _view.OnAddGoldClicked += HandleAddGold;
            _view.OnLevelUpClicked += HandleLevelUp;
            
            // 初始化显示
            UpdateView();
        }
        
        private void HandleAddGold()
        {
            _model.Gold += 100;
            UpdateView();
        }
        
        private void HandleLevelUp()
        {
            _model.Level++;
            _model.MaxHp += 10;
            _model.CurrentHp = _model.MaxHp;
            UpdateView();
        }
        
        private void UpdateView()
        {
            _view.PlayerName = $"{_model.Name} (Lv.{_model.Level})";
            _view.HpText = _model.HpText;
            _view.HpPercent = _model.HpPercent;
            _view.GoldText = $"💰 {_model.Gold}";
        }
    }
}
```

---

## 模式选择建议

| 场景 | 推荐模式 | 理由 |
|------|---------|------|
| 数据展示型界面 | MVVM | 数据绑定自动同步 |
| 复杂交互界面 | MVP | Presenter集中处理逻辑 |
| 表单/设置界面 | MVVM | 双向绑定简化输入 |
| 游戏HUD | MVP | 性能更优，无绑定开销 |
| 编辑器工具 | MVVM | Unity编辑器原生支持 |

---

## 最佳实践

### 1. 分离关注点
- Model: 只存数据，不含UI逻辑
- ViewModel: 格式化数据，不直接操作UI元素
- View: 只负责显示，不含业务逻辑

### 2. 命名约定
```
Model: PlayerModel.cs
ViewModel: PlayerViewModel.cs
View: Player.uxml + Player.uss
Presenter: PlayerPresenter.cs
```

### 3. 文件夹结构
```
Assets/
└── Scripts/
    ├── Models/
    ├── Views/
    │   └── IPlayerView.cs
    ├── ViewModels/
    │   └── PlayerViewModel.cs
    ├── Presenters/
    │   └── PlayerPresenter.cs
    └── UI/
        ├── Player/
        │   ├── Player.uxml
        │   └── Player.uss
        └── Common/
            └── Common.uss
```
