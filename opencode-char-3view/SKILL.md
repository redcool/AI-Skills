# opencode-char-3view

Generate character three-view reference sheets for game development.

## Description

This skill generates character turnaround sheets with front, side, and back views
for game characters, NPCs, enemies, and objects. Perfect for concept artists and
game developers who need consistent character references.

## Features

- **Three-View Generation**: Front, side (left), and back views in one image
- **7 Style Presets**: realistic, cartoon, anime, fantasy, scifi, chinese, chibi
- **Chinese Support**: Automatic translation of Chinese descriptions
- **Comprehensive Translation**: 150+ Chinese keywords (dynasties, classes, weapons, armor)
- **Horizontal Layout**: Optimized aspect ratios (21:9, 3:1) for three views
- **White Background**: Clean background for easy extraction

## Usage

### Basic Usage

```bash
# Realistic Han Dynasty warrior (Chinese input)
python char-3view.py --desc "汉朝战士" --style realistic --zh

# Cartoon sci-fi soldier (English input)
python char-3view.py --desc "sci-fi soldier with plasma rifle" --style cartoon

# Anime fantasy mage
python char-3view.py --desc "fantasy mage with staff and robes" --style anime

# Ancient Chinese assassin
python char-3view.py --desc "古代刺客，黑衣蒙面" --style chinese --zh

# Cute Q-version character
python char-3view.py --desc "小精灵魔法师" --style chibi --zh
```

### Advanced Options

```bash
# Fixed seed for reproducibility
python char-3view.py --desc "汉朝将军" --zh --seed 12345

# Higher quality (more steps)
python char-3view.py --desc "cyberpunk hacker" --style scifi --steps 50

# Custom dimensions
python char-3view.py --desc "knight" --style fantasy --width 1920 --height 640

# Dry run (prompt preview only)
python char-3view.py --desc "战士" --zh --dry-run
```

## Style Presets

| Style | Description | Best For |
|-------|-------------|----------|
| `realistic` | Photorealistic, detailed | Historical characters, realistic games |
| `cartoon` | Clean lines, vibrant colors | Family games, animated series style |
| `anime` | Japanese animation style | Anime games, manga style |
| `fantasy` | Fantasy concept art | RPG characters, fantasy games |
| `scifi` | Futuristic, cyberpunk | Sci-fi games, future settings |
| `chinese` | Ancient Chinese style | Wuxia games, historical China |
| `chibi` | Cute Q-version | Mobile games, casual games |

## Prompt Construction

The skill builds prompts in this priority order:

1. **Core Structure**: character reference sheet, turnaround, three views
2. **View Specification**: front view, side view (left), back view
3. **Character Description**: Your input description
4. **Composition Tags**: white background, full body, standing pose, consistent design
5. **Style Tags**: From the selected style preset
6. **Quality Tags**: detailed, professional, game asset

### Example Prompt Structure

```
character reference sheet, character turnaround, three views,
front view, side view (left), back view,
Han Dynasty warrior in traditional armor with sword,
white background, full body, standing pose, arms slightly extended,
neutral pose, same character in all views, consistent design,
photorealistic, hyperrealistic, 8k uhd, high detail,
professional photography, studio lighting, sharp focus,
detailed textures, realistic proportions,
detailed, professional concept art, game asset, character design
```

## Translation Dictionary

### Dynasties & Eras
- 汉朝/汉代 → Han Dynasty
- 唐朝/唐代 → Tang Dynasty
- 秦朝 → Qin Dynasty
- 三国 → Three Kingdoms period
- 现代/未来/科幻 → modern/future/sci-fi

### Character Classes
- 战士 → warrior
- 士兵/将军 → soldier/general
- 骑士 → knight
- 剑客/刺客 → swordsman/assassin
- 法师/巫师 → mage/wizard
- 精灵/矮人/兽人 → elf/dwarf/orc

### Weapons & Equipment
- 剑/刀/枪 → sword/blade/spear
- 弓/盾/斧 → bow/shield/axe
- 盔甲/铠甲 → armor/plate armor
- 头盔/披风 → helmet/cloak

## Output

- **Location**: `D:/tmp/char-3view/` (configurable)
- **Filename**: `{description}_3view_{timestamp}.png`
- **Format**: PNG with white background
- **Size**: Default 1536x640 (21:9 ratio)

## Requirements

- ComfyUI running at `http://127.0.0.1:8188`
- SDXL model: `sd_xl_base_1.0.safetensors`
- Python 3.10+
- `requests` library

## Notes

- White background makes it easy to extract individual views
- Arms are positioned slightly away from body for clearer side view
- Neutral pose ensures all views are recognizable as same character
- Seed is saved in output for reproduction

## Integration

This skill works with:
- **ai-painter**: Generate promotional art from three-view
- **pixel-forge**: Convert three-view to pixel art sprites
- **opencode-unity-uixml**: Use in Unity UI character selection
