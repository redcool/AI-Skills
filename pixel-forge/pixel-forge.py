"""
ComfyUI Text-to-Sprite Sheet Generator
Generates 2D game sprite sheets with transparent PNG frames + animated GIFs.
Usage:
  python pixel-forge.py --target player --mode player_sheet --prompt "samurai knight" --out D:\tmp\sprites
  python pixel-forge.py --target creature --mode idle --prompt "喷火龙" --out D:\tmp\dragon
  (Chinese detected automatically in --prompt, no --zh flag needed)
"""
import argparse, json, time, os, sys, re, urllib.request, urllib.parse, uuid, subprocess
from pathlib import Path

COMFYUI_URL   = "http://127.0.0.1:8188"
POSTPROC_SCRIPT = Path(__file__).parent / "scripts" / "generate2dsprite.py"

# ── Config ──────────────────────────────────────────────
DEFAULT_OUT  = "D:\\tmp\\sprites"
DEFAULT_CKPT = "sd_xl_base_1.0.safetensors"

# Target -> default rows x cols
TARGET_DEFAULTS = {
    "player":   (4, 4),   # 4-direction x 4-frame
    "creature": (2, 2),   # 2x2 idle
    "npc":      (4, 4),   # 4-direction NPC
    "asset":    (2, 3),   # 2-row spell effects
}

MODE_DEFAULTS = {
    "player_sheet":  (4, 4),
    "idle":         (2, 2),
    "walk":         (2, 4),
    "attack":       (2, 3),
    "cast":         (2, 3),
    "hurt":         (2, 2),
    "death":        (2, 2),
    "spell":        (2, 3),
    "projectile":  (1, 4),
    "impact":       (2, 2),
    "explode":      (2, 2),
    "prop":         (1, 1),
    "summon":       (3, 3),
}

PRESETS = {
    "std":     (20, 7.0, "euler",               "karras",  "Balanced"),
    "fast":    (12, 6.5, "euler",               "normal",  "Fast"),
    "hq":      (30, 7.5, "euler_ancestral",      "karras",  "High detail"),
    "anime":   (25, 7.0, "euler_ancestral",      "normal",  "Anime style"),
    "标准":    (20, 7.0, "euler",               "karras",  "Balanced"),
    "精细":    (30, 7.5, "euler_ancestral",      "karras",  "High detail"),
}

DEFAULT_NEGATIVE = (
    "blurry low quality distorted deformed ugly bad anatomy "
    "bad hands extra fingers missing fingers watermark text logo "
    "signature cropped frame worst quality low resolution"
)

ZH_MAP = sorted([
    ("赛博朋克", "cyberpunk"), ("蒸汽朋克", "steampunk"),
    ("像素风", "pixel art"), ("像素艺术", "pixel art"),
    ("动漫风格", "anime style"), ("动漫", "anime"),
    ("水墨画", "chinese ink wash painting"),
    ("写实", "photorealistic"), ("超写实", "hyperrealistic"),
    ("古风", "traditional asian style"),
    ("机械师", "mechanic"), ("机器人", "robot"),
    ("美少女", "beautiful girl"), ("少女", "girl"),
    ("帅哥", "handsome man"), ("美女", "beautiful woman"),
    ("猫娘", "catgirl"), ("猫", "cat"),
    ("龙", "dragon"), ("狼", "wolf"), ("鸟", "bird"),
    ("蝴蝶", "butterfly"), ("凤凰", "phoenix"),
    ("剑", "sword"), ("盔甲", "armor"), ("披风", "cape"),
    ("魔法", "magic"), ("法术", "magic spell"),
    ("火焰", "fire"), ("冰霜", "ice"), ("雷电", "lightning"),
    ("发光", "glowing"), ("霓虹", "neon"),
    ("樱花", "cherry blossom"), ("星空", "starry sky"),
    ("城堡", "castle"), ("森林", "forest"),
    ("城市", "city"), ("废墟", "ruins"),
    ("神社", "shrine"), ("机械", "mechanical"),
    ("水晶", "crystal"), ("宝石", "gemstone"),
    ("战士", "warrior"), ("骑士", "knight"), ("法师", "mage"),
    ("弓箭手", "archer"), ("刺客", "assassin"),
    ("僵尸", "zombie"), ("骷髅", "skeleton"),
    ("喷火龙", "fire-breathing dragon"), ("石魔", "stone golem"),
    ("幽灵", "ghost"),
    ("武士", "samurai"), ("忍者", "ninja"),
    ("怪物", "monster"), ("BOSS", "boss monster"),
    ("小兵", "mob enemy"),
    ("行走", "walking"), ("待机", "idle"),
    ("攻击", "attacking"), ("施法", "casting"),
    ("受伤", "hurt"), ("死亡", "dying"),
    ("背景", "background"),
], key=lambda x: -len(x[0]))


def zh_to_en(text):
    result = text
    for zh, en in ZH_MAP:
        result = result.replace(zh, en)
    remain = re.findall(r'[\u4e00-\u9fff]+', result)
    if remain:
        untrans = [r for r in remain if len(r) > 1]
        if untrans:
            print(f"  [ZH] Untranslated: {' '.join(untrans[:5])}")
    return result

def is_zh(text):
    return bool(re.search(r'[\u4e00-\u9fff]', text))

def check_comfyui():
    try:
        urllib.request.urlopen(f"{COMFYUI_URL}/system_stats", timeout=3)
        return True
    except Exception:
        return False

def build_sprite_prompt(target, mode, description):
    if not POSTPROC_SCRIPT.exists():
        return build_prompt_fallback(target, mode, description)
    cmd = [sys.executable, str(POSTPROC_SCRIPT), "build-prompt",
           "--target", target, "--mode", mode, "--prompt", description]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if result.returncode != 0:
        print(f"  [build-prompt warning] {result.stderr[:200]}")
        return build_prompt_fallback(target, mode, description)
    return result.stdout.strip()

def build_prompt_fallback(target, mode, description):
    layouts = {
        (4, 4): "A 4x4 pixel art sprite sheet, 4-direction walk cycle",
        (2, 2): "A 2x2 pixel art sprite sheet, idle animation",
        (2, 3): "A 2x3 pixel art sprite sheet, action animation",
        (1, 4): "A 1x4 pixel art sprite sheet, loop animation",
        (2, 4): "A 2x4 pixel art sprite sheet, 2-direction walk cycle",
        (3, 3): "A 3x3 pixel art sprite sheet, evolution stages",
    }
    rows, cols = get_dimensions(target, mode)
    layout = layouts.get((rows, cols), f"A {rows}x{cols} pixel art sprite sheet")
    return f"{layout}. CHARACTER: {description}. Solid #FF00FF background. Sheet format. Top-left quadrant: neutral pose. Pixel art style."

def get_dimensions(target, mode=None):
    rows, cols = TARGET_DEFAULTS.get(target, (2, 2))
    if mode:
        m_rows, m_cols = MODE_DEFAULTS.get(mode, (None, None))
        if m_rows: rows = m_rows
        if m_cols: cols = m_cols
    return rows, cols

def build_workflow(prompt, neg, ckpt, w, h, steps, cfg, sampler, scheduler, seed):
    if seed == -1:
        import random; seed = random.randint(0, 2**32 - 1)
    return {
        "3": {"class_type": "KSampler", "inputs": {
            "seed": seed, "steps": steps, "cfg": cfg,
            "sampler_name": sampler, "scheduler": scheduler,
            "denoise": 1.0,
            "model": ["4", 0], "positive": ["6", 0],
            "negative": ["7", 0], "latent_image": ["5", 0]
        }},
        "4": {"class_type": "CheckpointLoaderSimple", "inputs": {"ckpt_name": ckpt}},
        "5": {"class_type": "EmptyLatentImage", "inputs": {"batch_size": 1, "height": h, "width": w}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["4", 1], "text": prompt}},
        "7": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["4", 1], "text": neg}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
        "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": "sprite", "images": ["8", 0]}},
    }

def queue_prompt(workflow, client_id):
    data = json.dumps({"prompt": workflow, "client_id": client_id}).encode()
    req = urllib.request.Request(
        f"{COMFYUI_URL}/prompt", data=data,
        headers={"Content-Type": "application/json"}
    )
    resp = json.loads(urllib.request.urlopen(req, timeout=30).read())
    return resp["prompt_id"]

def wait_for(prompt_id, timeout=600):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            hist = json.loads(
                urllib.request.urlopen(f"{COMFYUI_URL}/history/{prompt_id}", timeout=10).read()
            )
            if prompt_id in hist:
                return hist[prompt_id]
        except Exception:
            pass
        time.sleep(2)
    return None

def download_imgs(result, output_dir):
    saved = []
    for node_out in result.get("outputs", {}).values():
        for img in node_out.get("images", []):
            url = (f"{COMFYUI_URL}/view?filename={urllib.parse.quote(img['filename'])}"
                   f"&subfolder={urllib.parse.quote(img.get('subfolder',''))}&type=output")
            path = Path(output_dir) / img["filename"]
            path.write_bytes(urllib.request.urlopen(url, timeout=30).read())
            saved.append(str(path))
    return saved

def postprocess(raw_path, output_dir, target, mode, rows, cols):
    if not POSTPROC_SCRIPT.exists():
        print("  [skip] postprocess script not found, raw image saved")
        return
    cmd = [
        sys.executable, str(POSTPROC_SCRIPT), "process",
        "--input", str(raw_path),
        "--target", target,
        "--mode", mode,
        "--output-dir", str(output_dir),
        "--rows", str(rows),
        "--cols", str(cols),
        "--threshold", "100",
        "--edge-threshold", "150",
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')
    if result.stdout:
        print(result.stdout)
    if result.returncode != 0 and result.stderr:
        print(f"  [postprocess] {result.stderr[:200]}")

def p(s):
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode('utf-8', errors='replace').decode('utf-8', errors='replace'))


def main():
    parser = argparse.ArgumentParser(
        description="ComfyUI Text-to-Sprite Sheet Generator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Targets: player, creature, npc, asset\n"
            "Modes: idle, walk, attack, cast, hurt, death, spell, projectile, player_sheet, etc.\n"
            "Examples:\n"
            "  pixel-forge.py --target player --mode player_sheet --prompt \"samurai knight\"\n"
            "  pixel-forge.py --target creature --mode idle --prompt \"喷火龙\" --out D:\\tmp\\dragon\n"
        )
    )
    parser.add_argument("--target",  required=True, choices=["player","creature","npc","asset"], help="Sprite type")
    parser.add_argument("--mode",   required=True, help="Animation mode (idle/walk/attack/cast/player_sheet/etc.)")
    parser.add_argument("--prompt",  default="", help="Character description (Chinese auto-detected)")
    parser.add_argument("--zh",      action="store_true", help="DEPRECATED: Chinese is auto-detected in --prompt")
    parser.add_argument("--out",    default=DEFAULT_OUT, help="Output directory")
    parser.add_argument("--ckpt",  default=DEFAULT_CKPT)
    parser.add_argument("--width",   type=int, default=1024)
    parser.add_argument("--height",  type=int, default=1024)
    parser.add_argument("--preset", default="std", choices=list(PRESETS.keys()))
    parser.add_argument("--steps",   type=int)
    parser.add_argument("--cfg",     type=float)
    parser.add_argument("--sampler", help="Override sampler")
    parser.add_argument("--scheduler", help="Override scheduler")
    parser.add_argument("--seed",   type=int, default=-1)
    parser.add_argument("--rows",    type=int)
    parser.add_argument("--cols",    type=int)
    parser.add_argument("--duration", type=int, default=200, help="GIF frame duration (ms)")
    parser.add_argument("--skip-generate", action="store_true")
    parser.add_argument("--input",   help="Input image for --skip-generate")
    args = parser.parse_args()

    if not args.skip_generate and not check_comfyui():
        p("ERROR: ComfyUI not running!")
        p("Start: Start-Process \"H:\\AI\\ComfyUI_windows_portable\\run_nvidia_gpu.bat\"")
        sys.exit(1)

    os.makedirs(args.out, exist_ok=True)

    if args.prompt:
        if is_zh(args.prompt):
            desc = zh_to_en(args.prompt)
            if desc != args.prompt:
                p(f"[ZH->EN] {args.prompt}  ->  {desc}")
        else:
            desc = args.prompt
    else:
        desc = f"{args.target} {args.mode} sprite"

    p_steps   = args.steps    if args.steps    else PRESETS[args.preset][0]
    p_cfg     = args.cfg      if args.cfg      else PRESETS[args.preset][1]
    p_sampler = args.sampler  if args.sampler  else PRESETS[args.preset][2]
    p_sched   = args.scheduler if args.scheduler else PRESETS[args.preset][3]

    rows = args.rows if args.rows else get_dimensions(args.target, args.mode)[0]
    cols = args.cols if args.cols else get_dimensions(args.target, args.mode)[1]

    p("=" * 55)
    p(f"  Target : {args.target}  |  mode: {args.mode}")
    p(f"  Desc   : {desc[:70]}{'...' if len(desc)>70 else ''}")
    p(f"  Grid   : {rows} x {cols}  ({rows*cols} frames)")
    p(f"  Size   : {args.width} x {args.height}")
    p(f"  Quality: {args.preset}  steps={p_steps}  CFG={p_cfg}")
    p(f"  Sampler: {p_sampler}/{p_sched}")
    p(f"  Seed   : {'random' if args.seed==-1 else args.seed}")
    p(f"  Output : {args.out}")
    p("=" * 55)

    if args.skip_generate:
        if not args.input:
            p("ERROR: --skip-generate requires --input")
            sys.exit(1)
        raw_path = Path(args.input)
        elapsed = 0
    else:
        p("-> Building sprite prompt...")
        sprite_prompt = build_sprite_prompt(args.target, args.mode, desc)
        p(f"  Prompt: {sprite_prompt[:120]}{'...' if len(sprite_prompt)>120 else ''}")

        p("-> Submitting to ComfyUI...")
        wf = build_workflow(sprite_prompt, DEFAULT_NEGATIVE, args.ckpt,
                            args.width, args.height, p_steps, p_cfg, p_sampler, p_sched, args.seed)
        actual_seed = wf["3"]["inputs"]["seed"] if args.seed == -1 else args.seed

        prompt_id = queue_prompt(wf, str(uuid.uuid4()))
        p(f"  Task ID: {prompt_id}")
        p(f"  Waiting (est. {p_steps*2//3+5}s)...")

        t0 = time.time()
        result = wait_for(prompt_id)
        elapsed = time.time() - t0
        if not result:
            p("ERROR: Timeout!")
            sys.exit(1)

        p("  Downloading...")
        imgs = download_imgs(result, args.out)
        raw_path = Path(imgs[0]) if imgs else None
        p(f"  Raw image: {raw_path}")

    if raw_path and raw_path.exists():
        p("-> Postprocessing (chroma-key -> transparent -> frames -> GIF)...")
        postprocess(raw_path, args.out, args.target, args.mode, rows, cols)
    else:
        p("  [skip] no raw image to postprocess")

    p(f"\n[DONE] {rows}x{cols} sprite sheet{(' in '+str(round(elapsed,1))+'s') if not args.skip_generate else ''}")
    p("  Output files:")
    for f in sorted(Path(args.out).glob("*")):
        p(f"   {f.name}")

    meta = {
        "target": args.target, "mode": args.mode,
        "description": desc, "rows": rows, "cols": cols,
        "width": args.width, "height": args.height,
        "steps": p_steps, "cfg": p_cfg,
        "sampler": p_sampler, "scheduler": p_sched,
        "seed": actual_seed if not args.skip_generate else None,
        "elapsed_sec": round(elapsed, 1) if not args.skip_generate else None,
    }
    (Path(args.out) / "pipeline-meta.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8"
    )

if __name__ == "__main__":
    main()
