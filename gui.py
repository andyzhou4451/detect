import os
import tkinter as tk

from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import cv2
import numpy as np

import predict
import detectX3

IMG_DIR = 'img'
OUT_DIR = 'img_out'

TXT_DIR = 'txt_out'


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('卫星图像处理系统')
        self.geometry('1000x600')

        self.img_path = None
        self.txt_path = None

        self.ctrl_panel = tk.Frame(self, width=200)
        self.ctrl_panel.pack(side='left', fill='y')

        self.btn_load_img = tk.Button(self.ctrl_panel, text='加载图像', command=self.load_image)
        self.btn_load_img.pack(pady=5)

        self.btn_load_coord = tk.Button(self.ctrl_panel, text='加载坐标', command=self.load_coord)
        self.btn_load_coord.pack(pady=5)

        self.btn_seg = tk.Button(self.ctrl_panel, text='U-Net分割', command=self.run_predict)
        self.btn_seg.pack(pady=5)

        self.btn_detect = tk.Button(self.ctrl_panel, text='坐标检测', command=self.run_detect)
        self.btn_detect.pack(pady=5)

        self.status = tk.Label(self.ctrl_panel, text='就绪')
        self.status.pack(pady=5)

        self.canvas_orig = tk.Label(self)
        self.canvas_orig.pack(side='left', expand=True)

        self.canvas_res = tk.Label(self)
        self.canvas_res.pack(side='right', expand=True)

    def set_status(self, text):
        self.status.config(text=text)

        self.update_idletasks()

    def load_image(self):
        filetypes = [('Images','*.jpg *.png *.jpeg *.bmp *.tif')]
        fname = filedialog.askopenfilename(initialdir=IMG_DIR, filetypes=filetypes)
        if not fname:
            return
        self.img_path = fname

        img = Image.open(fname)
        self.orig_img = ImageTk.PhotoImage(img)
        self.canvas_orig.config(image=self.orig_img)
        self.set_status('图像已加载')


    def load_coord(self):
        fname = filedialog.askopenfilename(initialdir=TXT_DIR, filetypes=[('TXT','*.txt')])
        if not fname:
            return
        self.txt_path = fname

        self.set_status('坐标已加载')


    def run_predict(self):
        if not self.img_path:
            messagebox.showwarning('提示', '请先加载图像')
            return
        basename = os.path.basename(self.img_path)
        out_path = os.path.join(OUT_DIR, basename)

        predict.process_image(self.img_path, out_path)
        img = Image.open(out_path)
        self.pred_img = ImageTk.PhotoImage(img)
        self.canvas_res.config(image=self.pred_img)
        self.set_status('分割完成')

    def run_detect(self):
        if not self.img_path or not self.txt_path:
            messagebox.showwarning('提示', '请先加载图像和坐标')
            return
        basename = os.path.basename(self.img_path)
        out_path = os.path.join(OUT_DIR, basename)
        coords_x, coords_y = detectX3.process_image(out_path, self.txt_path)

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

        self.set_status('检测完成')


if __name__ == '__main__':
    app = App()
    app.mainloop()
