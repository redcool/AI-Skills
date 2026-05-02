# ai-painter — ComfyUI Text-to-Image Skill

## When to Use

Generate images, illustrations, character art, landscapes, concept art from text prompts.

**Trigger keywords**: 绘图/生成图片/文生图/AI绘画/画一个/generate image/text to image/draw/illustration

## Prerequisites

- **ComfyUI running**: `Start-Process "H:\AI\ComfyUI_windows_portable\run_nvidia_gpu.bat"`
- Listening on `http://127.0.0.1:8188`
- Available model: `sd_xl_base_1.0.safetensors` (SDXL 6.5GB)

## One-liner

```bash
python "D:\tmp\skills\ai-painter\ai-painter.py" --zh "蒸汽朋克少女" --preset hq --out D:\tmp\out
```

## Parameters

| Flag | Default | Description |
|------|---------|-------------|
| `--prompt` | required | Positive prompt |
| `--zh` | no | Treat prompt as Chinese → auto-translate keywords |
| `--preset` | std | Quality: draft/std/hq/photo/fast/anime/realistic |
| `--size` | 1:1 | Aspect: 1:1/4:3/3:4/16:9/9:16/21:9 |
| `--width` `--height` | - | Direct pixels (overrides --size) |
| `--steps` | preset | Sampling steps (overrides preset) |
| `--cfg` | preset | CFG scale (overrides preset) |
| `--seed` | random | Seed (fix to reproduce) |
| `--batch` | 1 | Number of images |
| `--out` | D:\tmp\txt2img | Output directory |
| `--dry` | - | Preview only, skip generation |

## Quality Presets

| Preset | Steps | CFG | Sampler | Speed | Best for |
|--------|-------|-----|---------|-------|---------|
| draft | 10 | 6.0 | euler | ~5s | Quick preview |
| std | 20 | 7.0 | euler/karras | ~15s | Daily use |
| hq | 30 | 7.5 | euler_ancestral/karras | ~25s | More detail |
| photo | 40 | 8.0 | dpmpp_2m_sde/karras | ~40s | Photorealistic |
| fast | 8 | 5.0 | lcm | ~3s | LCM turbo |
| anime | 25 | 7.0 | euler_ancestral/normal | ~20s | 2D anime |
| realistic | 35 | 7.0 | dpmpp_2m_sde/karras | ~30s | Realistic scenes |

Chinese aliases: 标准/精细/草稿/照片/极速/动漫/写实

## Size Presets

| Preset | Dimensions | Use |
|--------|-----------|-----|
| 1:1 | 1024×1024 | Square (default) |
| 4:3 | 1152×896 | Landscape |
| 3:4 | 896×1152 | Portrait |
| 16:9 | 1344×768 | Cinematic |
| 9:16 | 768×1344 | Phone portrait |
| 21:9 | 1536×640 | Ultra-wide |

## Chinese Keyword Support

Auto-translated when `--zh` flag or Chinese detected in prompt:

```
赛博朋克/蒸汽朋克 → cyberpunk/steampunk
像素风/动漫 → pixel art/anime
水墨画 → chinese ink wash painting
写实/超写实 → photorealistic/hyperrealistic
美少女/少女/美女 → beautiful girl/woman
机械师/机器人 → mechanic/robot
龙/狼/猫娘 → dragon/wolf/catgirl
樱花/星空/日落 → cherry blossom/starry sky/sunset
城堡/神社/灯塔 → castle/shrine/lighthouse
```

## Examples

```bash
# Chinese input (auto-detected)
python ai-painter.py --zh "赛博朋克少女在霓虹雨中" --preset hq --out D:\tmp\cyber

# English
python ai-painter.py --prompt "floating crystal island in the sky" --preset hq --size 16:9 --out D:\tmp\island

# Reproduce with seed
python ai-painter.py --prompt "dragon" --seed 42 --out D:\tmp\dragon
```

## Output Files

- `txt2img_XXXX.png` — Generated image(s)
- `meta.json` — Full params (seed, prompt, size, elapsed) — **use for reproduction**
- `prompt.txt` — Plain prompt text

## Notes

- SDXL works best at resolution ≥ 896px
- Output filename counter is global to ComfyUI's output dir (not reset per run)
- Chinese input: add `--zh` flag or let auto-detection handle it
