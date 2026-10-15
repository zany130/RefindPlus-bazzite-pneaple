# Publishing this theme on GitHub

> This repository is a **first test candidate**. Verify it on actual UEFI firmware and get a screenshot before marking it stable.

GitHub repository suggestion: `zany130/rEFInd-bazzite-pneaple`.

1. Create a new **public empty repository** in your GitHub account at https://github.com/new . Use `rEFInd-bazzite-pneaple` as its name, and **do not check** "Add README", "Add .gitignore", or "Choose a license" (they are already inside this source package).
2. Download and extract `rEFInd-bazzite-pneaple-source.zip` **outside the ESP**, e.g. into `~/Projects/`.
3. Open a shell in the extracted directory (containing `theme.conf` and `README.md`) and run:

```bash
git init -b main
git add .
git commit -m 'Initial Bazzite Pneaple rEFInd theme test build'
git remote add origin https://github.com/zany130/rEFInd-bazzite-pneaple.git
git push -u origin main
```

GitHub will authenticate through your local Git credential helper. Never paste tokens/passwords into chat.

4. After the first successful firmware rendering test, take a real boot-menu screenshot and replace the illustrative preview in `screenshots/` or add a separately labeled `screenshots/actual-refind.png`.
5. Optionally publish `rEFInd-bazzite-pneaple-install.zip` as a **pre-release** asset under `v0.1.0-beta`. Do not market it as a fully tested stable release until you confirm menu placement.

If the GitHub CLI `gh` is installed/authenticated on your Bazzite machine, alternative one-command publication from the extracted source directory is `gh repo create zany130/rEFInd-bazzite-pneaple --public --source=. --push` (after making the initial local commit). Only use this if the GitHub repository does not already exist.
