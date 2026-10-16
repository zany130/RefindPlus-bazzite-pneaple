# Theme verification

Tested with patched RefindPlus Release commit `31cee4c00c2b98ce731e79bb635934884fe20ec9`, from [this successful build](https://github.com/zany130/RefindPlus/actions/runs/38934290203).

Binary SHA-256: `c973b6a92ee93871be3818cfecd04b16801bf0e27f0f55959c81b9ddd683f060`. No binary is committed in this theme repository. Both Release and Debug compiled successfully in the feature project; this theme was rendered with Release.

## Passed

- Actual QEMU/OVMF graphics rendering at **1920×1080**, with a VGA device advertising that native resolution.
- Real Firmware, Reboot and Shutdown entries rendered at the bottom with `tool_row_tune -10000`.
- Keyboard Down changes selection from an OS placeholder to Firmware. The glowing-dot indicator and shared label render at the moved tools row.
- A second VM run with `tool_row_tune 0` restores the normal tools position below the OS icons. Pixel comparison of the entire area above the original tools row (y < 628 at 1080p) is identical between the baseline and moved layout. Wallpaper and OS-row placement are unchanged.
- All existing wallpaper, icon and selection PNGs match the source theme byte-for-byte. PNG decoding and configured asset paths were checked; `git diff --check` passed.
- Preview script syntax and command-line interface checked. Captures validate the framebuffer dimensions.

The test OS entries are clearly labeled placeholders using copies of the boot manager for layout only. They were not launched. No real host disks were attached; tools were selected but firmware/reboot/shutdown actions were not executed.

## Captures

- `screenshots/refindplus-1080p-main.png`: main-row selection with tools at the bottom.
- `screenshots/refindplus-1080p-tools.png`: Firmware selected at the bottom.
- `screenshots/refindplus-1080p-baseline.png`: Firmware selected at the original tools position (`tool_row_tune 0`).

These are unedited screenshots, not composite mockups.

## Limitations and failed attempts

- A VM that initially exposed 1280×800 produced cropped output after requesting 1080p. Advertising 1920×1080 in the VM's VGA EDID before boot corrected the capture and is now part of the supplied launcher.
- **4K remains unverified.** Both standard VGA and virtio-vga attempts failed to retain a 3840×2160 framebuffer in the available OVMF setup. Those captures are not presented as successful previews. `profiles/2160p.conf` uses RefindPlus's documented UI enlargement to scale icons and font together; it needs verification on firmware that actually retains 4K.
- Earlier tests in this chat encountered intermittent host QEMU 10.2.2 SIGSEGV exits. The successful 1080p theme captures completed normally. The unrelated QEMU crash cause was not diagnosed or patched.
- Physical firmware, your live Bazzite/Windows boot entries, pointer input, Secure Boot, and the installed Shim chain have not been tested by this theme work.
- The shared selected-entry label is near the tools even when an OS icon is selected. Per-icon captions and independently located OS/tool labels are outside `tool_row_tune`'s scope.

## Reproduce

From the repository, using the exact patched binary above:

```sh
python3 scripts/preview.py --efi /absolute/path/to/x64_RefindPlus_REL.efi --capture /tmp/pneaple-moved
python3 scripts/preview.py --efi /absolute/path/to/x64_RefindPlus_REL.efi --baseline --capture /tmp/pneaple-baseline
```

These commands require existing QEMU, OVMF and Pillow. The graphical preview without `--capture` does not require Pillow. They attach no host disks, use a temporary firmware-variable file, and do not modify the installed bootloader.

After a safe hardware setup has been separately approved, compare omitted/zero and the theme's -10000 setting, navigate every tool with the keyboard, verify pointer targets, and confirm the normal Bazzite entry still boots through its existing trusted chain. Do not replace your working signed bootloader with the unsigned CI application.
