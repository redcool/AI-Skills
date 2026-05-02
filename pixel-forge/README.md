# pixel-forge — ComfyUI 精灵表生成器

通过文字描述，调用 ComfyUI + SDXL 生成游戏精灵表（透明 PNG + 动画 GIF），支持中文自动翻译。

## 环境依赖

| 依赖 | 说明 |
|------|------|
| **ComfyUI** | `H:\AI\ComfyUI_windows_portable\run_nvidia_gpu.bat` |
| **SDXL 模型** | `ComfyUI\models\checkpoints\sd_xl_base_1.0.safetensors` |
| **Python 库** | Pillow / numpy（自动安装）|
| **Python** | 3.x |

## 快速开始

```bash
# 启动 ComfyUI（如未运行）
Start-Process "H:\AI\ComfyUI_windows_portable\run_nvidia_gpu.bat"

# 生成角色精灵表
python H:\AI\AI_SKILLS\pixel-forge\pixel-forge.py --target player --mode player_sheet --prompt "catgirl mage" --out D:\tmp\sprites

# 生成生物待机
python H:\AI\AI_SKILLS\pixel-forge\pixel-forge.py --target creature --mode idle --zh "喷火龙" --out D:\tmp\dragon
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `--target` | 类型：`player / creature / npc / asset` |
| `--mode` | 动画模式（见下表）|
| `--prompt` | 角色描述（中文自动翻译）|
| `--zh` | 废弃：prompt 中的中文自动检测 |
| `--preset` | 质量：`fast / std / hq / anime` |
| `--out` | 输出目录 |

## 精灵布局

| Target | 默认 | 用途 |
|--------|------|------|
| player | 4×4（16帧）| 四方向行走循环 |
| creature | 2×2（4帧）| 生物待机 |
| npc | 4×4（16帧）| NPC 对话/行走 |
| asset | 2×3（6帧）| 法术/特效 |

| Mode | 布局 | 用途 |
|------|------|------|
| player_sheet | 4×4 | 四方向行走 |
| idle | 2×2 | 待机循环 |
| walk | 2×4 | 单方向行走 |
| attack | 2×3 | 攻击动画 |
| cast | 2×3 | 施法 |
| hurt | 2×2 | 受击 |
| death | 2×2 | 死亡 |
| spell | 2×3 | 法术特效 |
| projectile | 1×4 | 飞行物循环 |
| impact | 2×2 | 冲击 |
| explode | 2×2 | 爆炸 |
| prop | 1×1 | 单个道具 |
| summon | 3×3 | 召唤进化 |

## 输出文件

```
out/
  sheet-transparent.png   ← 最终透明精灵表（导入游戏用）
  raw-sheet.png          ← 裁剪后的原始表
  raw-sheet-clean.png    ← 色键清理后
  animation.gif          ← 全表动画预览 GIF
  idle-1.png ~ idle-4.png  ← 单帧 PNG
  down-1.png ~           ← 逐方向分帧
  pipeline-meta.json      ← 完整参数
```

## 精灵表布局

```
4x4 player_sheet:
  [左-1 左-2 左-3 左-4]   ← 向左
  [右-1 右-2 右-3 右-4]   ← 向右
  [上-1 上-2 上-3 上-4]   ← 向后
  [下-1 下-2 下-3 下-4]   ← 向前

2x2 idle:
  [待机1] [待机2]
  [待机3] [待机4]
```
