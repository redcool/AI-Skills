# AI Skills 技能库

OpenCode / Claude AI 智能体个人技能库。

## 📦 技能索引

| 技能 | 说明 | 快速开始 |
|------|------|----------|
| **[ai-painter](./ai-painter)** | ComfyUI + SDXL 文生图，支持中文关键词自动翻译，7种质量预设，6种比例。 | `python ai-painter.py --zh "蒸汽朋克飞艇" --out D:\tmp` |
| **[pixel-forge](./pixel-forge)** | ComfyUI 游戏精灵表生成，透明 PNG + 动画 GIF，多种布局（4×4/2×2/2×3）。 | `python pixel-forge.py --target player --mode player_sheet --zh "catgirl mage"` |
| **[opencode-unity-uixml](./opencode-unity-uixml)** | YAML 规格 → Unity UI Toolkit（UXML + USS + C#），MVP 模式，4种内置样式。 | `python unity_uixml_generator.py --spec yaml/login.yaml --out src/` |
| **[opencode-uiux-uxml](./opencode-uiux-uxml)** | 设计 Token 驱动的 Unity UI Toolkit 生成器，10种设计预设（毛玻璃/极光/赛博/科幻）。颜色/字体/间距/圆角/阴影独立配置。 | `python uxml_generator.py --preset dark_glassmorphism --name LoginView` |
| **[ReactUnity](./ReactUnity)** | ReactUnity 文档 — Unity WebGL 下 React 开发安装配置与 CSS 使用指南。 | 查看 [ReactUnity](./ReactUnity) 目录 |

## 目录结构

```
AI_SKILLS/
├── ai-painter/              ComfyUI 文生图
├── pixel-forge/             ComfyUI 精灵表生成
├── opencode-unity-uixml/     Unity UI Toolkit 快速原型（YAML 驱动）
├── opencode-uiux-uxml/       Unity UI Toolkit 设计系统（Token 驱动）
├── ReactUnity/              ReactUnity 文档
├── README.md                英文索引
└── README_cn.md             本文件（中文）
```

## 环境依赖

| 依赖 | 说明 |
|------|------|
| **ComfyUI** | `H:\AI\ComfyUI_windows_portable\run_nvidia_gpu.bat` |
| **SDXL 模型** | `ComfyUI\models\checkpoints\sd_xl_base_1.0.safetensors` |
| **Python** | 3.x（含 requests、Pillow）|

## 相关链接

- GitHub 仓库: [redcool/ReactUnity-ai](https://github.com/redcool/ReactUnity-ai)
- ReactUnity 核心: [redcool/ReactUnity](https://github.com/redcool/ReactUnity)