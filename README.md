# M3U8 to MP4 Smart Converter / M3U8至MP4智能转换器

A simple and elegant Tkinter GUI tool to convert M3U8 to MP4 using FFmpeg. Supports both Express (Stream Copy) and Compatibility (Re-encoding) modes, with powerful single/batch dual-mode processing capability.  
一个基于 Python Tkinter 的 M3U8 转 MP4 图形界面工具。支持极速流复制与高兼容性重编码双模式，兼具单任务（链接/单文件）与一键批量目录扫描转换功能。

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

## 🚀 How to Use / 如何使用

### Mode 1: Single Task Mode / 模式一：单任务模式（默认）
1. Paste a network M3U8 URL or click **"Browse Local File" / "浏览本地文件"** to select a local `.m3u8` index file.  
   粘贴网络 M3U8 链接，或点击按钮浏览并选择本地单个 `.m3u8` 文件。
2. Choose an output directory for MP4 and click **"Start Conversion" / "开始转换"**.  
   选择输出 MP4 的保存位置与文件名，点击按钮即可开始转换。

### Mode 2: Batch Folder Mode / 模式二：批量父文件夹扫描模式
1. Check the box **"Enable Parent Folder Batch Scan Mode" / "启用批量父文件夹扫描模式"**.  
   勾选顶部的 **“启用批量父文件夹扫描模式”**。
2. Click **"Select Parent Folder" / "选择父文件夹"** to pick the root directory containing your video segments.   
   点击按钮选择包含多个视频子目录的**“总父文件夹”**。程序将自动在后台智能扫描其第一层子目录。
3. The output directory defaults to the selected parent folder (exported MP4 files will be named after their corresponding sub-folders). Click **"Start Batch Scan & Convert" / "开始批量扫描并转换"**.  
   输出保存路径默认与输入的父文件夹一致（转出的 MP4 将自动以各子文件夹命名且并排放置）。点击按钮一键排队转换。

---

## 💡 Folder Structure Guide / 目录结构规范

For **Batch Mode**, the tool smartly scans the selected parent folder and automatically filters valid targets. It matches files conforming to any of the following structures:  
在**批量模式**下，程序会自动深度检索选中的总父文件夹，并自动过滤掉不相关的多余目录。只要子目录满足以下任意一种常见的 HLS 本地缓存格式，即可被精准识别并排队处理：

* **Structure A (Co-located Index) / 结构 A（外部同名索引并排）:**
```text
    📁 My_Videos_Parent (Selected / 选中的总父文件夹)
    ├── 📄 Video_01.m3u8 (Index / 索引)
    ├── 📁 Video_01      (Folder with .ts segments / 包含切片的同名文件夹)
    ├── 📄 Video_02.m3u8
    └── 📁 Video_02
 ```

* **Structure B (Internal Index) / 结构 B（内部嵌套浅层索引）:**
```text
    📁 My_Videos_Parent (Selected / 选中的总父文件夹)
    ├── 📁 Video_01
    │   ├── 📄 index.m3u8 (Or any .m3u8 file / 或任意.m3u8文件)
    │   └── 📄 segment0.ts, segment1.ts ...
    └── 📁 Video_02
        ├── 📄 play.m3u8
        └── 📄 0.ts, 1.ts ...
 ```

* **Structure C (Standalone Big-Box Wrapper) / 结构 C（独立大盒子两层套娃 - 常见于手机浏览器/手机APP下载缓存）:**
  *Each video project has an exclusive "Parent Box" folder, inside which contains both the `.m3u8` index and an identical folder for `.ts` segments. In this case, simply select the ultimate top parent directory.*  
  *每个视频项目被一个独立的“大盒子文件夹”包裹，大盒子内部同时存放了 `.m3u8` 索引以及一个专门用来存放 `.ts` 切片的同名文件夹（无三级嵌套）。在这种结构下，**操作时直接选择最外层的总总父文件夹即可实现一键全部批量转换**。*
```text
    📁 QuarkDownloads (Selected / 选中的总总父文件夹)
    ├── 📁 Video_Project_A (Big Box / 大盒子文件夹)
    │   ├── 📄 MovieA.m3u8  (Index / 索引)
    │   └── 📁 MovieA       (Identical folder name / 同名文件夹)
    │       └── 📄 0.ts, 1.ts, 2.ts ... (Segments / 切片直接躺在这里)
    └── 📁 Video_Project_B (Big Box / 大盒子文件夹)
        ├── 📄 MovieB.m3u8
        └── 📁 MovieB
            └── 📄 0.ts, 1.ts ...
 ```

---

## 🛠️ Mode Explanation / 转换模式说明

* **Express Mode (Default / 默认极速模式):** Stream copy without re-encoding. Extremely fast (takes only a few seconds) and zero quality loss.
    直接复制音视频流，不重新编码。速度极快（仅需几秒），且画面完全无损。
* **Compatibility Mode (兼容模式):** Re-encodes video to standard H.264+AAC. Use this if the output video from Express Mode cannot be seeked, has audio sync issues, or cannot play on mobile devices.
    将视频重新编码为万能的 H.264+AAC 格式。如果极速模式转出来的视频在手机上打不开、无法快进或音画不同步，请勾选此模式。

---

## 📸 Preview / 预览

### English Interface / 英文界面
![en](./images/en.png)

### Chinese Interface / 中文界面
![cn](./images/cn.png)