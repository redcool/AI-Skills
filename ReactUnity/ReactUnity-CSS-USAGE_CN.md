# ReactUnity 样式使用指南

本文档记录在 ReactUnity 项目中样式的正确使用方式。

## 目录

- [方式一：CSS Modules（推荐）](#方式一css-modules推荐)
- [方式二：内联样式](#方式二内联样式)
- [方式三：普通 SCSS/CSS](#方式三普通-scsscss)

---

## 方式一：CSS Modules（推荐）

这是 ReactUnity Sample 工程中使用的方式，也是**最推荐**的方式。

### 1. 文件命名

使用 `.module.scss` 后缀：

```
src/
├── index.tsx
└── index.module.scss  ✅ 正确
```

### 2. SCSS 编写

使用 **BEM 命名格式**（类名前缀 + 下划线）：

```scss
// index.module.scss

.appContainer {
  flex-direction: row;
  width: 100%;
  height: 100%;
  background-color: #1a1a2e;
}

.weaponList {
  width: 35%;
  height: 100%;
  flex-direction: column;
}

.weaponCard {
  background-color: #1f4068;
  border-radius: 8px;
  padding: 15px;
}

.weaponCard:hover {
  background-color: #2a5a8a;
}

.selected {
  border-color: #e94560;
}
```

### 3. TSX 导入和使用

```tsx
// index.tsx
import { render } from '@reactunity/renderer';
import styles from './index.module.scss';

function App() {
  return (
    <view className={styles.appContainer}>
      <view className={styles.weaponList}>
        <text className={styles.title}>武器库</text>
      </view>
    </view>
  );
}

render(<App />);
```

### 4. 组合类名

需要组合多个类名时使用模板字符串：

```tsx
<button 
  className={`${styles.weaponCard} ${isSelected ? styles.selected : ''}`}
>
```

### 关键点总结

| 要点 | 说明 |
|------|------|
| 文件后缀 | `.module.scss` |
| SCSS 类名 | `.weaponCard` 格式（不是 kebab-case） |
| 导入方式 | `import styles from './xxx.module.scss'` |
| 类名引用 | `className={styles.weaponCard}` |

---

## 方式二：内联样式

使用 `style` 属性传入对象：

```tsx
function App() {
  return (
    <view style={{
      flexDirection: 'row',
      width: '100%',
      height: '100%',
      backgroundColor: '#1a1a2e'
    }}>
      <text style={{
        fontSize: '28px',
        color: '#e94560'
      }}>
        武器库
      </text>
    </view>
  );
}
```

### ReactUnity 支持的样式属性

```
布局
- flex-direction: row | column
- align-items: center | stretch | flex-start | flex-end
- justify-content: center | flex-start | flex-end | space-between
- width: number | string
- height: number | string

颜色
- background-color: #hex | rgb() | rgba()
- color: #hex

边框
- border-width: number
- border-color: #hex
- border-radius: number

文本
- font-size: number
- font-weight: bold | normal
- text-align: center | left | right

其他
- padding: number
- margin: number
- opacity: number
```

---

## 方式三：普通 SCSS/CSS

### 1. 文件命名

使用普通 `.scss` 或 `.css` 后缀：

```
src/
├── index.tsx
└── index.scss  ✅ 可以（但不推荐）
```

### 2. SCSS 编写

```scss
// index.scss

app-container {
  flex-direction: row;
  width: 100%;
  height: 100%;
  background-color: #1a1a2e;
}

weapon-list {
  width: 35%;
  flex-direction: column;
}
```

### 3. TSX 导入和使用

```tsx
import './index.scss';

function App() {
  return (
    <view className="app-container">
      <view className="weapon-list">
        武器库
      </view>
    </view>
  );
}
```

### ⚠️ 注意

这种方式**不推荐**使用，原因：
- 类名可能会被哈希化（取决于 webpack 配置）
- 与其他组件的类名可能冲突
- 无法享受 CSS Modules 的局部作用域

---

## 常见问题

### Q: `className` 不生效？

**A:** 检查以下几点：

1. 是否使用 `.module.scss` 后缀？
2. 是否用 `import styles from './xxx.module.scss'` 导入？
3. 是否用 `className={styles.类名}` 引用（不是字符串）？

### Q: SCSS 编译报错？

**A:** 确保：
- webpack 配置了 `sass-loader`
- 安装了 `sass` 包：`npm i -D sass`

### Q: 样式被覆盖？

**A:** 使用 CSS Modules 的局部作用域可以避免这个问题。

---

## 完整示例

### 项目结构

```
src/
├── index.tsx
├── index.module.scss
└── components/
    ├── WeaponCard.tsx
    └── WeaponCard.module.scss
```

### index.module.scss

```scss
.appContainer {
  flex-direction: row;
  width: 100%;
  height: 100%;
  background-color: #1a1a2e;
}

.weaponList {
  width: 35%;
  height: 100%;
  flex-direction: column;
  background-color: #16213e;
}

.listTitle {
  font-size: 28px;
  font-weight: bold;
  color: #e94560;
  padding: 20px;
  text-align: center;
}

.weaponScroll {
  flex: 1;
  flex-direction: column;
  padding: 10px;
}
```

### index.tsx

```tsx
import { render } from '@reactunity/renderer';
import { useState } from 'react';
import styles from './index.module.scss';

const weapons = [...];

function WeaponCard({ weapon, isSelected, onClick }) {
  return (
    <button 
      className={`${styles.weaponCard} ${isSelected ? styles.selected : ''}`}
      onClick={onClick}
    >
      <view className={styles.weaponCardHeader}>
        <text className={styles.weaponIcon}>{weapon.icon}</text>
        <view className={styles.weaponInfo}>
          <text className={styles.weaponName}>{weapon.name}</text>
          <text className={styles.weaponType}>{weapon.type}</text>
        </view>
      </view>
    </button>
  );
}

function App() {
  const [selected, setSelected] = useState(weapons[0]);

  return (
    <view className={styles.appContainer}>
      <view className={styles.weaponList}>
        <text className={styles.listTitle}>武器库</text>
        <scroll className={styles.weaponScroll}>
          {weapons.map(weapon => (
            <WeaponCard
              key={weapon.id}
              weapon={weapon}
              isSelected={selected.id === weapon.id}
              onClick={() => setSelected(weapon)}
            />
          ))}
        </scroll>
      </view>
    </view>
  );
}

render(<App />);
```

---

## 参考

- 官方文档：https://github.com/ReactUnity/core
- 示例工程：https://github.com/ReactUnity/full-sample