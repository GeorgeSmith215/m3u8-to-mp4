import os
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class M3u8ConverterApp:

    def __init__(self, root):
        self.root = root
        self.root.geometry("680x520")

        # 变量定义
        self.input_path = tk.StringVar()
        self.output_path = tk.StringVar()
        self.is_compatible_mode = tk.BooleanVar(value=False)
        self.is_english = tk.BooleanVar(value=False)  # 语言控制变量
        self.process = None

        # 语言字典配置
        self.lang_pack = {
            "zh": {
                "title": "M3U8 至 MP4 智能转换器",
                "label_in": " 1. 输入 M3U8 地址 (支持本地文件或网络链接) ",
                "btn_browse_in": "浏览本地文件",
                "label_out": " 2. 输出 MP4 保存路径 ",
                "btn_browse_out": "选择保存位置",
                "cb_compat": "启用兼容性模式 (视频重编码，解决无法快进/音画不同步，速度较慢)",
                "cb_lang": "Show English Interface (显示英文文界面)",
                "btn_start": "开始转换",
                "btn_running": "正在转换中...",
                "label_log": " 3. 转换日志实时输出 ",
                "tip_missing": "请先填写输入地址和保存路径！",
                "msg_local": "检测到本地 M3U8 文件，正在解析...\n",
                "msg_compat_on": "已启用【兼容性重新编码模式】...\n",
                "msg_fast_on": "已启用【极速流复制模式】...\n",
                "msg_success": "视频成功转换并保存至：\n",
                "msg_failed": "转换失败，请检查下方日志输出或输入路径是否正确。",
                "msg_error": "运行中遭遇程序异常:\n",
                "file_m3u8": "M3U8 文件",
                "file_all": "所有文件",
                "file_mp4": "MP4 视频",
                "box_tip": "提示",
                "box_success": "成功",
                "box_failed": "错误",
                "box_error": "异常",
            },
            "en": {
                "title": "M3U8 to MP4 Smart Converter",
                "label_in": " 1. Input M3U8 Address (Supports Local File or URL) ",
                "btn_browse_in": "Browse Local",
                "label_out": " 2. Output MP4 Save Path ",
                "btn_browse_out": "Save As...",
                "cb_compat": "Enable Compatibility Mode (Re-encoding, fixes seek issue/sync, slower)",
                "cb_lang": "Show Chinese Interface (显示中文界面)",
                "btn_start": "Start Conversion",
                "btn_running": "Converting...",
                "label_log": " 3. Real-time Conversion Log ",
                "tip_missing": "Please fill in both input address and output path first!",
                "msg_local": "Local M3U8 file detected, parsing...\n",
                "msg_compat_on": "Enabled [Compatibility Re-encoding Mode]...\n",
                "msg_fast_on": "Enabled [Express Stream Copy Mode]...\n",
                "msg_success": "Video successfully converted and saved to:\n",
                "msg_failed": "Conversion failed. Please check the log or paths.",
                "msg_error": "An exception occurred during execution:\n",
                "file_m3u8": "M3U8 Files",
                "file_all": "All Files",
                "file_mp4": "MP4 Video",
                "box_tip": "Tip",
                "box_success": "Success",
                "box_failed": "Error",
                "box_error": "Exception",
            },
        }

        self.create_widgets()
        self.update_ui_language()  # 初始化语言

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TLabelframe", padding=10)

        # 语言与全局选项栏
        frame_top_opt = tk.Frame(self.root)
        frame_top_opt.pack(fill="x", padx=15, pady=(10, 0))

        self.cb_lang = tk.Checkbutton(
            frame_top_opt,
            text="",
            variable=self.is_english,
            font=("Segoe UI", 9, "bold"),
            fg="#0056b3",
            command=self.update_ui_language,
        )
        self.cb_lang.pack(side="right")

        # 1. 输入区域
        self.frame_input = ttk.LabelFrame(self.root, text="")
        self.frame_input.pack(fill="x", padx=15, pady=6)

        entry_input = tk.Entry(
            self.frame_input, textvariable=self.input_path, font=("Segoe UI", 10)
        )
        entry_input.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        self.btn_browse_in = tk.Button(
            self.frame_input, text="", command=self.browse_m3u8
        )
        self.btn_browse_in.pack(side="right", padx=5, pady=5)

        # 2. 输出区域
        self.frame_output = ttk.LabelFrame(self.root, text="")
        self.frame_output.pack(fill="x", padx=15, pady=6)

        entry_output = tk.Entry(
            self.frame_output, textvariable=self.output_path, font=("Segoe UI", 10)
        )
        entry_output.pack(side="left", fill="x", expand=True, padx=5, pady=5)

        self.btn_browse_out = tk.Button(
            self.frame_output, text="", command=self.browse_output
        )
        self.btn_browse_out.pack(side="right", padx=5, pady=5)

        # 3. 模式选择与控制区域
        frame_ctrl = tk.Frame(self.root)
        frame_ctrl.pack(fill="x", padx=15, pady=8)

        self.cb_compatible = tk.Checkbutton(
            frame_ctrl,
            text="",
            variable=self.is_compatible_mode,
            font=("Segoe UI", 9),
            anchor="w",
        )
        self.cb_compatible.pack(fill="x", pady=(0, 6))

        self.btn_start = tk.Button(
            frame_ctrl,
            text="",
            bg="#28a745",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            command=self.start_conversion_thread,
        )
        self.btn_start.pack(fill="x", ipady=6)

        # 4. 日志输出区域
        self.frame_log = ttk.LabelFrame(self.root, text="")
        self.frame_log.pack(fill="both", expand=True, padx=15, pady=6)

        self.log_text = tk.Text(
            self.frame_log,
            wrap="word",
            height=10,
            font=("Consolas", 9),
            bg="#1e1e1e",
            fg="#d4d4d4",
        )
        self.log_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        scrollbar = tk.Scrollbar(self.frame_log, command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y", pady=5)
        self.log_text.config(yscrollcommand=scrollbar.set)

    def get_current_lang(self):
        return self.lang_pack["en" if self.is_english.get() else "zh"]

    def update_ui_language(self):
        """动态无缝切换中英文标签文本"""
        l = self.get_current_lang()
        self.root.title(l["title"])
        self.cb_lang.config(text=l["cb_lang"])
        self.frame_input.config(text=l["label_in"])
        self.btn_browse_in.config(text=l["btn_browse_in"])
        self.frame_output.config(text=l["label_out"])
        self.btn_browse_out.config(text=l["btn_browse_out"])
        self.cb_compatible.config(text=l["cb_compat"])
        self.frame_log.config(text=l["label_log"])

        if self.btn_start["state"] == "normal":
            self.btn_start.config(text=l["btn_start"])
        else:
            self.btn_start.config(text=l["btn_running"])

    def browse_m3u8(self):
        l = self.get_current_lang()
        file_path = filedialog.askopenfilename(
            filetypes=[(l["file_m3u8"], "*.m3u8"), (l["file_all"], "*.*")]
        )
        if file_path:
            norm_path = os.path.normpath(file_path)
            self.input_path.set(norm_path)
            base_dir = os.path.dirname(norm_path)
            self.output_path.set(os.path.join(base_dir, "output.mp4"))

    def browse_output(self):
        l = self.get_current_lang()
        file_path = filedialog.asksaveasfilename(
            defaultextension=".mp4",
            filetypes=[(l["file_mp4"], "*.mp4")],
            initialfile="output.mp4",
        )
        if file_path:
            self.output_path.set(os.path.normpath(file_path))

    def log(self, message):
        self.log_text.insert(tk.END, message)
        self.log_text.see(tk.END)

    def start_conversion_thread(self):
        l = self.get_current_lang()
        m3u8_val = self.input_path.get().strip()
        mp4_val = self.output_path.get().strip()

        if not m3u8_val or not mp4_val:
            messagebox.showwarning(l["box_tip"], l["tip_missing"])
            return

        self.btn_start.config(state="disabled", text=l["btn_running"], bg="#6c757d")
        self.log_text.delete("1.0", tk.END)

        threading.Thread(
            target=self.run_ffmpeg, args=(m3u8_val, mp4_val), daemon=True
        ).start()

    def run_ffmpeg(self, infile, outfile):
        l = self.get_current_lang()
        cmd = [
            "ffmpeg",
            "-y",
            "-allowed_extensions",
            "ALL",
            "-protocol_whitelist",
            "file,http,https,tls,tcp,crypto",
            "-i",
            infile,
        ]

        if self.is_compatible_mode.get():
            self.root.after(0, self.log, l["msg_compat_on"])
            cmd.extend(
                [
                    "-c:v",
                    "libx264",
                    "-c:a",
                    "aac",
                    "-bsf:a",
                    "aac_adtstoasc",
                    "-pix_fmt",
                    "yuv420p",
                ]
            )
        else:
            self.root.after(0, self.log, l["msg_fast_on"])
            cmd.extend(["-c:v", "copy", "-c:a", "copy", "-bsf:a", "aac_adtstoasc"])

        cmd.append(outfile)

        try:
            if os.path.isfile(infile):
                self.root.after(0, self.log, l["msg_local"])

            self.root.after(
                0, self.log, f"执行命令: {' '.join(cmd)}\n\n" + "-" * 50 + "\n"
            )

            self.process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True,
                encoding="utf-8",
                errors="ignore",
                creationflags=subprocess.CREATE_NO_WINDOW,
            )

            while True:
                line = self.process.stdout.readline()
                if not line:
                    break
                self.root.after(0, self.log, line)

            self.process.wait()

            if self.process.returncode == 0:
                self.root.after(
                    0,
                    lambda: messagebox.showinfo(
                        l["box_success"], f"{l['msg_success']}{outfile}"
                    ),
                )
            else:
                self.root.after(
                    0, lambda: messagebox.showerror(l["box_failed"], l["msg_failed"])
                )

        except Exception as e:
            self.root.after(
                0,
                lambda: messagebox.showerror(
                    l["box_error"], f"{l['msg_error']}{str(e)}"
                ),
            )
        finally:
            self.root.after(0, self.reset_button)

    def reset_button(self):
        l = self.get_current_lang()
        self.btn_start.config(state="normal", text=l["btn_start"], bg="#28a745")


if __name__ == "__main__":
    root = tk.Tk()
    app = M3u8ConverterApp(root)
    root.mainloop()