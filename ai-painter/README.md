# ai-painter — ComfyUI 文生图

通过文字提示词，调用本地 ComfyUI + SDXL 生成高质量图片，支持中文关键词自动翻译。

## 环境依赖

| 依赖 | 说明 |
|------|------|
| **ComfyUI** | `H:\AI\ComfyUI_windows_portable\run_nvidia_gpu.bat` |
| **SDXL 模型** | `ComfyUI\models\checkpoints\sd_xl_base_1.0.safetensors` |
| **Python** | 3.x（已装在系统）|

## 快速开始

```bash
# 启动 ComfyUI（如未运行）
Start-Process "H:\AI\ComfyUI_windows_portable\run_nvidia_gpu.bat"

# 生成图片
python H:\AI\AI_SKILLS\ai-painter\ai-painter.py --zh "蒸汽朋克飞艇穿梭云层" --out D:\tmp\airship

# 直接英文
python H:\AI\AI_SKILLS\ai-painter\ai-painter.py --prompt "cyberpunk city at night" --preset hq --out D:\tmp\cyber
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `--prompt` | 正向提示词 |
| `--zh` | 将 prompt 作为中文处理，自动翻译关键词 |
| `--preset` | 质量预设：`draft/std/hq/photo/fast/anime/realistic` |
| `--size` | 比例：`1:1 / 4:3 / 3:4 / 16:9 / 9:16 / 21:9` |
| `--seed` | 随机种子（固定可复现） |
| `--out` | 输出目录 |

## 质量预设

| 预设 | 步数 | CFG | 速度 |
|------|------|-----|------|
| draft（草稿） | 10 | 6.0 | 最快 ~5s |
| std（标准） | 20 | 7.0 | 快 ~15s |
| hq（精细） | 30 | 7.5 | 中 ~25s |
| photo（照片） | 40 | 8.0 | 慢 ~40s |
| fast（极速） | 8 | 5.0 | 最快 LCM |
| anime（动漫） | 25 | 7.0 | 快 |
| realistic（写实） | 35 | 7.0 | 中 |

中文别名：`标准/精细/草稿/照片/极速/动漫/写实`

## 输出文件

```
out/
  txt2img_XXXX.png   ← 生成图片
  meta.json          ← 完整参数（复现用）
  prompt.txt         ← 提示词文本
```

## 复现图片

从 `meta.json` 复制参数：

```bash
python H:\AI\AI_SKILLS\ai-painter\ai-painter.py --prompt "..." --seed 12345 --size 16:9 --preset hq --out D:\tmp\repro
```
