import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import numpy as np
import matplotlib.pyplot as plt

import predict
import detectX3


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Satellite ISW Detector")
        self.image_label = tk.Label(root)
        self.image_label.pack()

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=10)
        tk.Button(btn_frame, text="选择图像", command=self.load_image).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="显示地图", command=self.show_map).pack(side=tk.LEFT, padx=5)

        self.current_csv = None

    def load_image(self):
        path = filedialog.askopenfilename(initialdir='img',
                                          filetypes=[('Image', '*.jpg *.png')])
        if not path:
            return
        out_path = predict.predict_image(path)
        csv_path, _ = detectX3.extract_coordinates_from_image(out_path)
        self.current_csv = csv_path

        img = Image.open(out_path)
        txt_file = os.path.join('txt_out', os.path.basename(out_path)[:-4] + '.txt')
        try:
            data = detectX3.loadtxtmethod(txt_file)
            b = float(data[0])
            a = float(data[3])
            d = float(data[2])
            c = float(data[1])
            draw = ImageDraw.Draw(img)
            w, h = img.size
            draw.text((2, 2), f"{d:.4f},{c:.4f}", fill=(255, 255, 255))
            draw.text((w-120, 2), f"{d:.4f},{a:.4f}", fill=(255, 255, 255))
            draw.text((2, h-20), f"{b:.4f},{c:.4f}", fill=(255, 255, 255))
            draw.text((w-120, h-20), f"{b:.4f},{a:.4f}", fill=(255, 255, 255))
        except Exception as e:
            print('label corner failed:', e)

        tk_img = ImageTk.PhotoImage(img)
        self.image_label.configure(image=tk_img)
        self.image_label.image = tk_img

    def show_map(self):
        if not self.current_csv:
            messagebox.showinfo('提示', '请先选择图像')
            return
        data = np.loadtxt(self.current_csv, delimiter=',')
        plt.figure(figsize=(6, 4))
        if data.size > 0:
            plt.scatter(data[:, 0], data[:, 1], s=2, c='r')
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title(os.path.basename(self.current_csv))
        plt.grid(True)
        plt.show()


def main():
    root = tk.Tk()
    App(root)
    root.mainloop()


if __name__ == '__main__':
    main()
