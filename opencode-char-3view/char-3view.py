#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
opencode-char-3view: Character Three-View Generator

Generate character reference sheets with front/side/back views
for game development using ComfyUI SDXL.

Usage:
    python char-3view.py --desc "汉朝战士" --style realistic
    python char-3view.py --desc "sci-fi soldier" --style cartoon --zh
    python char-3view.py --desc "medieval knight" --preset fantasy --output D:/output/
"""

import argparse
import json
import requests
import time
import random
import sys
import os
from pathlib import Path
from typing import Optional, Dict, Any

# ============================================================================
# Configuration
# ============================================================================

COMFYUI_URL = os.environ.get("COMFYUI_URL", "http://127.0.0.1:8188")
DEFAULT_MODEL = "sd_xl_base_1.0.safetensors"
DEFAULT_OUTPUT_DIR = "D:/tmp/char-3view"

# ============================================================================
# Translation Dictionary (中文 → English)
# ============================================================================

TRANSLATIONS = {
    # 朝代/时代
    "汉朝": "Han Dynasty",
    "汉代": "Han Dynasty",
    "唐朝": "Tang Dynasty",
    "唐代": "Tang Dynasty",
    "宋朝": "Song Dynasty",
    "明代": "Ming Dynasty",
    "清朝": "Qing Dynasty",
    "秦朝": "Qin Dynasty",
    "三国": "Three Kingdoms period",
    "战国": "Warring States period",
    "春秋": "Spring and Autumn period",
    "民国": "Republic of China era",
    "现代": "modern",
    "未来": "future",
    "科幻": "sci-fi",

    # 角色类型
    "战士": "warrior",
    "士兵": "soldier",
    "将军": "general",
    "骑士": "knight",
    "剑客": "swordsman",
    "刺客": "assassin",
    "弓箭手": "archer",
    "法师": "mage",
    "巫师": "wizard",
    "牧师": "priest",
    "盗贼": "rogue",
    "忍者": "ninja",
    "武士": "samurai",
    "海盗": "pirate",
    "国王": "king",
    "女王": "queen",
    "公主": "princess",
    "王子": "prince",
    "精灵": "elf",
    "矮人": "dwarf",
    "兽人": "orc",
    "巨魔": "troll",
    "龙": "dragon",
    "恶魔": "demon",
    "天使": "angel",
    "机器人": "robot",
    "机甲": "mech",

    # 武器
    "剑": "sword",
    "刀": "blade",
    "枪": "spear",
    "弓": "bow",
    "盾": "shield",
    "斧": "axe",
    "锤": "hammer",
    "杖": "staff",
    "匕首": "dagger",
    "长枪": "lance",
    "双剑": "dual swords",
    "大刀": "greatsword",

    # 装备
    "盔甲": "armor",
    "铠甲": "plate armor",
    "头盔": "helmet",
    "披风": "cloak",
    "斗篷": "cape",
    "靴子": "boots",
    "手套": "gloves",
    "腰带": "belt",
    "护肩": "shoulder guards",
    "护腿": "greaves",
    "护臂": "arm guards",

    # 服装
    "长袍": "robe",
    "战袍": "battle robe",
    "旗袍": "cheongsam",
    "汉服": "hanfu",
    "和服": "kimono",
    "制服": "uniform",
    "盔甲": "armor suit",
    "皮甲": "leather armor",

    # 风格
    "写实": "realistic",
    "卡通": "cartoon",
    "动漫": "anime",
    "奇幻": "fantasy",
    "科幻": "sci-fi",
    "古风": "ancient Chinese style",
    "蒸汽朋克": "steampunk",
    "赛博朋克": "cyberpunk",

    # 其他
    "男性": "male",
    "女性": "female",
    "青年": "young",
    "中年": "middle-aged",
    "老年": "elderly",
    "英俊": "handsome",
    "美丽": "beautiful",
    "威武": "imposing",
    "神秘": "mysterious",
    "邪恶": "evil",
    "正义": "righteous",
}

# ============================================================================
# Style Presets
# ============================================================================

STYLE_PRESETS = {
    "realistic": {
        "name": "写实风格",
        "positive": [
            "photorealistic", "hyperrealistic", "8k uhd", "high detail",
            "professional photography", "studio lighting", "sharp focus",
            "detailed textures", "realistic proportions"
        ],
        "negative": [
            "cartoon", "anime", "illustration", "painting", "drawing",
            "sketch", "stylized", "low quality", "blurry"
        ],
    },
    "cartoon": {
        "name": "卡通风格",
        "positive": [
            "cartoon style", "animated series style", "clean lines",
            "vibrant colors", "cel shaded", "stylized", "disney style",
            "pixar style", "3d render"
        ],
        "negative": [
            "photorealistic", "realistic", "photo", "grain", "noise",
            "blurry", "low quality", "ugly"
        ],
    },
    "anime": {
        "name": "动漫风格",
        "positive": [
            "anime style", "manga style", "cel shading", "vibrant colors",
            "clean lines", "japanese animation", "detailed anime art",
            "studio ghibli style"
        ],
        "negative": [
            "photorealistic", "realistic", "photo", "3d render",
            "western cartoon", "low quality", "blurry"
        ],
    },
    "fantasy": {
        "name": "奇幻风格",
        "positive": [
            "fantasy art", "detailed fantasy illustration", "magical",
            "epic fantasy", "dungeons and dragons style", "concept art",
            "digital painting", "rich colors", "detailed"
        ],
        "negative": [
            "modern", "contemporary", "photorealistic", "low quality",
            "blurry", "simple"
        ],
    },
    "scifi": {
        "name": "科幻风格",
        "positive": [
            "sci-fi", "science fiction", "futuristic", "cyberpunk",
            "high tech", "neon lights", "holographic", "advanced technology",
            "space age", "mechanical details"
        ],
        "negative": [
            "medieval", "ancient", "fantasy", "magic", "low quality",
            "blurry", "primitiv e"
        ],
    },
    "chinese": {
        "name": "古风风格",
        "positive": [
            "ancient Chinese style", "traditional Chinese painting",
            "elegant", "classical", "detailed hanfu", "period costume",
            "historical accuracy", "traditional patterns"
        ],
        "negative": [
            "modern", "western", "contemporary", "low quality",
            "blurry", "anime"
        ],
    },
    "chibi": {
        "name": "Q版风格",
        "positive": [
            "chibi", "super deformed", "cute", "small body",
            "big head", "adorable", "simple style", "kawaii"
        ],
        "negative": [
            "realistic", "photorealistic", "adult", "mature",
            "detailed", "complex", "scary"
        ],
    },
}

# ============================================================================
# Three-View Prompt Templates
# ============================================================================

THREE_VIEW_TEMPLATE = {
    "positive": [
        # Core structure
        "character reference sheet",
        "character turnaround",
        "three views",
        "front view",
        "side view (left)",
        "back view",
        # Composition
        "white background",
        "full body",
        "standing pose",
        "arms slightly extended",
        "neutral pose",
        "same character in all views",
        "consistent design",
        # Quality
        "detailed",
        "professional concept art",
        "game asset",
        "character design",
    ],
    "negative": [
        # Composition issues
        "different characters",
        "inconsistent",
        "different outfit",
        "different colors",
        "bad anatomy",
        "deformed",
        # Quality issues
        "low quality",
        "blurry",
        "watermark",
        "text",
        "signature",
        "gradient background",
        "shadows",
        "dynamic pose",
        "action pose",
    ],
}

# ============================================================================
# Translation Function
# ============================================================================

def translate_chinese(text: str) -> str:
    """Translate Chinese keywords to English."""
    import re
    result = text
    for zh, en in TRANSLATIONS.items():
        result = result.replace(zh, en + " ")
    # Normalize multiple spaces
    result = re.sub(r' +', ' ', result)
    return result.strip()

# ============================================================================
# Prompt Building
# ============================================================================

def build_prompt(description: str, style: str, is_chinese: bool = False) -> tuple:
    """
    Build positive and negative prompts for three-view generation.

    Args:
        description: Character description
        style: Style preset name
        is_chinese: Whether to translate Chinese

    Returns:
        (positive_prompt, negative_prompt)
    """
    # Translate if needed
    if is_chinese:
        description = translate_chinese(description)

    # Get style preset
    style_preset = STYLE_PRESETS.get(style, STYLE_PRESETS["realistic"])

    # Build positive prompt
    positive_parts = []

    # 1. Core three-view structure (highest priority)
    positive_parts.extend(THREE_VIEW_TEMPLATE["positive"][:6])  # Core structure

    # 2. Character description
    positive_parts.append(description)

    # 3. Composition elements
    positive_parts.extend(THREE_VIEW_TEMPLATE["positive"][6:12])

    # 4. Style-specific tags
    positive_parts.extend(style_preset["positive"])

    # 5. Quality tags
    positive_parts.extend(THREE_VIEW_TEMPLATE["positive"][12:])

    positive_prompt = ", ".join(positive_parts)

    # Build negative prompt
    negative_parts = []
    negative_parts.extend(THREE_VIEW_TEMPLATE["negative"])
    negative_parts.extend(style_preset["negative"])

    negative_prompt = ", ".join(negative_parts)

    return positive_prompt, negative_prompt

# ============================================================================
# ComfyUI Workflow
# ============================================================================

def create_workflow(
    positive_prompt: str,
    negative_prompt: str,
    seed: int = -1,
    width: int = 1536,
    height: int = 640,
    steps: int = 30,
    cfg_scale: float = 7.0,
    sampler: str = "euler_ancestral",
    scheduler: str = "normal",
    model: str = DEFAULT_MODEL,
) -> Dict[str, Any]:
    """
    Create ComfyUI workflow for three-view generation.

    Recommended dimensions:
    - 1536x640 (21:9 ratio, 3 views horizontal)
    - 1280x640 (2:1 ratio)
    - 1920x640 (3:1 ratio)
    """

    if seed == -1:
        seed = random.randint(0, 2**32 - 1)

    workflow = {
        "3": {
            "class_type": "KSampler",
            "inputs": {
                "cfg": cfg_scale,
                "denoise": 1.0,
                "latent_image": ["5", 0],
                "model": ["4", 0],
                "negative": ["7", 0],
                "positive": ["6", 0],
                "sampler_name": sampler,
                "scheduler": scheduler,
                "seed": seed,
                "steps": steps,
            },
        },
        "4": {
            "class_type": "CheckpointLoaderSimple",
            "inputs": {"ckpt_name": model},
        },
        "5": {
            "class_type": "EmptyLatentImage",
            "inputs": {
                "batch_size": 1,
                "height": height,
                "width": width,
            },
        },
        "6": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "clip": ["4", 1],
                "text": positive_prompt,
            },
        },
        "7": {
            "class_type": "CLIPTextEncode",
            "inputs": {
                "clip": ["4", 1],
                "text": negative_prompt,
            },
        },
        "8": {
            "class_type": "VAEDecode",
            "inputs": {
                "samples": ["3", 0],
                "vae": ["4", 2],
            },
        },
        "9": {
            "class_type": "SaveImage",
            "inputs": {
                "filename_prefix": "char-3view",
                "images": ["8", 0],
            },
        },
    }

    return workflow

# ============================================================================
# ComfyUI API Functions
# ============================================================================

def check_comfyui_connection(url: str = COMFYUI_URL) -> bool:
    """Check if ComfyUI is running."""
    try:
        resp = requests.get(f"{url}/system_stats", timeout=3)
        return resp.status_code == 200
    except:
        return False

def queue_prompt(workflow: Dict, url: str = COMFYUI_URL) -> str:
    """Queue workflow and return prompt ID."""
    resp = requests.post(f"{url}/prompt", json={"prompt": workflow})
    if resp.status_code != 200:
        raise Exception(f"Failed to queue prompt: {resp.text}")
    return resp.json()["prompt_id"]

def wait_for_completion(
    prompt_id: str,
    url: str = COMFYUI_URL,
    timeout: int = 300,
    poll_interval: float = 1.0,
) -> Dict:
    """Wait for workflow completion and return result."""
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            resp = requests.get(f"{url}/history/{prompt_id}")
            if resp.status_code == 200:
                data = resp.json()
                if prompt_id in data:
                    return data[prompt_id]
        except:
            pass
        time.sleep(poll_interval)

    raise TimeoutError(f"Workflow timed out after {timeout}s")

def get_output_images(result: Dict, url: str = COMFYUI_URL) -> list:
    """Extract output images from result."""
    images = []
    outputs = result.get("outputs", {})

    for node_id, node_output in outputs.items():
        if "images" in node_output:
            for img in node_output["images"]:
                filename = img["filename"]
                subfolder = img.get("subfolder", "")
                images.append({
                    "filename": filename,
                    "subfolder": subfolder,
                    "url": f"{url}/view?filename={filename}&subfolder={subfolder}",
                })

    return images

def download_image(url: str, output_path: str) -> str:
    """Download image from URL to local path."""
    resp = requests.get(url, timeout=30)
    if resp.status_code != 200:
        raise Exception(f"Failed to download image: {resp.status_code}")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(resp.content)

    return output_path

# ============================================================================
# Main Generation Function
# ============================================================================

def generate_three_view(
    description: str,
    style: str = "realistic",
    seed: int = -1,
    width: int = 1536,
    height: int = 640,
    steps: int = 30,
    cfg_scale: float = 7.0,
    sampler: str = "euler_ancestral",
    model: str = DEFAULT_MODEL,
    output_dir: str = DEFAULT_OUTPUT_DIR,
    is_chinese: bool = False,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """
    Generate character three-view image.

    Args:
        description: Character description
        style: Style preset (realistic/cartoon/anime/fantasy/scifi/chinese/chibi)
        seed: Random seed (-1 for random)
        width: Image width (recommended: 1536)
        height: Image height (recommended: 640)
        steps: Sampling steps
        cfg_scale: CFG scale
        sampler: Sampler name
        model: Model filename
        output_dir: Output directory
        is_chinese: Whether to translate Chinese
        dry_run: Only build prompts, don't generate

    Returns:
        Dict with generation results
    """
    result = {
        "description": description,
        "style": style,
        "seed": seed,
        "prompts": {},
        "images": [],
        "output_path": None,
    }

    # Build prompts
    positive, negative = build_prompt(description, style, is_chinese)
    result["prompts"] = {
        "positive": positive,
        "negative": negative,
    }

    print(f"\n{'='*60}")
    print(f"Character Three-View Generator")
    print(f"{'='*60}")
    print(f"Style: {STYLE_PRESETS.get(style, {}).get('name', style)}")
    print(f"Description: {description}")
    print(f"\n[Positive Prompt]")
    print(f"{positive[:200]}..." if len(positive) > 200 else positive)
    print(f"\n[Negative Prompt]")
    print(f"{negative[:100]}..." if len(negative) > 100 else negative)

    if dry_run:
        print(f"\n[DRY RUN] Workflow not executed")
        return result

    # Check connection
    if not check_comfyui_connection():
        raise Exception(f"ComfyUI not running at {COMFYUI_URL}")

    print(f"\n[ComfyUI] Connected to {COMFYUI_URL}")

    # Create workflow
    workflow = create_workflow(
        positive_prompt=positive,
        negative_prompt=negative,
        seed=seed,
        width=width,
        height=height,
        steps=steps,
        cfg_scale=cfg_scale,
        sampler=sampler,
        model=model,
    )

    print(f"\n[Generating] {width}x{height}, {steps} steps, seed={seed if seed >= 0 else 'random'}")

    # Queue and wait
    prompt_id = queue_prompt(workflow)
    print(f"[Queued] Prompt ID: {prompt_id}")

    completion_result = wait_for_completion(prompt_id)
    print(f"[Completed] Generation finished")

    # Get images
    images = get_output_images(completion_result)
    if not images:
        raise Exception("No images generated")

    # Download images
    os.makedirs(output_dir, exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    safe_desc = "".join(c if c.isalnum() or c in "-_" else "_" for c in description[:20])

    for i, img in enumerate(images):
        filename = img["filename"]
        ext = os.path.splitext(filename)[1] or ".png"
        local_path = os.path.join(output_dir, f"{safe_desc}_3view_{timestamp}{ext}")

        download_image(img["url"], local_path)
        result["images"].append(img)
        result["output_path"] = local_path

        print(f"[Saved] {local_path}")

    # Get actual seed from result
    if prompt_id in completion_result:
        outputs = completion_result[prompt_id].get("outputs", {})
        for node_id, node_output in outputs.items():
            if "images" in node_output:
                for img in node_output["images"]:
                    result["seed"] = img.get("seed", seed)

    return result

# ============================================================================
# CLI Interface
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Generate character three-view reference sheets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Realistic Han Dynasty warrior
  python char-3view.py --desc "汉朝战士" --style realistic --zh

  # Cartoon sci-fi soldier
  python char-3view.py --desc "sci-fi soldier with plasma rifle" --style cartoon

  # Anime fantasy mage
  python char-3view.py --desc "fantasy mage with staff" --style anime

  # Chinese ancient assassin
  python char-3view.py --desc "古代刺客，黑衣蒙面" --style chinese --zh

Available styles:
  realistic  - Photorealistic, detailed
  cartoon    - Cartoon style, clean lines
  anime      - Japanese anime style
  fantasy    - Fantasy concept art
  scifi      - Science fiction, futuristic
  chinese    - Ancient Chinese style
  chibi      - Cute Q-version style
        """
    )

    parser.add_argument(
        "--desc", "-d",
        required=True,
        help="Character description"
    )

    parser.add_argument(
        "--style", "-s",
        choices=list(STYLE_PRESETS.keys()),
        default="realistic",
        help="Style preset (default: realistic)"
    )

    parser.add_argument(
        "--zh", "-z",
        action="store_true",
        help="Translate Chinese keywords to English"
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=-1,
        help="Random seed (-1 for random)"
    )

    parser.add_argument(
        "--width", "-W",
        type=int,
        default=1536,
        help="Image width (default: 1536)"
    )

    parser.add_argument(
        "--height", "-H",
        type=int,
        default=640,
        help="Image height (default: 640)"
    )

    parser.add_argument(
        "--steps",
        type=int,
        default=30,
        help="Sampling steps (default: 30)"
    )

    parser.add_argument(
        "--cfg",
        type=float,
        default=7.0,
        help="CFG scale (default: 7.0)"
    )

    parser.add_argument(
        "--sampler",
        default="euler_ancestral",
        choices=["euler", "euler_ancestral", "dpmpp_2m", "dpmpp_2m_sde", "ddim"],
        help="Sampler (default: euler_ancestral)"
    )

    parser.add_argument(
        "--model", "-m",
        default=DEFAULT_MODEL,
        help=f"Model filename (default: {DEFAULT_MODEL})"
    )

    parser.add_argument(
        "--output", "-o",
        default=DEFAULT_OUTPUT_DIR,
        help=f"Output directory (default: {DEFAULT_OUTPUT_DIR})"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Build prompts but don't generate"
    )

    args = parser.parse_args()

    try:
        result = generate_three_view(
            description=args.desc,
            style=args.style,
            seed=args.seed,
            width=args.width,
            height=args.height,
            steps=args.steps,
            cfg_scale=args.cfg,
            sampler=args.sampler,
            model=args.model,
            output_dir=args.output,
            is_chinese=args.zh,
            dry_run=args.dry_run,
        )

        print(f"\n{'='*60}")
        print(f"Generation complete")
        print(f"{'='*60}\n")

    except KeyboardInterrupt:
        print(f"\n[Cancelled]")
        sys.exit(1)
    except Exception as e:
        print(f"\n[Error] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
