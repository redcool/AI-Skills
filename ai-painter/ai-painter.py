"""
ComfyUI Text-to-Image
One-shot script with Chinese keyword support and quality presets.
Usage:
  python comfyui_txt2img.py --prompt "a cat" --out D:\tmp\out
  python comfyui_txt2img.py --prompt "steampunk city" --preset hq --out D:\tmp
"""
import argparse, json, uuid, time, os, sys, re, urllib.request, urllib.parse
from pathlib import Path

# ── Config ──────────────────────────────────────────────
COMFYUI_URL  = "http://127.0.0.1:8188"
DEFAULT_CKPT = "sd_xl_base_1.0.safetensors"
DEFAULT_OUT  = "D:\\tmp\\txt2img"

SIZE_PRESETS = {
    "1:1":   (1024, 1024),
    "4:3":   (1152, 896),
    "3:4":   (896,  1152),
    "16:9":  (1344, 768),
    "9:16":  (768,  1344),
    "21:9":  (1536, 640),
}
DEFAULT_SIZE = "1:1"

# quality presets: (steps, cfg, sampler, scheduler, description)
PRESETS = {
    "draft":  (10,  6.0, "euler",               "normal",  "Fast draft, a few seconds"),
    "std":    (20,  7.0, "euler",               "karras",  "Balanced quality and speed"),
    "hq":     (30,  7.5, "euler_ancestral",    "karras",  "More details"),
    "photo":  (40,  8.0, "dpmpp_2m_sde",         "karras",  "Photorealistic"),
    "fast":   (8,   5.0, "lcm",                 "normal",  "LCM acceleration"),
    "anime":  (25,  7.0, "euler_ancestral",      "normal",  "Anime style"),
    "realistic": (35, 7.0, "dpmpp_2m_sde",      "karras",  "Realistic"),
    # Chinese aliases
    "标准":  (20,  7.0, "euler",               "karras",  "Balanced"),
    "精细":  (30,  7.5, "euler_ancestral",       "karras",  "More details"),
    "草稿":  (10,  6.0, "euler",               "normal",  "Fast draft"),
    "照片":  (40,  8.0, "dpmpp_2m_sde",         "karras",  "Photorealistic"),
    "极速":  (8,   5.0, "lcm",                 "normal",  "LCM fast"),
    "动漫":  (25,  7.0, "euler_ancestral",       "normal",  "Anime style"),
    "写实":  (35,  7.0, "dpmpp_2m_sde",         "karras",  "Realistic"),
}

DEFAULT_NEGATIVE = (
    "blurry low quality distorted deformed ugly bad anatomy "
    "bad hands extra fingers missing fingers watermark text logo "
    "signature cropped frame worst quality low resolution "
    "jpeg artifacts mutated disfigured malformed gross proportions"
)

# Chinese keyword map (sorted by length desc for greedy matching)
ZH_MAP = sorted([
    ("赛博朋克少女", "cyberpunk girl"),
    ("赛博朋克", "cyberpunk"),
    ("蒸汽朋克机械师", "steampunk mechanic"),
    ("蒸汽朋克", "steampunk"),
    ("像素艺术风格", "pixel art style"),
    ("像素风格", "pixel art style"),
    ("像素艺术", "pixel art"),
    ("像素风", "pixel art"),
    ("动漫风格", "anime style"),
    ("水墨画风格", "chinese ink wash painting style"),
    ("水墨风格", "chinese ink wash painting"),
    ("水墨画", "chinese ink wash painting"),
    ("水墨", "ink wash painting"),
    ("超写实风格", "hyperrealistic style"),
    ("超写实", "hyperrealistic"),
    ("写实风格", "photorealistic style"),
    ("写实", "photorealistic"),
    ("机械师", "mechanic"),
    ("美少女", "beautiful girl"),
    ("古风建筑", "traditional asian architecture"),
    ("古风", "traditional asian style"),
    ("科幻风格", "sci-fi style"),
    ("奇幻风格", "fantasy style"),
    ("魔法风格", "magic fantasy style"),
    ("发光效果", "glowing effect"),
    ("发光", "glowing"),
    ("霓虹灯光", "neon lights"),
    ("霓虹", "neon"),
    ("下雨天", "rainy weather"),
    ("下雨", "rain"),
    ("雷雨", "thunderstorm"),
    ("日落时分", "during sunset"),
    ("日落", "sunset"),
    ("日出", "sunrise"),
    ("夜空", "night sky"),
    ("星空下", "under the starry sky"),
    ("星空", "starry sky"),
    ("樱花树下", "under cherry blossom trees"),
    ("樱花", "cherry blossom"),
    ("枫叶", "autumn maple leaves"),
    ("废墟中", "among ruins"),
    ("废墟", "ruins"),
    ("古镇", "ancient town"),
    ("山川", "mountains"),
    ("大海", "ocean"),
    ("河流", "river"),
    ("灯塔", "lighthouse"),
    ("神社", "shrine"),
    ("奇幻", "fantasy"),
    ("科幻", "sci-fi"),
    ("魔法", "magic"),
    ("水晶", "crystal"),
    ("宝石", "gemstone"),
    ("飞艇", "airship"),
    ("飞船", "airship"),
    ("战舰", "battleship"),
    ("战甲", "combat armor"),
    ("盔甲", "armor"),
    ("披风", "flowing cape"),
    ("城堡", "castle"),
    ("森林", "forest"),
    ("城市", "city"),
    ("机械", "mechanical machinery"),
    ("机器人", "robot"),
    ("齿轮工坊", "gear workshop"),
    ("工坊", "workshop"),
    ("猫娘", "catgirl"),
    ("猫", "cat"),
    ("龙", "dragon"),
    ("狼", "wolf"),
    ("鸟", "bird"),
    ("少女", "girl"),
    ("帅哥", "handsome man"),
    ("女孩", "girl"),
    ("男孩", "boy"),
    ("美女", "beautiful woman"),
    ("夜景", "night view"),
    ("华丽的", "magnificent"),
    ("精致的", "exquisite"),
    ("细腻的", "delicate"),
    ("梦幻的", "dreamy"),
    ("神秘的", "mysterious"),
    ("庄严的", "solemn"),
    ("宁静的", "tranquil"),
    ("喧闹的", "bustling"),
    ("背景下", "in background"),
    ("背景下", ""),
    ("的", " "),
], key=lambda x: -len(x[0]))


# ── Helpers ─────────────────────────────────────────────
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

def build_workflow(prompt, neg, ckpt, w, h, steps, cfg, sampler, scheduler, seed, batch=1):
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
        "5": {"class_type": "EmptyLatentImage", "inputs": {"batch_size": batch, "height": h, "width": w}},
        "6": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["4", 1], "text": prompt}},
        "7": {"class_type": "CLIPTextEncode", "inputs": {"clip": ["4", 1], "text": neg}},
        "8": {"class_type": "VAEDecode", "inputs": {"samples": ["3", 0], "vae": ["4", 2]}},
        "9": {"class_type": "SaveImage", "inputs": {"filename_prefix": "txt2img", "images": ["8", 0]}},
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

def p(s):
    """Print with fallback encoding for Windows GBK"""
    try:
        print(s)
    except UnicodeEncodeError:
        print(s.encode('utf-8', errors='replace').decode('utf-8', errors='replace'))


# ── Main ────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="ComfyUI Text-to-Image with Chinese keyword support",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Size presets: " + ", ".join(SIZE_PRESETS.keys()) + "\n"
            "Quality presets: " + ", ".join(PRESETS.keys()) + "\n\n"
            "Examples:\n"
            "  comfyui_txt2img.py --zh \"cyberpunk girl with neon\"\n"
            "  comfyui_txt2img.py --prompt \"fantasy castle\" --preset hq\n"
        )
    )
    parser.add_argument("--prompt",    required=True, help="Positive prompt (use --zh for Chinese)")
    parser.add_argument("--zh",        action="store_true", help="Treat prompt as Chinese and translate")
    parser.add_argument("--negative",  default=DEFAULT_NEGATIVE)
    parser.add_argument("--ckpt",      default=DEFAULT_CKPT)
    parser.add_argument("--size",      default=DEFAULT_SIZE, help="Size preset: " + ", ".join(SIZE_PRESETS.keys()))
    parser.add_argument("--width",     type=int, help="Pixel width (overrides --size)")
    parser.add_argument("--height",    type=int, help="Pixel height (overrides --size)")
    parser.add_argument("--preset",   default="std", help="Quality preset: " + ", ".join(PRESETS.keys()))
    parser.add_argument("--steps",     type=int, help="Sampling steps (overrides --preset)")
    parser.add_argument("--cfg",        type=float, help="CFG scale (overrides --preset)")
    parser.add_argument("--sampler",   help="Sampler name (overrides --preset)")
    parser.add_argument("--scheduler", help="Scheduler (overrides --preset)")
    parser.add_argument("--seed",     type=int, default=-1, help="Seed (-1=random)")
    parser.add_argument("--batch",     type=int, default=1, help="Batch count")
    parser.add_argument("--out",       default=DEFAULT_OUT, help="Output directory")
    parser.add_argument("--dry",       action="store_true", help="Print params only, skip generation")
    args = parser.parse_args()

    if not args.dry and not check_comfyui():
        p("ERROR: ComfyUI is not running!")
        p("Start it with: Start-Process \"H:\\AI\\ComfyUI_windows_portable\\run_nvidia_gpu.bat\"")
        sys.exit(1)

    raw_prompt = args.prompt
    if args.zh or is_zh(args.prompt):
        prompt = zh_to_en(args.prompt)
        if prompt != args.prompt:
            p(f"[ZH->EN] {args.prompt}  ->  {prompt}")
    else:
        prompt = args.prompt

    if args.width and args.height:
        w, h = args.width, args.height
    else:
        w, h = SIZE_PRESETS.get(args.size, (1024, 1024))

    p_steps   = args.steps    if args.steps    else PRESETS.get(args.preset, (20,))[0]
    p_cfg     = args.cfg      if args.cfg      else PRESETS.get(args.preset, (20, 7.0))[1]
    p_sampler = args.sampler  if args.sampler  else PRESETS.get(args.preset, (20, 7.0, "euler"))[2]
    p_sched   = args.scheduler if args.scheduler else PRESETS.get(args.preset, (20, 7.0, "euler", "normal"))[3]
    p_desc    = PRESETS.get(args.preset, (20,))[4] if not args.steps else "(custom)"

    p("=" * 55)
    p(f"  Prompt : {prompt[:80]}{'...' if len(prompt)>80 else ''}")
    p(f"  Size   : {w} x {h}  |  preset: {args.preset} ({p_desc})")
    p(f"  Sampler: {p_sampler}/{p_sched}  |  steps: {p_steps}  CFG: {p_cfg}")
    p(f"  Seed   : {'random' if args.seed==-1 else args.seed}")
    p(f"  Output : {args.out}")
    p("=" * 55)

    if args.dry:
        p("[DRY] Preview only, skipping generation")
        sys.exit(0)

    os.makedirs(args.out, exist_ok=True)
    client_id = str(uuid.uuid4())

    wf = build_workflow(prompt, args.negative, args.ckpt, w, h,
                        p_steps, p_cfg, p_sampler, p_sched, args.seed, args.batch)
    actual_seed = wf["3"]["inputs"]["seed"] if args.seed == -1 else args.seed

    p("-> Submitting to ComfyUI...")
    prompt_id = queue_prompt(wf, client_id)
    p(f"  Task ID: {prompt_id}")

    p(f"  Waiting (est. {p_steps*2//3 + 5}s)...")
    t0 = time.time()
    result = wait_for(prompt_id)
    elapsed = time.time() - t0

    if not result:
        p("ERROR: Timeout! ComfyUI may be overloaded, retry later")
        sys.exit(1)

    p("  Downloading images...")
    saved = download_imgs(result, args.out)

    meta = {
        "prompt":     prompt,
        "raw_prompt": raw_prompt,
        "negative":   args.negative,
        "checkpoint": args.ckpt,
        "width":      w, "height": h,
        "steps":      p_steps, "cfg": p_cfg,
        "sampler":    p_sampler, "scheduler": p_sched,
        "seed":       actual_seed,
        "preset":     args.preset,
        "elapsed_sec": round(elapsed, 1),
        "files":      [Path(f).name for f in saved],
    }
    meta_path = Path(args.out) / "meta.json"
    meta_path.write_text(json.dumps(meta, indent=2, ensure_ascii=False), encoding="utf-8")
    (Path(args.out) / "prompt.txt").write_text(prompt, encoding="utf-8")

    p(f"\n[DONE] {len(saved)} image(s) in {elapsed:.1f}s")
    for f in saved:
        p(f"   {f}")
    p(f"   {meta_path}")

if __name__ == "__main__":
    main()
