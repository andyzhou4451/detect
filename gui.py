import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk, ImageDraw
import cv2
import numpy as np

import predict
import detectX3

IMG_DIR = 'img'
OUT_DIR = 'img_out'
TXT_DIR = os.path.join('样例', 'txt_out')

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('卫星图像处理系统')
        self.geometry('1000x600')

        self.img_path = None
        self.txt_path = None

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.columnconfigure(2, weight=2)
        self.rowconfigure(0, weight=1)

        self.ctrl_panel = ttk.LabelFrame(self, text='控制面板')
        self.ctrl_panel.grid(row=0, column=0, sticky='nswe', padx=5, pady=5)
        self.ctrl_panel.columnconfigure(0, weight=1)

        self.btn_load_img = ttk.Button(self.ctrl_panel, text='加载图像', command=self.load_image)
        self.btn_load_img.grid(row=0, column=0, pady=5, sticky='ew')

        self.btn_load_coord = ttk.Button(self.ctrl_panel, text='加载坐标', command=self.load_coord)
        self.btn_load_coord.grid(row=1, column=0, pady=5, sticky='ew')

        ttk.Label(self.ctrl_panel, text='坐标类型').grid(row=2, column=0, pady=(5,0), sticky='w')
        self.dd_coord = ttk.Combobox(self.ctrl_panel, values=['默认'])
        self.dd_coord.current(0)
        self.dd_coord.grid(row=3, column=0, sticky='ew')

        self.btn_seg = ttk.Button(self.ctrl_panel, text='U-Net分割', command=self.run_predict)
        self.btn_seg.grid(row=4, column=0, pady=5, sticky='ew')

        self.btn_detect = ttk.Button(self.ctrl_panel, text='坐标检测', command=self.run_detect)
        self.btn_detect.grid(row=5, column=0, pady=5, sticky='ew')

        self.status_var = tk.StringVar(value='就绪')
        self.status = ttk.Label(self.ctrl_panel, textvariable=self.status_var)
        self.status.grid(row=6, column=0, pady=5)

        self.progress = ttk.Progressbar(self.ctrl_panel, mode='indeterminate')
        self.progress.grid(row=7, column=0, pady=5, sticky='ew')

        self.canvas_orig = ttk.Label(self)
        self.canvas_orig.grid(row=0, column=1, sticky='nsew')

        self.canvas_res = ttk.Label(self)
        self.canvas_res.grid(row=0, column=2, sticky='nsew')

    def set_status(self, text, color='black'):
        self.status_var.set(text)
        self.status.configure(foreground=color)
        self.update_idletasks()

    def load_image(self):
        filetypes = [('Images','*.jpg *.png *.jpeg *.bmp *.tif')]
        fname = filedialog.askopenfilename(initialdir=IMG_DIR, filetypes=filetypes)
        if not fname:
            return
        self.img_path = fname
        # try to locate matching coordinate file
        base = os.path.basename(fname)
        possible_txt = os.path.join(TXT_DIR, f"{os.path.splitext(base)[0]}.txt")
        if os.path.exists(possible_txt):
            self.txt_path = possible_txt
            self.set_status('图像和坐标已加载', 'green')
        else:
            self.txt_path = None
            self.set_status('图像已加载', 'green')
        img = Image.open(fname)
        self.orig_img = ImageTk.PhotoImage(img)
        self.canvas_orig.config(image=self.orig_img)

    def load_coord(self):
        fname = filedialog.askopenfilename(initialdir=TXT_DIR, filetypes=[('TXT','*.txt')])
        if not fname:
            return
        self.txt_path = fname
        self.set_status('坐标已加载', 'green')

    def run_predict(self):
        if not self.img_path:
            messagebox.showwarning('提示', '请先加载图像')
            return
        basename = os.path.basename(self.img_path)
        out_path = os.path.join(OUT_DIR, basename)
        self.set_status('分割中...', 'orange')
        self.progress.start()
        self.update_idletasks()
        predict.process_image(self.img_path, out_path)
        self.progress.stop()
        img = Image.open(out_path)
        self.pred_img = ImageTk.PhotoImage(img)
        self.canvas_res.config(image=self.pred_img)
        self.set_status('分割完成', 'green')

    def run_detect(self):
        if not self.img_path:
            messagebox.showwarning('提示', '请先加载图像')
            return
        if not self.txt_path:
            base = os.path.basename(self.img_path)
            auto_txt = os.path.join(TXT_DIR, f"{os.path.splitext(base)[0]}.txt")
            if os.path.exists(auto_txt):
                self.txt_path = auto_txt
            else:
                messagebox.showwarning('提示', '未找到对应坐标文件')
                return
        basename = os.path.basename(self.img_path)
        out_path = os.path.join(OUT_DIR, basename)
        self.set_status('检测中...', 'orange')
        self.progress.start()
        self.update_idletasks()
        coords_x, coords_y = detectX3.process_image(out_path, self.txt_path)
        self.progress.stop()
        img = Image.open(out_path)
        draw = ImageDraw.Draw(img)
        data = detectX3.loadtxtmethod(self.txt_path)
        b, c, d, a, e, f = data[0], data[1], data[2], data[3], data[4], data[5]
        w, h = img.size
        draw.text((5,5), f"{d:.4f},{c:.4f}", fill='white')
        draw.text((w-150,5), f"{d:.4f},{a:.4f}", fill='white')
        draw.text((5,h-20), f"{b:.4f},{c:.4f}", fill='white')
        draw.text((w-150,h-20), f"{b:.4f},{a:.4f}", fill='white')
        self.det_img = ImageTk.PhotoImage(img)
        self.canvas_res.config(image=self.det_img)
        self.set_status('检测完成', 'green')

if __name__ == '__main__':
    app = App()
    app.mainloop()
