"""
pixel-forge 示例脚本集合
用法: python run_examples.py
"""
import subprocess, sys, os

SCRIPT = r"D:\tmp\skills\pixel-forge\pixel-forge.py"
OUT_BASE = r"D:\tmp\skills\pixel-forge\examples"

examples = [
    # (target, mode, prompt, zh, preset, name)
    ("creature", "idle", "fire breathing dragon", False, "hq", "dragon_idle"),
    ("player", "player_sheet", "samurai knight with flowing cape", False, "std", "samurai"),
    ("creature", "idle", "幽灵少女", True, "hq", "ghost_girl"),
    ("asset", "spell", "ice magic crystal projectile", False, "std", "ice_spell"),
    ("creature", "idle", "机械石魔", True, "std", "stone_golem"),
    ("npc", "walk", "年老的长者杖", True, "fast", "npc_elder"),
]

for target, mode, prompt, zh, preset, name in examples:
    out = os.path.join(OUT_BASE, name)
    os.makedirs(out, exist_ok=True)
    args = [sys.executable, SCRIPT,
            "--target", target,
            "--mode", mode,
            "--prompt", prompt,
            "--preset", preset,
            "--out", out]
    if zh:
        args.insert(2, "--zh")
    print(f"\n>>> Generating: {name}")
    r = subprocess.run(args)
    if r.returncode != 0:
        print(f"FAILED: {name}")
