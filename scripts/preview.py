#!/usr/bin/env python3
"""Preview this theme in an isolated QEMU VM, without attaching host disks."""
import argparse
import json
from pathlib import Path
import shutil
import socket
import subprocess
import tempfile
import time

p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--efi', required=True, type=Path, help='patched RefindPlus x64 EFI binary')
p.add_argument('--resolution', choices=['1920x1080', '3840x2160'], default='1920x1080')
p.add_argument('--baseline', action='store_true', help='override tool_row_tune to zero for comparison')
p.add_argument('--capture', type=Path, help='headless capture directory; requires Pillow')
a = p.parse_args()
repo = Path(__file__).resolve().parents[1]
efi = a.efi.resolve(strict=True)
fw = Path('/usr/share/edk2/ovmf')
if not (fw/'OVMF_CODE.fd').exists():
    fw = Path('/usr/share/OVMF')
for name in ['OVMF_CODE.fd', 'OVMF_VARS.fd']:
    if not (fw/name).is_file():
        p.error(f'Missing OVMF file: {fw/name}')
if a.capture:
    from PIL import Image
    a.capture = a.capture.resolve()
    a.capture.mkdir(parents=True, exist_ok=True)
with tempfile.TemporaryDirectory(prefix='pneaple-refindplus-') as tmp:
    tmp = Path(tmp)
    boot = tmp/'esp/EFI/BOOT'
    theme = boot/'themes/RefindPlus-bazzite-pneaple'
    theme.mkdir(parents=True)
    for name in ['background.png', 'theme.conf', 'selection_big.png', 'selection_small.png']:
        shutil.copy2(repo/name, theme/name)
    for name in ['icons', 'profiles']:
        shutil.copytree(repo/name, theme/name)
    shutil.copy2(efi, boot/'BOOTX64.EFI')
    test = tmp/'esp/EFI/Test'
    test.mkdir()
    shutil.copy2(efi, test/'layout.efi')
    config = f'''timeout 0
resolution {a.resolution.replace('x', ' ')}
scanfor manual
showtools firmware,reboot,shutdown
include themes/RefindPlus-bazzite-pneaple/theme.conf
'''
    if a.resolution == '3840x2160':
        config += 'include themes/RefindPlus-bazzite-pneaple/profiles/2160p.conf\n'
    if a.baseline:
        config += 'tool_row_tune 0\n'
    for title, icon in [('Bazzite (VM layout test)', 'os_bazzite.png'), ('Windows (VM layout test)', 'os_win11.png')]:
        config += f'''menuentry "{title}" {{
    loader \\EFI\\Test\\layout.efi
    icon \\EFI\\BOOT\\themes\\RefindPlus-bazzite-pneaple\\icons\\{icon}
}}
'''
    (boot/'config.conf').write_text(config)
    variables = tmp/'vars.fd'
    shutil.copy2(fw/'OVMF_VARS.fd', variables)
    command = ['qemu-system-x86_64', '-machine', 'q35', '-accel', 'tcg', '-m', '1024',
        '-drive', f'if=pflash,format=raw,readonly=on,file={fw}/OVMF_CODE.fd',
        '-drive', f'if=pflash,format=raw,file={variables}',
        '-drive', f'format=raw,file=fat:rw:{tmp}/esp',
        '-net', 'none', '-vga', 'none', '-device', f'VGA,vgamem_mb=64,xres={a.resolution.split("x")[0]},yres={a.resolution.split("x")[1]}']
    print('VM only: no host disks. Test entries are placeholders; do not launch them.', flush=True)
    if not a.capture:
        subprocess.run(command, check=True)
    else:
        sock = tmp/'qmp.sock'
        command += ['-display', 'none', '-qmp', f'unix:{sock},server=on,wait=off']
        with (a.capture/'qemu.log').open('w') as log:
            proc = subprocess.Popen(command, stderr=log)
            try:
                for _ in range(100):
                    if sock.exists(): break
                    if proc.poll() is not None: raise RuntimeError(f'QEMU exited: {proc.returncode}')
                    time.sleep(.1)
                with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
                    client.settimeout(10)
                    client.connect(str(sock))
                    with client.makefile('rwb', buffering=0) as f:
                        f.readline()
                        def qmp(name, args=None):
                            f.write((json.dumps({'execute': name, 'arguments': args or {}})+'\n').encode())
                            while True:
                                raw = f.readline()
                                if not raw: raise RuntimeError(f'QEMU disconnected: {proc.poll()}')
                                result = json.loads(raw)
                                if 'error' in result: raise RuntimeError(result)
                                if 'return' in result: return result['return']
                        qmp('qmp_capabilities')
                        time.sleep(40)
                        for name, key in [('main', None), ('tools', 'down')]:
                            if key:
                                qmp('human-monitor-command', {'command-line': f'sendkey {key}'})
                                time.sleep(1)
                            ppm = a.capture/f'{name}.ppm'
                            qmp('screendump', {'filename': str(ppm)})
                            image = Image.open(ppm)
                            expected = tuple(map(int, a.resolution.split('x')))
                            if image.size != expected:
                                raise RuntimeError(f'Framebuffer {image.size} does not match {expected}')
                            image.save(a.capture/f'{name}.png')
                            ppm.unlink()
                        qmp('quit')
                proc.wait(timeout=10)
            finally:
                if proc.poll() is None:
                    proc.terminate()
                    proc.wait(timeout=10)
        print(f'Captured {a.resolution}: {a.capture}', flush=True)
