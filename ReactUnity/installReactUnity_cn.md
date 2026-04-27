# ReactUnity 安装与初始化指南

本文档记录 ReactUnity 的完整安装流程和项目初始化步骤。

---

## 一、Unity 端安装

### 方式一：OpenUPM（推荐）

```bash
npx openupm-cli add com.reactunity.core com.reactunity.quickjs
```

### 方式二：Package Manager

在 Unity 中：
1. 打开 `Window > Package Manager`
2. 点击 `+` 按钮
3. 选择 `Add package from git URL`
4. 输入：`https://github.com/ReactUnity/core.git#latest`

### 安装验证

检查 `Packages/manifest.json` 中是否包含：

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

## 二、创建 React 项目

### 自动创建（推荐）

```bash
npx @reactunity/create@latest
```

> 注意：如果遇到 `spawn EINVAL` 错误，这是 Windows 平台的已知问题，项目文件已成功创建。

### 项目结构

```
[Unity_Project_Root]
├── Assets/
├── react/                    ← React 项目目录
│   ├── src/
│   │   ├── index.tsx         ← 入口文件
│   │   └── index.scss        ← 样式文件
│   ├── package.json
│   ├── tsconfig.json
│   └── ...
└── Packages/
```

---

## 三、安装依赖

```bash
cd react
npm install
```

或使用 yarn：

```bash
cd react
yarn
```

### 依赖说明

| 包 | 版本 | 说明 |
|---|---|---|
| `@reactunity/renderer` | ^0.18.0 | ReactUnity 渲染核心 |
| `react` | ^18.2.0 | React 库 |
| `@reactunity/scripts` | ^0.18.3 | 构建脚本 |
| `typescript` | ^5.4.4 | TypeScript 支持 |

---

## 四、开发命令

在 `react/` 目录下运行：

```bash
npm start         # 启动开发服务器（HMR 热重载）
npm run build     # 构建生产版本到 Assets/Resources/react/index.js
```

---

## 五、Unity 端配置

### 快速开始

1. 在 Unity 菜单中选择 `React > Quick Start`
2. 自动创建 Canvas 并添加 `ReactRendererUGUI` 组件

### 手动配置

1. 创建 Canvas（`GameObject > UI > Canvas`）
2. 添加 `ReactRendererUGUI` 组件
3. 运行 `npm start` 启动开发服务器
4. 点击 Unity Play 按钮预览

---

## 六、项目入口文件示例

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

## 七、常见问题

### Q: npm start 无法连接 Unity？

A: 确保 Unity 处于 Play 模式，且已添加 `ReactRendererUGUI` 组件。

### Q: 样式不生效？

A: 检查：
1. 文件后缀是否为 `.module.scss`
2. 导入方式是否为 `import styles from './xxx.module.scss'`
3. 引用方式是否为 `className={styles.类名}`

### Q: 需要重新创建 React 项目？

A: 可以删除 `react/` 目录后重新执行创建命令，Unity 端的包不受影响。

---

## 参考资料

- 官方文档：https://github.com/ReactUnity/core
- 示例工程：https://github.com/ReactUnity/full-sample
- 快速开始向导：https://github.com/ReactUnity/create