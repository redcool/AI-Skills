# opencode-char-3view

> 角色三视图生成器 - 用于游戏开发的角色参考图

## 功能特性

- ✅ 生成角色三视图（正面、侧面、背面）
- ✅ 7种风格预设（写实、卡通、动漫、奇幻、科幻、古风、Q版）
- ✅ 中文描述自动翻译
- ✅ 150+中文关键词词典
- ✅ 白色背景便于后期处理
- ✅ 横向布局优化三视图展示

## 快速开始

```bash
# 汉朝战士（写实风格）
python char-3view.py --desc "汉朝战士" --style realistic --zh

# 科幻士兵（卡通风格）
python char-3view.py --desc "sci-fi soldier" --style cartoon

# 奇幻法师（动漫风格）
python char-3view.py --desc "fantasy mage" --style anime

# 古代刺客（古风）
python char-3view.py --desc "古代刺客，黑衣蒙面" --style chinese --zh

# Q版精灵
python char-3view.py --desc "小精灵" --style chibi --zh
```

## 风格预设

| 风格 | 说明 | 适用场景 |
|------|------|----------|
| `realistic` | 写实、高细节 | 历史题材、写实游戏 |
| `cartoon` | 卡通、线条清晰 | 休闲游戏、动画风格 |
| `anime` | 日式动漫 | 动漫游戏、二次元 |
| `fantasy` | 奇幻概念艺术 | RPG、奇幻游戏 |
| `scifi` | 科幻、未来感 | 科幻游戏、赛博朋克 |
| `chinese` | 中国古风 | 武侠游戏、历史题材 |
| `chibi` | Q版、可爱风 | 手游、休闲游戏 |

## 参数说明

```bash
--desc, -d     角色描述（必需）
--style, -s    风格预设（默认：realistic）
--zh, -z       中文输入（自动翻译）
--seed         随机种子（-1为随机）
--width, -W    图片宽度（默认：1536）
--height, -H   图片高度（默认：640）
--steps        采样步数（默认：30）
--cfg          CFG强度（默认：7.0）
--sampler      采样器（默认：euler_ancestral）
--output, -o   输出目录（默认：D:/tmp/char-3view）
--dry-run      仅预览提示词
```

## 输出示例

```
D:/tmp/char-3view/
├── 汉朝战士_3view_20260503_094200.png
├── sci-fi soldier_3view_20260503_094350.png
└── fantasy mage_3view_20260503_094500.png
```

## 中文翻译词典

### 朝代/时代
汉朝、唐代、三国、战国、现代、未来、科幻

### 角色类型
战士、士兵、将军、骑士、剑客、刺客、法师、精灵、矮人、兽人

### 武器装备
剑、刀、枪、弓、盾、盔甲、头盔、披风、战袍

### 风格特征
男性/女性、青年/中年/老年、英俊/美丽、威武/神秘

## 依赖要求

- ComfyUI 运行中（`http://127.0.0.1:8188`）
- SDXL 模型：`sd_xl_base_1.0.safetensors`
- Python 3.10+
- `requests` 库

## 提示词构建逻辑

1. **核心结构**：character reference sheet, turnaround, three views
2. **视角指定**：front view, side view, back view
3. **角色描述**：用户输入（自动翻译）
4. **构图标签**：white background, full body, consistent design
5. **风格标签**：根据选择的风格预设
6. **质量标签**：detailed, professional, game asset

## 与其他技能联动

- **ai-painter**：从三视图生成宣传图
- **pixel-forge**：将三视图转为像素精灵
- **opencode-unity-uixml**：Unity UI角色选择界面

## 注意事项

- 白色背景方便后期提取单个视角
- 建议使用21:9或3:1的横向比例
- 保持中性姿势确保三视图一致性
- 保存seed可复现结果
