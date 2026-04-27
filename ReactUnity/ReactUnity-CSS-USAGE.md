# ReactUnity CSS Usage Guide

This document covers the correct way to use styles in ReactUnity projects.

## Table of Contents

- [Method 1: CSS Modules (Recommended)](#method-1-css-modules-recommended)
- [Method 2: Inline Styles](#method-2-inline-styles)
- [Method 3: Regular SCSS/CSS](#method-3-regular-scsscss)

---

## Method 1: CSS Modules (Recommended)

This is the approach used in the ReactUnity Sample project, and the **most recommended** method.

### 1. File Naming

Use `.module.scss` suffix:

```
src/
├── index.tsx
└── index.module.scss  ✅ Correct
```

### 2. SCSS Writing

Use **BEM naming format** (class name prefix + underscore):

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

### 3. TSX Import and Usage

```tsx
// index.tsx
import { render } from '@reactunity/renderer';
import styles from './index.module.scss';

function App() {
  return (
    <view className={styles.appContainer}>
      <view className={styles.weaponList}>
        <text className={styles.title}>Weapon Arsenal</text>
      </view>
    </view>
  );
}

render(<App />);
```

### 4. Combining Class Names

Use template strings when combining multiple class names:

```tsx
<button
  className={`${styles.weaponCard} ${isSelected ? styles.selected : ''}`}
>
```

### Key Points Summary

| Point | Description |
|-------|-----------|
| File suffix | `.module.scss` |
| SCSS class name | `.weaponCard` format (not kebab-case) |
| Import method | `import styles from './xxx.module.scss'` |
| Class reference | `className={styles.weaponCard}` |

---

## Method 2: Inline Styles

Use `style` attribute with an object:

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
        Weapon Arsenal
      </text>
    </view>
  );
}
```

### Supported Style Properties

```
Layout
- flex-direction: row | column
- align-items: center | stretch | flex-start | flex-end
- justify-content: center | flex-start | flex-end | space-between
- width: number | string
- height: number | string

Colors
- background-color: #hex | rgb() | rgba()
- color: #hex

Borders
- border-width: number
- border-color: #hex
- border-radius: number

Text
- font-size: number
- font-weight: bold | normal
- text-align: center | left | right

Other
- padding: number
- margin: number
- opacity: number
```

---

## Method 3: Regular SCSS/CSS

### 1. File Naming

Use regular `.scss` or `.css` suffix:

```
src/
├── index.tsx
└── index.scss  ✅ Works (but not recommended)
```

### 2. SCSS Writing

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

### 3. TSX Import and Usage

```tsx
import './index.scss';

function App() {
  return (
    <view className="app-container">
      <view className="weapon-list">
        Weapon Arsenal
      </view>
    </view>
  );
}
```

### ⚠️ Note

This method is **not recommended** because:
- Class names may be hashed (depending on webpack config)
- May conflict with class names from other components
- Can't benefit from CSS Modules' local scope

---

## FAQ

### Q: `className` not working?

**A:** Check:
1. Using `.module.scss` suffix?
2. Importing with `import styles from './xxx.module.scss'`?
3. Referencing with `className={styles.className}` (not a string)?

### Q: SCSS compilation error?

**A:** Make sure:
- webpack has `sass-loader` configured
- `sass` package installed: `npm i -D sass`

### Q: Styles being overridden?

**A:** CSS Modules' local scope avoids this issue.

---

## Complete Example

### Project Structure

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
        <text className={styles.listTitle}>Weapon Arsenal</text>
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

## References

- Official docs: https://github.com/ReactUnity/core
- Sample project: https://github.com/ReactUnity/full-sample