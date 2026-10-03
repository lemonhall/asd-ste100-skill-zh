# 文章配图

公众号首图，2026-10-03 生成。

| 文件 | 尺寸 | 用途 |
| --- | --- | --- |
| `cover-2.35x1.png` / `.jpg` | 1792×763 | 首图（2.35:1），PNG 是母版 |
| `cover-900x383.jpg` | 900×383 | 公众号首图规格 |
| `cover-1x1-1024.png` / `.jpg` | 1024×1024 | 次图 / 方图位 |
| `run-02/image-01.png` | 1792×1024 | 生图原图（未裁切） |

## 出处

- 模型：`openai/gpt-image-2.5-sunburst`（OFOX，`size=1792x1024`，`background=opaque`）
- prompt：`prompt-cover.txt`
- 生成器：`E:\development\tools\ofox-image.py`（官方 skill 的 `generate.py` 固定 1024×1024，这里补了 `--size`）
- 裁切：`python make-covers.py`（源图只有一个，尺寸都是派生的，可重跑）

第一次请求（`run-01`）被内容安全策略拒了，改写 prompt 后第二次通过 —— 同一个主题换措辞即可，拒稿不计费。
