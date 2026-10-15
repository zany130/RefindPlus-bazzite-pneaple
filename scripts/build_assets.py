#!/usr/bin/env python3
"""Rebuild the 4K/rEFInd-sized assets from checked-in source PNGs.

Requires Pillow: python -m pip install Pillow
Run from any directory: python scripts/build_assets.py
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / 'source'
ICONS = ROOT / 'icons'
ICONS.mkdir(exist_ok=True)

base = Image.open(SRC / 'original-clean-background-1672x941.png').convert('RGB')
base.resize((3840, 2160), Image.Resampling.LANCZOS).save(ROOT / 'background.png',format='PNG',compress_level=7)

icon_files = {
  'glowing_cyan_to_magenta_monogram_icon.png':['os_bazzite.png'],
  'neon_glass_windows_logo.png':['os_win.png','os_windows.png','os_win11.png'],
  'glossy_neon_terminal_icon.png':['os_shell.png'],
  'neon_frosted_six_tooth_gear.png':['os_rescue.png'],
  'glowing_neon_microchip_icon.png':['func_firmware.png'],
  'glowing_glass_reboot_icon.png':['func_reset.png'],
  'glowing_cyan_purple_power_icon.png':['func_shutdown.png'],
}
for original, outputs in icon_files.items():
    im = Image.open(SRC / ('original-' + original)).convert('RGBA')
    alpha = im.getchannel('A').point(lambda v: 0 if v <= 2 else v)
    im.putalpha(alpha)
    size = 96 if outputs[0].startswith('func_') else 256
    im = im.resize((size, size), Image.Resampling.LANCZOS)
    for output in outputs:
        im.save(ICONS / output, format='PNG', optimize=True)

selection = Image.open(SRC / 'original-selection.png').convert('RGBA')
selection.putalpha(selection.getchannel('A').point(lambda v: 0 if v <= 2 else v))
for output, size in [('selection_big.png', 288), ('selection_small.png', 128)]:
    selection.resize((size,size), Image.Resampling.LANCZOS).save(ROOT / output, format='PNG', optimize=True)
print('Generated 4K background, 256px/96px icons and 288px/128px selection graphics')
