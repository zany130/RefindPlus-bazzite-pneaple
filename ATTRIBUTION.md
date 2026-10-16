# Credits, asset provenance and license scope

This repository is an **unofficial rEFInd theme**, not an official or endorsed release of Bazzite, Universal Blue, Microsoft, rEFInd, or the other projects cited below. Names, artwork and trademarks belong to their respective rights holders.

## Shadow-rEFInd graphics (GNU AGPL-3.0)

The rEFInd icon collection is sourced from [chris1111/Shadow-rEFInd](https://github.com/chris1111/Shadow-rEFInd) at pinned Git revision `fe639d2869f59d291489c0c416c17577bd166046`.

- Imported original PNGs in `icons/` cover the upstream OS icon family (`os_*`), functional icons (`func_*`), utility icons (`tool_*`), volume badges (`vol_*`), boot labels (`boot_*`), and navigation/decorative icons. **Unmodified upstream selection graphics remain at `icons/selection_big.png` and `icons/selection_small.png`.** The two **root-level** `selection_big.png` and `selection_small.png` images are now original, transparent Pneaple-specific glowing-dot active-selection graphics rather than unchanged Shadow-rEFInd originals.
- **Original upstream assets are unchanged** where they remain under `icons/` (except that the **custom** `icons/os_bazzite.png` is not an upstream file). Extra aliases such as `icons/os_win11.png` reuse the corresponding Shadow Windows icon image. The replaced Bazzite image is recreated from the user-approved, ChatGPT-assisted glowing cyan/magenta monogram asset at `source/original-glowing_cyan_to_magenta_monogram_icon.png`, not from Shadow-rEFInd or from official Bazzite brand files. The root-level selection graphics are theme originals; they are not represented as imported Shadow selections.
- Imported assets remain under Shadow-rEFInd's **GNU AGPL-3.0** license. Preserve the source attribution and the complete license notice in [third_party/Shadow-rEFInd-AGPL-3.0.txt](third_party/Shadow-rEFInd-AGPL-3.0.txt) when redistributing.
- The repository's root `LICENSE` applies **MIT only to independently originated project material**, not to imported AGPL-3.0 graphics; the MIT license does not supersede AGPL-3.0 terms.

## Bazzite Convergence wallpaper and derived design

- **Official source:** [Convergence_Wallpaper.png in Bazzite's press kit](https://github.com/ublue-os/bazzite/blob/main/press_kit/art/Convergence_Wallpaper.png); related Bazzite wallpapers are also collected in the [Universal Blue artwork repository](https://github.com/ublue-os/artwork/tree/main/wallpapers/bazzite/images).
- **Adaptation:** `background.png` incorporates and recomposes the Convergence gaming-room illustration as a 4K boot-menu wallpaper, with translucent header/menu/footer bands and the final “PNEAPLE GAMING THEME” heading. The central menu band has been extended downward to sit behind rEFInd's utility row; the footer band remains unchanged. This is **not** the original unmodified official wallpaper.
- **Supporting source files:** PNGs under `source/` are historic/generated assets and prior visual composition inputs; none are necessary on the EFI System Partition.
- **Screenshots:** `screenshots/concept-preview.png` is a design mockup; `screenshots/preview.png` is a real rEFInd screenshot from **QEMU/OVMF**, not actual physical UEFI.
- **Licensing:** the [Universal Blue artwork repository](https://github.com/ublue-os/artwork) declares Apache-2.0 at the repository level but expressly warns that **individual wallpapers may have different licenses**. The file-specific Convergence license and permission to publish this particular derivative are **not independently verified**. The theme's MIT license and attribution do not grant such permissions; seek a decision from the rights holder before a release that assumes they do.

## Design inspiration

- [Pneaple Boot Theme](https://github.com/pineapplelite/Pneaple-Boot-Theme) by pineapplelite (MIT): translucent black band and menu treatment.
- [rEFInd Lumen](https://github.com/shoxjaxon-atabayev/rEFInd-lumen) by Shoxjaxon Atabayev (MIT): general glow aesthetic.
- [BsxM1](https://github.com/AlexFullmoon/refind-bsxm1-theme) by AlexFullmoon: icon shadow styling.
- These themes are **inspiration**, not sources of copied application code or third-party icons in this repository.

## Logo and permission caveats

Bazzite, Universal Blue, Microsoft, Windows, and other third-party identifiers are the property of their respective owners. The custom Bazzite icon is not an official branding-license grant. This documentation records known sources and license terms; it does not imply consent from rightsholders or resolve any specifically unverified wallpaper permissions.

See the project [README](README.md) for safe installation and QEMU-versus-hardware testing distinctions.
