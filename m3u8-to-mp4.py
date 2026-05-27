import os
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class M3u8ConverterApp:

    def __init__(self, root):
        self.root = root
        self.root.geometry("720x580")

        # 核心控制变量
        self.is_batch_mode = tk.BooleanVar(value=False)
        self.is_compatible_mode = tk.BooleanVar(value=False)
        self.is_english = tk.BooleanVar(value=False)

        # 路径变量
        self.input_path = tk.StringVar()  # 单任务：存储URL/单文件；批量任务：存储选中的父文件夹路径
        self.output_path = tk.StringVar()  # 单任务：存储MP4路径；批量任务：存储输出的父文件夹路径

        # 批量模式专用数据流
        self.selected_folders = []
        self.current_process = None
        self.is_running = False

        # 语言字典配置
        self.lang_pack = {
            "zh": {
                "title": "M3U8 至 MP4 智能转换器",
                "label_in_single": " 1. 输入 M3U8 地址 (支持本地文件或网络链接) ",
                "label_in_batch": " 1. 选择包含多个视频的【父文件夹】 (将自动扫描子目录) ",
                "btn_browse_in_single": "浏览本地文件",
                "btn_browse_in_batch": "选择父文件夹",
                "label_out_single": " 2. 输出 MP4 保存路径 ",
                "label_out_batch": " 2. 输出 MP4 父级保存路径 ",
                "btn_browse_out_single": "选择保存位置",
                "btn_browse_out_batch": "更改保存位置",
                "cb_batch": "启用批量父文件夹扫描模式",
                "cb_compat": "启用兼容性模式 (视频重编码，解决无法快进/音画不同步，速度较慢)",
                "cb_lang": "Show English Interface (显示英文界面)",
                "btn_start_single": "开始转换",
                "btn_start_batch": "开始批量扫描并转换",
                "btn_running": "正在转换中...",
                "label_log": " 3. 转换日志实时输出 ",
                "tip_missing_single": "请先填写输入地址和保存路径！",
                "tip_missing_batch": "请先选择输入的父文件夹！",
                "msg_local": "检测到本地 M3U8 文件，正在解析...\n",
                "msg_compat_on": "已启用【兼容性重新编码模式】...\n",
                "msg_fast_on": "已启用【极速流复制模式】...\n",
                "msg_success_single": "视频成功转换并保存至：\n",
                "msg_success_batch": "批量转换完成！\n找到有效任务: {} 个，成功: {} 个, 失败: {} 个",
                "msg_failed_single": "转换失败，请检查下方日志输出或输入路径是否正确。",
                "msg_failed_search": "在文件夹 '{}' 中未找到对应的 .m3u8 索引文件，跳过。\n",
                "msg_scan_summary": "🔍 扫描完成：在父目录下找到 {} 个有效的 M3U8 视频文件夹。\n",
                "msg_error": "运行中遭遇程序异常:\n",
                "file_m3u8": "M3U8 文件",
                "file_all": "所有文件",
                "file_mp4": "MP4 视频",
                "box_tip": "提示",
                "box_success": "成功",
                "box_failed": "错误",
                "box_error": "异常",
                "box_info": "完成",
            },
            "en": {
                "title": "M3U8 to MP4 Smart Converter",
                "label_in_single": " 1. Input M3U8 Address (Supports Local File or URL) ",
                "label_in_batch": " 1. Select 【Parent Folder】 (Will automatically scan sub-directories) ",
                "btn_browse_in_single": "Browse Local",
                "btn_browse_in_batch": "Select Parent Folder",
                "label_out_single": " 2. Output MP4 Save Path ",
                "label_out_batch": " 2. Output MP4 Parent Directory ",
                "btn_browse_out_single": "Save As...",
                "btn_browse_out_batch": "Change Location",
                "cb_batch": "Enable Parent Folder Batch Scan Mode",
                "cb_compat": "Enable Compatibility Mode (Re-encoding, fixes seek issue/sync, slower)",
                "cb_lang": "Show Chinese Interface (显示中文界面)",
                "btn_start_single": "Start Conversion",
                "btn_start_batch": "Start Batch Scan & Convert",
                "btn_running": "Converting...",
                "label_log": " 3. Real-time Conversion Log ",
                "tip_missing_single": "Please fill in both input address and output path first!",
                "tip_missing_batch": "Please select the input parent folder first!",
                "msg_local": "Local M3U8 file detected, parsing...\n",
                "msg_compat_on": "Enabled [Compatibility Re-encoding Mode]...\n",
                "msg_fast_on": "Enabled [Express Stream Copy Mode]...\n",
                "msg_success_single": "Video successfully converted and saved to:\n",
                "msg_success_batch": "Batch conversion completed!\nValid Tasks: {}, Success: {}, Failed: {}",
                "msg_failed_single": "Conversion failed. Please check the log or paths.",
                "msg_failed_search": "No matching .m3u8 file found for folder '{}', skipped.\n",
                "msg_scan_summary": "🔍 Scan complete: Found {} valid M3U8 video folders under parent directory.\n",
                "msg_error": "An exception occurred during execution:\n",
                "file_m3u8": "M3U8 Files",
                "file_all": "All Files",
                "file_mp4": "MP4 Video",
                "box_tip": "Tip",
                "box_success": "Success",
                "box_failed": "Error",
                "box_error": "Exception",
                "box_info": "Done",
            },
        }

        self.create_widgets()
        self.toggle_mode()
        self.update_ui_language()

    def create_widgets(self):
        # 顶部选项栏（语言 & 批量模式切换）
        frame_top_opt = tk.Frame(self.root)
        frame_top_opt.pack(fill="x", padx=15, pady=(10, 0))

        self.cb_batch = tk.Checkbutton(
            frame_top_opt, text="", variable=self.is_batch_mode,
            font=("Segoe UI", 9, "bold"), fg="#28a745", command=self.toggle_mode
        )
        self.cb_batch.pack(side="left")

        self.cb_lang = tk.Checkbutton(
            frame_top_opt, text="", variable=self.is_english,
            font=("Segoe UI", 9, "bold"), fg="#0056b3", command=self.update_ui_language
        )
        self.cb_lang.pack(side="right")

        # 1. 输入区域
        self.frame_input = ttk.LabelFrame(self.root, text="")
        self.frame_input.pack(fill="x", padx=15, pady=6)

        self.entry_input = tk.Entry(self.frame_input, textvariable=self.input_path, font=("Segoe UI", 10))
        self.entry_input.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        self.btn_browse_in = tk.Button(self.frame_input, text="", command=self.handle_input_browse)
        self.btn_browse_in.pack(side="right", padx=5, pady=5)

        # 2. 输出区域
        self.frame_output = ttk.LabelFrame(self.root, text="")
        self.frame_output.pack(fill="x", padx=15, pady=6)

        entry_output = tk.Entry(self.frame_output, textvariable=self.output_path, font=("Segoe UI", 10))
        entry_output.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        self.btn_browse_out = tk.Button(self.frame_output, text="", command=self.handle_output_browse)
        self.btn_browse_out.pack(side="right", padx=5, pady=5)

        # 3. 模式选择与控制区域
        frame_ctrl = tk.Frame(self.root)
        frame_ctrl.pack(fill="x", padx=15, pady=8)

        self.cb_compatible = tk.Checkbutton(
            frame_ctrl, text="", variable=self.is_compatible_mode,
            font=("Segoe UI", 9), anchor="w"
        )
        self.cb_compatible.pack(fill="x", pady=(0, 6))

        self.btn_start = tk.Button(
            frame_ctrl, text="", bg="#28a745", fg="white",
            font=("Segoe UI", 10, "bold"), command=self.start_conversion_thread
        )
        self.btn_start.pack(fill="x", ipady=6)

        # 4. 日志输出区域
        self.frame_log = ttk.LabelFrame(self.root, text="")
        self.frame_log.pack(fill="both", expand=True, padx=15, pady=6)

        self.log_text = tk.Text(
            self.frame_log, wrap="word", height=12,
            font=("Consolas", 9), bg="#1e1e1e", fg="#d4d4d4"
        )
        self.log_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        scrollbar = tk.Scrollbar(self.frame_log, command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y", pady=5)
        self.log_text.config(yscrollcommand=scrollbar.set)

    def get_current_lang(self):
        return self.lang_pack["en" if self.is_english.get() else "zh"]

    def toggle_mode(self):
        """处理批量模式和单文件/URL模式的输入框硬切换"""
        self.input_path.set("")
        self.output_path.set("")
        self.selected_folders = []

        if self.is_batch_mode.get():
            self.entry_input.config(state="readonly")  # 批量时不允许手动乱打字，必须点按钮选目录
        else:
            self.entry_input.config(state="normal")

        self.update_ui_language()

    def update_ui_language(self):
        l = self.get_current_lang()
        self.root.title(l["title"])
        self.cb_batch.config(text=l["cb_batch"])
        self.cb_lang.config(text=l["cb_lang"])
        self.cb_compatible.config(text=l["cb_compat"])
        self.frame_log.config(text=l["label_log"])

        if self.is_batch_mode.get():
            self.frame_input.config(text=l["label_in_batch"])
            self.btn_browse_in.config(text=l["btn_browse_in_batch"])
            self.frame_output.config(text=l["label_out_batch"])
            self.btn_browse_out.config(text=l["btn_browse_out_batch"])
            if not self.is_running:
                self.btn_start.config(text=l["btn_start_batch"])
        else:
            self.frame_input.config(text=l["label_in_single"])
            self.btn_browse_in.config(text=l["btn_browse_in_single"])
            self.frame_output.config(text=l["label_out_single"])
            self.btn_browse_out.config(text=l["btn_browse_out_single"])
            if not self.is_running:
                self.btn_start.config(text=l["btn_start_single"])

        if self.is_running:
            self.btn_start.config(text=l["btn_running"])

    def handle_input_browse(self):
        l = self.get_current_lang()
        if self.is_batch_mode.get():
            # 批量模式：直接干净利落地选择一个大父目录
            parent_dir = filedialog.askdirectory(title="选择包含多个视频文件夹的【总父文件夹】")
            if parent_dir:
                norm_parent = os.path.normpath(parent_dir)
                self.input_path.set(norm_parent)
                # 默认输出目标也定为这个父目录（输出的mp4文件会和各个视频文件夹并排躺在一起）
                self.output_path.set(norm_parent)
        else:
            # 单任务模式：选择单个文件
            file_path = filedialog.askopenfilename(
                filetypes=[(l["file_m3u8"], "*.m3u8"), (l["file_all"], "*.*")]
            )
            if file_path:
                norm_path = os.path.normpath(file_path)
                self.input_path.set(norm_path)
                self.output_path.set(os.path.join(os.path.dirname(norm_path), "output.mp4"))

    def handle_output_browse(self):
        l = self.get_current_lang()
        if self.is_batch_mode.get():
            dir_path = filedialog.askdirectory()
            if dir_path:
                self.output_path.set(os.path.normpath(dir_path))
        else:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".mp4", filetypes=[(l["file_mp4"], "*.mp4")], initialfile="output.mp4"
            )
            if file_path:
                self.output_path.set(os.path.normpath(file_path))

    def log(self, message):
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)

    def start_conversion_thread(self):
        l = self.get_current_lang()

        if self.is_batch_mode.get():
            if not self.input_path.get().strip() or not self.output_path.get().strip():
                messagebox.showwarning(l["box_tip"], l["tip_missing_batch"])
                return
            target_func = self.batch_process
        else:
            if not self.input_path.get().strip() or not self.output_path.get().strip():
                messagebox.showwarning(l["box_tip"], l["tip_missing_single"])
                return
            target_func = self.single_process

        self.is_running = True
        self.btn_start.config(state="disabled", text=l["btn_running"], bg="#6c757d")
        self.log_text.delete("1.0", tk.END)

        threading.Thread(target=target_func, daemon=True).start()

    def single_process(self):
        l = self.get_current_lang()
        infile = self.input_path.get().strip()
        outfile = self.output_path.get().strip()

        cmd = [
            "ffmpeg", "-y", "-allowed_extensions", "ALL",
            "-protocol_whitelist", "file,http,https,tls,tcp,crypto",
            "-i", infile
        ]

        if self.is_compatible_mode.get():
            self.root.after(0, self.log, l["msg_compat_on"])
            cmd.extend(["-c:v", "libx264", "-c:a", "aac", "-bsf:a", "aac_adtstoasc", "-pix_fmt", "yuv420p"])
        else:
            self.root.after(0, self.log, l["msg_fast_on"])
            cmd.extend(["-c:v", "copy", "-c:a", "copy", "-bsf:a", "aac_adtstoasc"])

        cmd.append(outfile)

        try:
            if os.path.isfile(infile):
                self.root.after(0, self.log, l["msg_local"])

            self.root.after(0, self.log, f"执行命令: {' '.join(cmd)}\n\n" + "-" * 50 + "\n")

            self.current_process = subprocess.Popen(
                cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                universal_newlines=True, encoding="utf-8", errors="ignore",
                creationflags=subprocess.CREATE_NO_WINDOW
            )

            while True:
                line = self.current_process.stdout.readline()
                if not line: break
                self.root.after(0, self.log, line)

            self.current_process.wait()
            if self.current_process.returncode == 0:
                self.root.after(0, lambda: messagebox.showinfo(l["box_success"], f"{l['msg_success_single']}{outfile}"))
            else:
                self.root.after(0, lambda: messagebox.showerror(l["box_failed"], l["msg_failed_single"]))
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror(l["box_error"], f"{l['msg_error']}{str(e)}"))
        finally:
            self.root.after(0, self.reset_ui)

    def find_m3u8_file(self, folder_path):
        """核心智能查找：判定这个子文件夹是不是包含 M3U8 的标准结构"""
        folder_name = os.path.basename(folder_path)
        parent_dir = os.path.dirname(folder_path)

        # 模式 1：检查同级是否有“子文件夹名.m3u8”
        p1 = os.path.join(parent_dir, f"{folder_name}.m3u8")
        if os.path.exists(p1): return p1

        # 模式 2：进入子文件夹内，找任意存在的以 .m3u8 结尾的文件
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            try:
                for f in os.listdir(folder_path):
                    if f.lower().endswith(".m3u8"):
                        return os.path.join(folder_path, f)
            except Exception:
                pass
        return None

    def batch_process(self):
        """核心重构：一键深度扫描父目录并自动提取合法任务"""
        l = self.get_current_lang()
        scan_parent = self.input_path.get().strip()
        out_parent = self.output_path.get().strip()

        # 1. 扫描第一层子目录
        self.selected_folders = []
        if os.path.exists(scan_parent) and os.path.isdir(scan_parent):
            for entry in os.listdir(scan_parent):
                full_sub_path = os.path.join(scan_parent, entry)
                if os.path.isdir(full_sub_path):
                    # 只有当这个子文件夹满足 M3U8 视频特征（内含或同名存在m3u8）时，才抓进队列
                    if self.find_m3u8_file(full_sub_path):
                        self.selected_folders.append(full_sub_path)

        total_tasks = len(self.selected_folders)
        self.root.after(0, self.log, l["msg_scan_summary"].format(total_tasks))

        success_count, fail_count = 0, 0

        # 2. 队列执行转换循环
        for idx, folder in enumerate(self.selected_folders):
            folder_name = os.path.basename(folder)
            self.root.after(0, self.log, f"\n[任务 {idx + 1}/{total_tasks}] 正在处理子目录: {folder_name}\n")

            m3u8_file = self.find_m3u8_file(folder)
            output_mp4_path = os.path.join(out_parent, f"{folder_name}.mp4")

            cmd = [
                "ffmpeg", "-y", "-allowed_extensions", "ALL",
                "-protocol_whitelist", "file,http,https,tls,tcp,crypto",
                "-i", m3u8_file
            ]

            if self.is_compatible_mode.get():
                cmd.extend(["-c:v", "libx264", "-c:a", "aac", "-bsf:a", "aac_adtstoasc", "-pix_fmt", "yuv420p"])
            else:
                cmd.extend(["-c:v", "copy", "-c:a", "copy", "-bsf:a", "aac_adtstoasc"])
            cmd.append(output_mp4_path)

            try:
                self.current_process = subprocess.Popen(
                    cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                    universal_newlines=True, encoding="utf-8", errors="ignore",
                    creationflags=subprocess.CREATE_NO_WINDOW
                )

                while True:
                    line = self.current_process.stdout.readline()
                    if not line: break
                    # 稀释输出，防止批量跑上百个任务时频繁修改DOM导致UI雪崩卡死
                    if "frame=" in line or "time=" in line:
                        if idx % 6 == 0: self.root.after(0, self.log, line)
                    else:
                        self.root.after(0, self.log, line)

                self.current_process.wait()
                if self.current_process.returncode == 0:
                    self.root.after(0, self.log, f"📈 转换成功 -> {output_mp4_path}\n")
                    success_count += 1
                else:
                    self.root.after(0, self.log, f"❌ FFmpeg 执行失败。\n")
                    fail_count += 1
            except Exception as e:
                self.root.after(0, self.log, f"💥 捕获异常: {str(e)}\n")
                fail_count += 1

        # 3. 汇总报告弹窗
        self.root.after(0, lambda: self.post_batch_feedback(total_tasks, success_count, fail_count))

    def post_batch_feedback(self, total, success, fail):
        l = self.get_current_lang()
        self.reset_ui()
        messagebox.showinfo(l["box_info"], l["msg_success_all"].format(total, success, fail))

    def reset_ui(self):
        self.is_running = False
        self.update_ui_language()
        self.btn_start.config(state="normal", bg="#28a745")


if __name__ == "__main__":
    root = tk.Tk()
    app = M3u8ConverterApp(root)
    root.mainloop()