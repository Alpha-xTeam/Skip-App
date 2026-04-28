# SKIP - YouTube Downloader 🚀

A modern, high-performance YouTube downloader with a clean, minimalist aesthetic. Built with Python and CustomTkinter.

## ✨ Features

### 1. Modern Minimalist UI
- **Clean Slate Design**: Deep slate backgrounds with high-contrast Sky Blue accents.
- **Side-Bar Navigation**: A professional, dashboard-like experience.
- **Fluid Layout**: Responsive components using CustomTkinter.

### 2. Smart Functionality
- **Smart Clipboard**: Automatically detects and pastes YouTube links from your clipboard.
- **Robust Download History**: Keep track of your downloads with a built-in library.
- **Smart Playback**: Play downloaded files directly from the app, with automatic path and filename correction for Windows.

### 3. High-Performance Core
- **Async Downloads**: Non-blocking downloads using `yt-dlp` and threading.
- **Quality Multiplexing**: Choose between Video (MP4) and Audio (MP3) with dynamic quality options.
- **Bundled FFmpeg**: Ready to use without complex system setups.

## 📂 Project Structure
```text
Skip/
├── src/
│   ├── app.py           # Application Entry Point
│   ├── core/            # Business Logic (yt-dlp wrapper)
│   ├── gui/             # UI Components & Main Window
│   │   └── styles.py    # Design System & Themes
│   └── config/          # History and settings storage
├── main.py              # Root Redirect
├── requirements.txt     # Dependencies
├── build_exe.py         # PyInstaller build script
└── SkipDownloader.spec  # PyInstaller spec file
```

## 🛠️ Installation & Usage

### Running from Source
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python main.py
   ```

### Building the Executable
To compile the application into a standalone `.exe`:
```bash
python build_exe.py
```
The output will be located in the `dist/` folder.
