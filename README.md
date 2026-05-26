# M3U8 to MP4 Smart Converter / M3U8至MP4智能转换器

A simple and elegant Tkinter GUI tool to convert M3U8 to MP4 using FFmpeg. Supports both Express (Stream Copy) and Compatibility (Re-encoding) modes.
一个基于 Python Tkinter 的 M3U8 转 MP4 图形界面工具。支持极速流复制与高兼容性重编码双模式。

---

## 📋 Prerequisites / 前置条件

This tool relies on **FFmpeg** to process video streams. You must have FFmpeg installed and added to your system's PATH before running the application.
本工具的核心转换功能依赖 **FFmpeg**。在运行本软件前，请确保您的电脑已安装 FFmpeg 并已配置好系统环境变量（PATH）。

### How to Install FFmpeg (Windows) / 如何安装配置 FFmpeg
1. **Download / 下载:** Go to [Gyan.dev](https://www.gyan.dev/ffmpeg/builds/) or [BogoToBogo](https://www.bogotobogo.com/FFmpeg/ffmpeg_gadigital_builds.php) to download the standard FFmpeg essentials build (zip format).
   前往 FFmpeg 官网或信任源下载适用于 Windows 的压缩包。
2. **Extract / 解压:** Extract the zip file and move the folders to a safe place (e.g., `C:\ffmpeg`).
   将压缩包解压，把解压出来的文件夹放到一个不易被删的位置（例如 `C:\ffmpeg`）。
3. **Environment Path / 配置环境变量:**
   - Search for "Edit the system environment variables" in Windows search.
   - Click "Environment Variables...", find `Path` under User/System variables, and click "Edit".
   - Click "New" and add the path to the `bin` folder (e.g., `C:\ffmpeg\bin`).
   - 在 Windows 搜索栏输入“编辑系统环境变量”，点击“环境变量”按钮。在系统变量中找到 `Path` 并双击，点击“新建”，将 FFmpeg 文件夹下的 `bin` 目录路径（如 `C:\ffmpeg\bin`）添加进去。
4. **Verify / 验证:** Open Command Prompt (CMD) or PowerShell, type `ffmpeg -version` and press Enter. If it displays version info, you are good to go!
   打开 CMD 或 PowerShell，输入 `ffmpeg -version`。若能正常输出版本号，即代表配置成功！

---

## 🚀 How to use / 如何使用

1. Download the compiled standalone executable from the [Releases](https://github.com/GeorgeSmith215/m3u8-to-mp4/releases/tag/v1.0.0) page.
   从 [Releases](https://github.com/GeorgeSmith215/m3u8-to-mp4/releases/tag/v1.0.0) 页面下载编译好的独立运行程序 `m3u8-to-mp4.exe`。
2. Double-click to run `m3u8-to-mp4.exe`.
   直接双击运行 `m3u8-to-mp4.exe`。
3. Paste a network M3U8 URL or click "Browse" to select a local `.m3u8` file.
   粘贴网络 M3U8 链接，或点击按钮浏览并选择本地的 `.m3u8` 文件。
4. Choose an output directory and click **Start Conversion**.
   选择输出 MP4 的保存位置，点击**开始转换**即可。

> **💡 Mode Explanation / 模式说明:**
> - **Express Mode (Default / 默认极速模式):** Stream copy without re-encoding. Extremely fast (takes only a few seconds) and zero quality loss.
>   直接复制音视频流，不重新编码。速度极快（仅需几秒），且画面完全无损。
> - **Compatibility Mode (兼容模式):** Re-encodes video to standard H.264+AAC. Use this if the output video from Express Mode cannot be seeked, has audio sync issues, or cannot play on mobile devices.
>   将视频重新编码为万能的 H.264+AAC 格式。如果极速模式转出来的视频在手机上打不开、无法快进或音画不同步，请勾选此模式。

---

## 📸 Preview / 预览

### English Interface / 英文界面
![en](./images/en.png)

### Chinese Interface / 中文界面
![cn](./images/cn.png)