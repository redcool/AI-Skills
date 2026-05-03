# AI Skills

Personal skill library for OpenCode/Claude AI agents.

## 📦 Skills Index

| Skill | Description | Quick Start |
|-------|-------------|-------------|
| **[ai-painter](./ai-painter)** | Text-to-image via ComfyUI + SDXL. Chinese prompt auto-translation. 7 quality presets, 6 aspect ratios. | `python ai-painter.py --zh "蒸汽朋克飞艇" --out D:\tmp` |
| **[pixel-forge](./pixel-forge)** | Game sprite sheet generation via ComfyUI. Transparent PNG + animated GIF. Multiple layouts (4×4/2×2/2×3). | `python pixel-forge.py --target player --mode player_sheet --zh "catgirl mage"` |
| **[opencode-char-3view](./opencode-char-3view)** | Character three-view reference sheet generator (front/side/back). 7 style presets. Chinese support. | `python char-3view.py --desc "汉朝战士" --style realistic --zh` |
| **[opencode-unity-uixml](./opencode-unity-uixml)** | YAML spec → Unity UI Toolkit (UXML + USS + C#). MVP pattern. 4 style presets. | `python unity_uixml_generator.py --spec yaml/login.yaml --out src/` |
| **[opencode-uiux-uxml](./opencode-uiux-uxml)** | Design-token-driven Unity UI Toolkit generator. 10 design presets (glassmorphism/aurora/cyber/scifi). Token system for colors, typography, spacing. | `python uxml_generator.py --preset dark_glassmorphism --name LoginView` |
| **[ReactUnity](./ReactUnity)** | ReactUnity docs — install guide & CSS usage for Unity WebGL. | See docs in [ReactUnity](./ReactUnity) |

## Directory Structure

```
AI_SKILLS/
├── ai-painter/           ComfyUI text-to-image
├── pixel-forge/          ComfyUI sprite sheet generator
├── opencode-char-3view/  Character three-view generator
├── opencode-unity-uixml/ Unity UI Toolkit rapid prototype (YAML→UXML)
├── opencode-uiux-uxml/   Unity UI Toolkit design system (Token-driven)
├── ReactUnity/           ReactUnity documentation
├── README.md             This file (English)
└── README_cn.md         中文索引
```

## Environment

- **ComfyUI**: `H:\AI\ComfyUI_windows_portable\run_nvidia_gpu.bat`
- **Model**: SDXL `sd_xl_base_1.0.safetensors`
- **Python**: 3.x with requests, PIL (Pillow)

## Links

- Repository: [redcool/ReactUnity-ai](https://github.com/redcool/ReactUnity-ai)
- ReactUnity Core: [redcool/ReactUnity](https://github.com/redcool/ReactUnity)