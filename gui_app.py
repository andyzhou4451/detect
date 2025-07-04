import os
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import cv2
import numpy as np

from unet import Unet

# Small helper to run the detector logic from detectX3.py

def detect_coordinates(img_path, txt_path, output_csv):
    data = np.loadtxt(txt_path, dtype=np.float32, delimiter=',')
    b, c, d, a, e, f = data

    img = cv2.imread(img_path)
    grid_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    grid_hsv = cv2.cvtColor(grid_rgb, cv2.COLOR_RGB2HSV)

    lower1 = np.array([0, 43, 46])
    upper1 = np.array([10, 255, 255])
    mask1 = cv2.inRange(grid_hsv, lower1, upper1)

    lower2 = np.array([156, 43, 46])
    upper2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(grid_hsv, lower2, upper2)

    lower3 = np.array([35, 43, 46])
    upper3 = np.array([77, 255, 255])
    mask3 = cv2.inRange(grid_hsv, lower3, upper3)

    mask4 = mask1 + mask2 + mask3
    xy = np.column_stack(np.where(mask4 == 255))

    coord_x = [c + int(t[1]) * ((a - c) / e) for t in xy]
    coord_y = [d - int(t[0]) * ((d - b) / f) for t in xy]

    with open(output_csv, 'w', encoding='utf8') as csvfile:
        for x, y in zip(coord_x, coord_y):
            csvfile.write(f"{x},{y}\n")

    return list(zip(coord_x, coord_y))


def draw_corner_coords(image, txt_path):
    data = np.loadtxt(txt_path, dtype=np.float32, delimiter=',')
    b, c, d, a, e, f = data

    h, w = image.shape[:2]
    corners = {
        f"({c:.4f},{d:.4f})": (0, 0),
        f"({a:.4f},{d:.4f})": (w - 1, 0),
        f"({c:.4f},{b:.4f})": (0, h - 1),
        f"({a:.4f},{b:.4f})": (w - 1, h - 1),
    }

    for text, pos in corners.items():
        cv2.putText(image, text, pos, cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 0), 1)
    return image


class SatelliteApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("卫星图像处理系统")
        self.geometry("1000x600")

        self.unet = Unet(blend=False)
        self.img_path = None
        self.original_img = None
        self.result_img = None

        self._build_ui()

    def _build_ui(self):
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        ctrl = ttk.Frame(self)
        ctrl.grid(row=0, column=0, sticky="nsw", padx=5, pady=5)
        for i in range(8):
            ctrl.rowconfigure(i, pad=5)

        ttk.Label(ctrl, text="控制面板", font=("Arial", 12, "bold")).grid(row=0, column=0)
        ttk.Button(ctrl, text="加载图像", command=self.load_image).grid(row=1, column=0, sticky="ew")
        ttk.Button(ctrl, text="加载坐标", command=self.load_coord).grid(row=2, column=0, sticky="ew")
        self.dd_type = ttk.Combobox(ctrl, values=["坐标"], state="readonly")
        self.dd_type.current(0)
        self.dd_type.grid(row=3, column=0, sticky="ew")
        ttk.Button(ctrl, text="U-Net分割", command=self.segment_image).grid(row=4, column=0, sticky="ew")
        ttk.Button(ctrl, text="坐标检测", command=self.detect_coord).grid(row=5, column=0, sticky="ew")
        self.lbl_status = ttk.Label(ctrl, text="就绪", foreground="green")
        self.lbl_status.grid(row=6, column=0)

        right = ttk.Frame(self)
        right.grid(row=0, column=1, sticky="nsew")
        right.columnconfigure(0, weight=1)
        right.columnconfigure(1, weight=1)
        right.rowconfigure(0, weight=1)

        self.canvas_orig = tk.Label(right, text="原始图像", bg="gray")
        self.canvas_orig.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.canvas_result = tk.Label(right, text="处理结果", bg="gray")
        self.canvas_result.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

    def set_status(self, text, color="green"):
        self.lbl_status.configure(text=text, foreground=color)
        self.update_idletasks()

    def load_image(self):
        file_path = filedialog.askopenfilename(initialdir="img", filetypes=[("Image", "*.jpg;*.png;*.jpeg;*.tif;*.bmp")])
        if not file_path:
            return
        self.img_path = file_path
        self.original_img = Image.open(file_path)
        self.display_image(self.original_img, self.canvas_orig)
        self.set_status("已加载图像")

    def load_coord(self):
        if not self.img_path:
            return
        base = os.path.basename(self.img_path)
        name, _ = os.path.splitext(base)
        txt_path = os.path.join("txt_out", f"{name}.txt")
        if not os.path.exists(txt_path):
            self.set_status("坐标文件不存在", "red")
            return
        img = np.array(self.original_img.copy())
        img = draw_corner_coords(img, txt_path)
        self.display_image(Image.fromarray(img), self.canvas_orig)
        self.set_status("已加载坐标")

    def segment_image(self):
        if not self.original_img:
            self.set_status("请先加载图像", "red")
            return
        self.set_status("处理中", "orange")
        r_image = self.unet.detect_image(self.original_img.copy())
        base = os.path.basename(self.img_path)
        save_path = os.path.join("img_out", base)
        r_image.save(save_path)
        self.result_img = r_image
        self.display_image(r_image, self.canvas_result)
        self.set_status("分割完成")

    def detect_coord(self):
        if not self.result_img:
            self.set_status("请先分割图像", "red")
            return
        base = os.path.basename(self.img_path)
        name, _ = os.path.splitext(base)
        txt_path = os.path.join("txt_out", f"{name}.txt")
        if not os.path.exists(txt_path):
            self.set_status("坐标文件不存在", "red")
            return
        img_out_path = os.path.join("img_out", base)
        csv_path = f"{name}.csv"
        detect_coordinates(img_out_path, txt_path, csv_path)
        self.set_status("坐标检测完成")

    def display_image(self, image, widget):
        max_w, max_h = 400, 400
        img = image.copy()
        img.thumbnail((max_w, max_h))
        tk_img = ImageTk.PhotoImage(img)
        widget.configure(image=tk_img)
        widget.image = tk_img


if __name__ == '__main__':
    app = SatelliteApp()
    app.mainloop()
