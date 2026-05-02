# USS 能力边界与降级策略

Unity UI Toolkit 的 USS 是 CSS 的子集。直接使用 CSS/React 知识会导致不兼容。
本文档明确 USS 能力边界，以及从 CSS 美观效果到 USS 的降级策略。

## 1. 布局系统

| CSS 特性 | USS 支持 | 降级策略 |
|----------|---------|---------|
| Flexbox | ✅ 完整支持 | 直接使用 |
| CSS Grid | ❌ 不支持 | 用 Flex 嵌套模拟：row 容器 > column 子容器 |
| `position: absolute` | ✅ 支持 | 直接使用 |
| `position: sticky` | ❌ 不支持 | 用 ScrollView 替代 |
| `gap` (flex) | ✅ 2023.2+ | 直接使用 |
| `float` | ❌ 不支持 | 用 Flex 替代 |

### Grid → Flex 降级模式

```css
/* CSS Grid */
.grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }

/* USS Flex 等效 */
.grid { flex-direction: row; flex-wrap: wrap; }
.grid > * { width: calc(25% - 6px); margin: 4px; }
```

## 2. 颜色与背景

| CSS 特性 | USS 支持 | 降级策略 |
|----------|---------|---------|
| 纯色 `background-color` | ✅ | 直接使用 |
| 线性渐变 `linear-gradient` | ❌ | 用 9-slice 背景图 或 单色 |
| 径向渐变 `radial-gradient` | ❌ | 同上 |
| `rgba()` 半透明 | ✅ | 直接使用 |
| `hsla()` | ❌ | 转为 rgba |
| `currentColor` | ❌ | 手动指定颜色值 |
| 多背景层 | ❌ | 单层背景 + overlay 元素 |
| `background-image` | ✅ | 直接使用（需资源引用） |
| `background-blend-mode` | ❌ | 不支持 |

### 渐变降级

```css
/* CSS 渐变按钮 */
.btn { background: linear-gradient(135deg, #6366F1, #8B5CF6); }

/* USS 降级：单色 + 微妙边框模拟渐变感 */
.btn {
  background-color: #7C3AED;  /* 取渐变中间色 */
  border-top-color: #8B5CF6;
  border-bottom-color: #6366F1;
  border-top-width: 1px;
  border-bottom-width: 1px;
}
```

## 3. 毛玻璃 / 磨砂效果

| CSS 特性 | USS 支持 | 降级策略 |
|----------|---------|---------|
| `backdrop-filter: blur()` | ❌ | 半透明背景色 |
| `backdrop-filter: saturate()` | ❌ | 同上 |

### 降级模式

```css
/* CSS 毛玻璃 */
.glass { background: rgba(255,255,255,0.1); backdrop-filter: blur(12px); }

/* USS 降级：纯半透明 */
.glass {
  background-color: rgba(30, 30, 50, 0.7);  /* 深色半透明 */
  border-color: rgba(139, 92, 246, 0.3);     /* 微光边框模拟光晕 */
  border-width: 1px;
}
```

## 4. 阴影

| CSS 特性 | USS 支持 | 降级策略 |
|----------|---------|---------|
| `box-shadow` | ⚠️ 有限 | Unity 2023.1+ 支持，但语法不同 |
| `text-shadow` | ❌ | 不支持，用 Label outline 模拟 |
| `drop-shadow()` filter | ❌ | 不支持 |

### USS 阴影（2023.1+）

```css
/* USS box-shadow 语法 */
.card {
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.25);  /* offset-x offset-y blur color */
}
/* 注意：USS 只支持单层阴影，不支持 inset */
```

## 5. 边框与圆角

| CSS 特性 | USS 支持 | 降级策略 |
|----------|---------|---------|
| `border-radius` | ✅ | 直接使用 |
| `border-style` | ⚠️ 有限 | 仅 solid，无 dashed/dotted |
| `border-image` | ❌ | 用 9-slice sprite |
| `outline` | ❌ | 用额外 border 模拟 |

## 6. 动画与过渡

| CSS 特性 | USS 支持 | 降级策略 |
|----------|---------|---------|
| `transition` | ✅ | 直接使用 |
| `@keyframes` | ❌ | 用 C# 脚本 + USS transition |
| `animation` | ❌ | 同上 |
| `transform` | ⚠️ 有限 | 仅 translate/rotate/scale，需 USS transition 配合 |

### 动画降级

```css
/* CSS 关键帧动画 */
@keyframes pulse { 0% { transform: scale(1); } 50% { transform: scale(1.05); } 100% { transform: scale(1); } }
.btn:hover { animation: pulse 0.3s; }

/* USS 降级：transition + :hover */
.btn {
  transition-duration: 200ms;
  transition-property: scale;  /* Unity 2023.2+ */
}
.btn:hover {
  scale: 1.05;
}
```

## 7. 伪类 / 伪元素

| CSS 特性 | USS 支持 |
|----------|---------|
| `:hover` | ✅ |
| `:active` | ✅ |
| `:focus` | ✅ |
| `:disabled` | ✅ |
| `:checked` | ✅ (Toggle) |
| `:nth-child()` | ❌ |
| `::before` / `::after` | ❌ |
| `::placeholder` | ❌ (用 placeholder-text 属性) |

## 8. 排版

| CSS 特性 | USS 支持 | 降级策略 |
|----------|---------|---------|
| `font-family` | ✅ | 需 Unity Font Asset |
| `font-size` | ✅ | 直接使用 |
| `font-weight` | ✅ | bold / normal |
| `line-height` | ✅ | 直接使用 |
| `letter-spacing` | ✅ | 直接使用 |
| `text-overflow: ellipsis` | ✅ | 直接使用 |
| `-webkit-line-clamp` | ❌ | 用固定高度 + overflow: hidden |
| `word-break` | ⚠️ | 有限支持 |

## 9. 设计 Token 中的降级标记

在 design_tokens.py 中，我们用以下约定标记降级：

```json
{
  "colors": {
    "surface": "rgba(30,30,50,0.7)",     // 毛玻璃降级 → 半透明
    "border": "rgba(139,92,246,0.3)"      // 光晕降级 → 微光边框
  },
  "shadow": {
    "md": "0 2px 4px rgba(0,0,0,0.12)"   // 简化阴影（USS 2023.1+）
  }
}
```

## 10. 完整降级对照表

| 设计效果 | CSS 实现 | USS 实现 | 视觉差距 |
|---------|---------|---------|---------|
| 毛玻璃面板 | backdrop-filter: blur | rgba 半透明 + 微光边框 | 中等 |
| 渐变按钮 | linear-gradient | 单色 + 异色上下边框 | 较大 |
| 发光文字 | text-shadow | 无（仅 C# outline） | 大 |
| 浮动卡片 | box-shadow 多层 | 单层 box-shadow | 小 |
| 网格布局 | CSS Grid | Flex wrap | 无 |
| 霓虹边框 | border + box-shadow | border + 单层 shadow | 小 |
| 平滑动画 | @keyframes | transition + :hover | 中等 |
| 响应式 | @media | C# 脚本动态调整 | — |

## 结论

USS 在以下方面表现良好：
- ✅ Flexbox 布局
- ✅ 颜色（含半透明）
- ✅ 圆角
- ✅ 基础过渡动画
- ✅ 伪类状态

USS 主要短板：
- ❌ 无渐变背景
- ❌ 无毛玻璃效果
- ❌ 无关键帧动画
- ❌ 无 CSS Grid
- ❌ 无多层阴影

**关键原则：在设计阶段就考虑 USS 能力边界，不要先做 CSS 美图再降级。**
在 Token 层面预设好降级方案（如毛玻璃 → 半透明 + 微光边框），生成时直接使用。
