"""从生图原图裁出公众号要用的几个尺寸（可重跑，源图只有一个）。

    python make-covers.py [--source run-02/image-01.png]

产出（都写在本目录）：
    cover-2.35x1.png / .jpg   1792x763   公众号首图比例 2.35:1
    cover-900x383.jpg         900x383    公众号首图规格
    cover-1x1-1024.png / .jpg 1024x1024  次图 / 头像位

裁切一律居中；生图 prompt 已要求把重要元素放在中间横带，所以纵向裁掉 261 px 是安全的。
"""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent


def center_crop(image: Image.Image, ratio: float) -> Image.Image:
    width, height = image.size
    if width / height > ratio:
        new_width = int(round(height * ratio))
        left = (width - new_width) // 2
        return image.crop((left, 0, left + new_width, height))
    new_height = int(round(width / ratio))
    top = (height - new_height) // 2
    return image.crop((0, top, width, top + new_height))


def save(image: Image.Image, stem: str, size: tuple[int, int] | None = None) -> None:
    target = image.resize(size, Image.LANCZOS) if size else image
    target.save(HERE / f'{stem}.png', optimize=True)
    target.convert('RGB').save(HERE / f'{stem}.jpg', quality=92, optimize=True, progressive=True)
    print(f'{stem}.png / .jpg  {target.size[0]}x{target.size[1]}')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', default='run-02/image-01.png')
    args = parser.parse_args()
    source = Image.open(HERE / args.source)
    source.load()
    print(f'源图：{args.source}  {source.size[0]}x{source.size[1]} {source.mode}')

    wide = center_crop(source, 2.35)
    save(wide, 'cover-2.35x1')
    save(wide, 'cover-900x383', (900, 383))
    save(center_crop(source, 1.0), 'cover-1x1-1024', (1024, 1024))


if __name__ == '__main__':
    main()
