# ReactUnity Installation & Setup Guide

This document outlines the complete installation process and project initialization steps for ReactUnity.

---

## 1. Unity Side Installation

### Option 1: OpenUPM (Recommended)

```bash
npx openupm-cli add com.reactunity.core com.reactunity.quickjs
```

### Option 2: Package Manager

In Unity:
1. Open `Window > Package Manager`
2. Click the `+` button
3. Select `Add package from git URL`
4. Enter: `https://github.com/ReactUnity/core.git#latest`

### Verification

Check `Packages/manifest.json` for:

```json
{
  "dependencies": {
    "com.reactunity.core": "0.21.2",
    "com.reactunity.quickjs": "0.19.0"
  },
  "scopedRegistries": [
    {
      "name": "package.openupm.com",
      "url": "https://package.openupm.com",
      "scopes": [
        "com.reactunity.core",
        "com.reactunity.quickjs"
      ]
    }
  ]
}
```

---

## 2. Create React Project

### Auto Creation (Recommended)

```bash
npx @reactunity/create@latest
```

> Note: If you encounter `spawn EINVAL` error, this is a known Windows issue - the project files are successfully created.

### Project Structure

```
[Unity_Project_Root]
├── Assets/
├── react/                    ← React project directory
│   ├── src/
│   │   ├── index.tsx         ← Entry file
│   │   └── index.scss        ← Styles
│   ├── package.json
│   ├── tsconfig.json
│   └── ...
└── Packages/
```

---

## 3. Install Dependencies

```bash
cd react
npm install
```

Or using yarn:

```bash
cd react
yarn
```

### Dependencies

| Package | Version | Description |
|---------|---------|-----------|
| `@reactunity/renderer` | ^0.18.0 | ReactUnity rendering core |
| `react` | ^18.2.0 | React library |
| `@reactunity/scripts` | ^0.18.3 | Build scripts |
| `typescript` | ^5.4.4 | TypeScript support |

---

## 4. Development Commands

In the `react/` directory:

```bash
npm start         # Start dev server (HMR hot reload)
npm run build     # Build production to Assets/Resources/react/index.js
```

---

## 5. Unity Side Configuration

### Quick Start

1. Select `React > Quick Start` from Unity menu
2. Creates Canvas automatically and adds `ReactRendererUGUI` component

### Manual Configuration

1. Create Canvas (`GameObject > UI > Canvas`)
2. Add `ReactRendererUGUI` component
3. Run `npm start` to start dev server
4. Click Unity Play button to preview

---

## 6. Project Entry File Examples

### src/index.tsx

```tsx
import { render } from '@reactunity/renderer';
import styles from './index.module.scss';

function App() {
  return (
    <view className={styles.appContainer}>
      <text>Hello ReactUnity!</text>
    </view>
  );
}

render(<App />);
```

### src/index.module.scss

```scss
.appContainer {
  flex-direction: column;
  width: 100%;
  height: 100%;
  background-color: #1a1a2e;
  align-items: center;
  justify-content: center;
}
```

---

## 7. FAQ

### Q: npm start can't connect to Unity?

A: Make sure Unity is in Play mode and the `ReactRendererUGUI` component is added.

### Q: Styles not working?

A: Check:
1. File suffix is `.module.scss`
2. Import is `import styles from './xxx.module.scss'`
3. Reference is `className={styles.className}`

### Q: Need to recreate React project?

A: Delete the `react/` directory and run the creation command again. Unity-side packages won't be affected.

---

## References

- Official docs: https://github.com/ReactUnity/core
- Sample project: https://github.com/ReactUnity/full-sample
- Quick start wizard: https://github.com/ReactUnity/create