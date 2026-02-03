# 🪟 HTML Desktop Wrapper (Archived)
### Run HTML games / web apps as a native-feeling desktop app (PyQt6 + QtWebEngine)

This project is a lightweight desktop shell that renders either a **local HTML file** or a **web URL** inside a frameless PyQt6 window powered by **QtWebEngine (Chromium)**.

It was built to make HTML games and small web apps feel portable and “app-like” — without rewriting them.

---

## ✨ What it does

- ✅ Loads **local HTML** (default: `index.html`) *or* a **web URL**
- 🪟 **Frameless window UI** with custom window controls (min/max/close)
- 🖱️ Drag window from the top bar area
- ⌨️ Shortcuts:
  - `F11` → maximize/restore
  - `Ctrl+F` → fullscreen toggle
  - `Esc` → close
- 🧰 Right-click → **Inspect** to open Chromium DevTools (debug HTML/JS/CSS)
- ⚡ Optional GPU disable switch for stability on some systems
- 📦 Can be packaged as a **single executable** with PyInstaller

---

## 🧠 Why this exists

HTML games and small web apps are incredibly portable — until you want them to:
- run like a desktop app
- ship as a single file
- have a clean window chrome
- keep DevTools available for debugging

This repo is a simple “HTML → Desktop App” wrapper for exactly that workflow.

---

## 📦 Requirements

- Python 3.8+ recommended
- Dependencies:

```bash
pip install PyQt6 PyQt6-WebEngine pyinstaller
```
## ▶️ Run
Local HTML (default)
```bash
python main.py --html index.html
```
Web URL
```bash
python main.py --html https://example.com
```
Disable GPU acceleration (helpful if you see flicker/blank redraws)
```bash
python main.py --html index.html --gpu disable
```
### 🛠️ Build a single-file executable (local HTML)

Quick build via script
```bash
python build.py
```
Manual PyInstaller examples
Windows

```bash
pyinstaller --onefile --windowed --add-data "index.html;." main.py
```
Linux/macOS

```bash
pyinstaller --onefile --windowed --add-data "index.html:." main.py
```
If your HTML uses assets (images/audio/js), add them via additional --add-data entries.

## ⚠️ Project status
Archived — feature-complete for its intended purpose.
Kept as a portable wrapper pattern for HTML games/web apps.

📜 License
Unlicensed (personal archive).
