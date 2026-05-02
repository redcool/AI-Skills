# Unity UI Toolkit 组件参考

## 容器类组件

### VisualElement
通用容器，用于布局和分组。

```xml
<VisualElement name="container" class="panel">
    <!-- 子元素 -->
</VisualElement>
```

**常用属性：**
- `name`: 元素名称（用于C#查询）
- `class`: CSS类名（多个用空格分隔）
- `style`: 内联样式
- `picking-mode`: 点击检测模式（Position/Ignore）

### ScrollView
滚动视图容器。

```xml
ScrollView name="scroll-list">
    <VisualElement name="content" />
</ScrollView>
```

**属性：**
- `mode`: Vertical/Horizontal/VerticalAndHorizontal
- `show-vertical-scroller`: 显示垂直滚动条

### ListView
列表视图（数据驱动）。

```xml
<ListView name="item-list" make-item="." bind-item="." />
```

**属性：**
- `make-item`: 创建Item模板
- `bind-item`: 绑定数据回调
- `selection-type`: Single/Multiple/None

---

## 输入类组件

### TextField
文本输入框。

```xml
<TextField name="username" label="用户名" value="" />
```

**属性：**
- `label`: 标签文本
- `value`: 默认值
- `max-length`: 最大长度
- `is-password`: 密码模式
- `keyboard-type`: 键盘类型

### IntegerField / FloatField
数字输入。

```xml
<IntegerField name="quantity" label="数量" value="1" />
<FloatField name="price" label="价格" value="0.0" />
```

### Slider
滑块控件。

```xml
<Slider name="volume" label="音量" low-value="0" high-value="100" value="50" />
```

**属性：**
- `low-value`: 最小值
- `high-value`: 最大值
- `direction`: Horizontal/Vertical

### Toggle
开关控件。

```xml
<Toggle name="sound-toggle" label="音效" value="true" />
```

### DropdownField
下拉选择框。

```xml
<DropdownField name="quality" label="画质" choices="Low,Medium,High" index="1" />
```

---

## 按钮类组件

### Button
标准按钮。

```xml
<Button name="login-btn" text="登录" />
```

**属性：**
- `text`: 按钮文本

---

## 显示类组件

### Label
文本标签。

```xml
<Label name="title" text="标题" />
```

### Image
图片显示。

```xml
<Image name="icon" sprite="Assets/Icons/icon.png" />
```

**属性：**
- `sprite`: Sprite资源
- `tint-color": 着色

### ProgressBar
进度条。

```xml
<ProgressBar name="health-bar" title="HP" value="50" low-value="0" high-value="100" />
```

---

## 布局属性（USS）

### Flexbox布局

```css
.container {
    display: flex;
    flex-direction: column;  /* row / column */
    flex-wrap: wrap;
    justify-content: center; /* flex-start/center/flex-end/space-between/space-around */
    align-items: center;
    align-content: flex-start;
}
```

### 尺寸

```css
.element {
    width: 100px;
    height: 50px;
    min-width: 50px;
    max-width: 200px;
    margin: 10px;
    padding: 8px;
}
```

### 定位

```css
.element {
    position: absolute;  /* relative / absolute */
    left: 10px;
    top: 20px;
    right: auto;
    bottom: auto;
}
```

---

## 数据绑定（MVVM）

### 绑定属性
在UXML中设置绑定路径：

```xml
<TextField name="username" binding-path="Username" />
<Label name="hp-label" binding-path="HpText" />
<ProgressBar name="hp-bar" binding-path="HpPercent" />
```

### ViewModel定义

```csharp
public class LoginViewModel : MonoBehaviour
{
    [CreateProperty] public string Username { get; set; }
    [CreateProperty] public string Password { get; set; }
    
    void Start()
    {
        var root = GetComponent<UIDocument>().rootVisualElement;
        root.dataSource = this;
    }
}
```

---

## 事件系统

### 注册事件

```csharp
private void BindEvents()
{
    _loginButton.clicked += OnLoginClicked;
    _usernameField.RegisterValueChangedCallback(OnUsernameChanged);
    _root.RegisterCallback<ClickEvent>(OnRootClick);
}

private void OnLoginClicked()
{
    Debug.Log("Login button clicked");
}
```

### 常用事件

| 事件 | 说明 |
|------|------|
| ClickEvent | 点击 |
| MouseDownEvent / MouseUpEvent | 鼠标按下/释放 |
| MouseEnterEvent / MouseLeaveEvent | 鼠标进入/离开 |
| KeyDownEvent / KeyUpEvent | 键盘按下/释放 |
| ChangeEvent<T> | 值变化 |
| FocusEvent / BlurEvent | 获得/失去焦点 |
