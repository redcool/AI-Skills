"""
ai-painter 示例脚本集合
用法: python run_examples.py
"""
import subprocess, sys, os

SCRIPT = r"D:\tmp\skills\ai-painter\ai-painter.py"
OUT_BASE = r"D:\tmp\skills\ai-painter\examples"

examples = [
    # (prompt, zh, preset, size, name)
    ("steampunk airship flying over clouds", False, "hq", "16:9", "steampunk_airship"),
    ("赛博朋克少女在霓虹雨中", True, "hq", "3:4", "cyberpunk_girl"),
    ("ancient asian shrine in cherry blossom, sunset", False, "std", "16:9", "shrine_sunset"),
    ("floating crystal island in the sky, magical", False, "hq", "16:9", "crystal_island"),
    ("pixel art dragon", False, "anime", "1:1", "pixel_dragon"),
]

for prompt, zh, preset, size, name in examples:
    out = os.path.join(OUT_BASE, name)
    os.makedirs(out, exist_ok=True)
    args = [sys.executable, SCRIPT,
            "--prompt", prompt,
            "--preset", preset,
            "--size", size,
            "--out", out]
    if zh:
        args.insert(2, "--zh")
    print(f"\n>>> Generating: {name}")
    r = subprocess.run(args)
    if r.returncode != 0:
        print(f"FAILED: {name}")
