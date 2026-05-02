# pixel-forge — ComfyUI Text-to-Sprite Sheet Skill

## When to Use

Generate 2D game sprite sheets (transparent PNG frames + animated GIFs) from text descriptions.

**Trigger keywords**: 精灵表/sprite sheet/角色动画/行走动画/生成精灵/generate sprites/animation sheet

## Prerequisites

- **ComfyUI running**: `Start-Process "H:\AI\ComfyUI_windows_portable\run_nvidia_gpu.bat"`
- Listening on `http://127.0.0.1:8188`
- Available model: `sd_xl_base_1.0.safetensors` (SDXL)

## One-liner

```bash
python "D:\tmp\skills\pixel-forge\pixel-forge.py" --target player --mode player_sheet --prompt "samurai knight" --out D:\tmp\sprites
```

## Parameters

| Flag | Default | Description |
|------|---------|-------------|
| `--target` | required | Sprite type: **player** / creature / npc / asset |
| `--mode` | required | Animation mode (see below) |
| `--prompt` | - | Character description (Chinese auto-detected) |
| `--zh` | no | DEPRECATED: Chinese auto-detected in --prompt |
| `--out` | D:\tmp\sprites | Output directory |
| `--preset` | std | Quality: fast / std / hq / anime |
| `--width` `--height` | 1024 | Image size (pixels) |
| `--rows` `--cols` | auto | Grid dimensions (auto from target+mode) |
| `--seed` | random | Seed |
| `--duration` | 200 | GIF frame duration in ms |
| `--skip-generate` | - | Postprocess only, skip ComfyUI |
| `--input` | - | Input image for --skip-generate |

## Target → Default Grid

| Target | Default Grid | Use case |
|--------|-------------|---------|
| player | 4×4 (16 frames) | 4-direction walk cycle |
| creature | 2×2 (4 frames) | Idle / small creature |
| npc | 4×4 (16 frames) | NPC with directions |
| asset | 2×3 (6 frames) | Spell effects / FX |

## Mode → Grid Overrides

| Mode | Grid | Use |
|------|------|-----|
| player_sheet | 4×4 | 4-direction hero walk |
| idle | 2×2 | Neutral idle loop |
| walk | 2×4 | Single-direction walk |
| attack | 2×3 | Attack animation |
| cast | 2×3 | Casting / spell cast |
| hurt | 2×2 | Hit reaction |
| death | 2×2 | Death animation |
| spell | 2×3 | Spell projectile |
| projectile | 1×4 | Flying projectile loop |
| impact | 2×2 | Impact / explosion |
| explode | 2×2 | Explosion loop |
| prop | 1×1 | Single prop |
| summon | 3×3 | Summon creature / evolution |

## Quality Presets

| Preset | Steps | CFG | Sampler | Speed |
|--------|-------|-----|---------|-------|
| fast | 12 | 6.5 | euler | fastest |
| std | 20 | 7.0 | euler/karras | fast |
| hq | 30 | 7.5 | euler_ancestral/karras | medium |
| anime | 25 | 7.0 | euler_ancestral/normal | fast |

Chinese aliases: 标准/精细

## Chinese Keyword Support

Auto-translated keywords:

```
武士 → samurai  忍者 → ninja  骑士 → knight  战士 → warrior
法师 → mage  弓箭手 → archer  刺客 → assassin
喷火龙 → fire-breathing dragon  石魔 → stone golem
幽灵 → ghost  僵尸 → zombie  骷髅 → skeleton
怪物 → monster  BOSS → boss monster
火焰 → fire  冰霜 → ice  雷电 → lightning  魔法 → magic
发光 → glowing  霓虹 → neon  水晶 → crystal
猫娘 → catgirl  龙 → dragon  狼 → wolf  蝴蝶 → butterfly  凤凰 → phoenix
樱花 → cherry blossom  星空 → starry sky
```

## Examples

```bash
# 4-direction samurai player sheet
python pixel-forge.py --target player --mode player_sheet --prompt "samurai knight with red cape" --out D:\tmp\samurai

# Fire-breathing dragon idle
python pixel-forge.py --target creature --mode idle --zh "喷火龙" --preset hq --out D:\tmp\dragon

# Ice magic projectile
python pixel-forge.py --target asset --mode spell --prompt "ice magic crystal projectile" --out D:\tmp\icespell

# Ghost character
python pixel-forge.py --target creature --mode idle --zh "幽灵少女" --out D:\tmp\ghost

# Quick test (skip generation, reprocess existing image)
python pixel-forge.py --target player --mode player_sheet --skip-generate --input D:\tmp\raw-sheet.png --out D:\tmp\reproc
```

## Output Files

- `sheet-transparent.png` — **Final transparent sprite sheet** (import to game engine)
- `raw-sheet.png` — Cropped sprite sheet
- `raw-sheet-clean.png` — After chroma-key cleanup
- `animation.gif` — Full sheet animation preview
- `idle-1~4.png` — Individual frame PNGs (for 2×2)
- `down-1~4.png` — Directional frame PNGs (for 4×4)
- `pipeline-meta.json` — Full generation metadata

## Sprite Sheet Layout

```
4x4 player_sheet:
  Row 0: left-1  left-2  left-3  left-4   (facing left)
  Row 1: right-1 right-2 right-3 right-4  (facing right)
  Row 2: up-1    up-2    up-3    up-4      (facing up)
  Row 3: down-1  down-2  down-3  down-4    (facing down)

2x2 idle:
  TL: idle 1    TR: idle 2
  BL: idle 3    BR: idle 4
```

## Notes

- Sprite sheets require **solid magenta (#FF00FF) background** for chroma-key cleanup
- Generation: ~10-30s depending on preset
- For larger sprites use `--width 512 --height 512` for cell_size=128px
- The internal `scripts/generate2dsprite.py` is called automatically for postprocessing
- See `scripts/references/` for prompt building rules and mode details
