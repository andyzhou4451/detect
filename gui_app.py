import os
import csv
import cv2
import numpy as np
from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
from tkinter import messagebox

IMG_DIR = 'img'
OUT_DIR = 'img_out'
TXT_DIR = 'txt_out'
CSV_DIR = 'csv_out'

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(CSV_DIR, exist_ok=True)


def predict_image(image_path, output_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    result = np.zeros_like(img)
    result[edges != 0] = (0, 255, 0)
    cv2.imwrite(output_path, result)
    return output_path


def load_coords(txt_path):
    with open(txt_path, 'r') as f:
        data = [float(x) for x in f.read().strip().split(',')]
    return data  # b,c,d,a,e,f


def extract_coordinates(pred_path, txt_path, csv_path):
    data = load_coords(txt_path)
    b, c, d, a, e, f_ = data
    img = cv2.imread(pred_path)
    grid_HSV = cv2.cvtColor(cv2.cvtColor(img, cv2.COLOR_BGR2RGB), cv2.COLOR_RGB2HSV)
    lower1 = np.array([0, 43, 46])
    upper1 = np.array([10, 255, 255])
    mask1 = cv2.inRange(grid_HSV, lower1, upper1)
    lower2 = np.array([156, 43, 46])
    upper2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(grid_HSV, lower2, upper2)
    lower3 = np.array([35, 43, 46])
    upper3 = np.array([77, 255, 255])
    mask3 = cv2.inRange(grid_HSV, lower3, upper3)
    mask = mask1 + mask2 + mask3
    xy = np.column_stack(np.where(mask == 255))
    coord = []
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for t in xy:
            x = c + int(t[1]) * ((a - c) / e)
            y = d - int(t[0]) * ((d - b) / f_)
            writer.writerow([x, y])
            coord.append((x, y))
    return coord


def overlay_results(out_path, txt_path, points):
    b, c, d, a, e, f_ = load_coords(txt_path)
    with Image.open(out_path) as im:
        draw = ImageDraw.Draw(im)
        draw.text((2, 2), f"{b:.4f},{c:.4f}", fill='white')
        draw.text((im.width - 100, 2), f"{b:.4f},{a:.4f}", fill='white')
        draw.text((2, im.height - 20), f"{d:.4f},{c:.4f}", fill='white')
        draw.text((im.width - 100, im.height - 20), f"{d:.4f},{a:.4f}", fill='white')
        for x, y in points:
            px = (x - c) / (a - c) * im.width
            py = (d - y) / (d - b) * im.height
            draw.ellipse((px - 1, py - 1, px + 1, py + 1), fill='red')
        im.save(out_path)
    return out_path


def process(filename):
    img_path = os.path.join(IMG_DIR, filename)
    out_path = os.path.join(OUT_DIR, filename)
    txt_path = os.path.join(TXT_DIR, os.path.splitext(filename)[0] + '.txt')
    csv_path = os.path.join(CSV_DIR, os.path.splitext(filename)[0] + '.csv')
    predict_image(img_path, out_path)
    if os.path.exists(txt_path):
        pts = extract_coordinates(out_path, txt_path, csv_path)
        overlay_results(out_path, txt_path, pts)
    return out_path


def show_image(img_path):
    img = Image.open(img_path)
    img.thumbnail((600, 600))
    img_tk = ImageTk.PhotoImage(img)
    panel.configure(image=img_tk)
    panel.image = img_tk


def on_process():
    sel = listbox.curselection()
    if not sel:
        messagebox.showwarning('select', '请选择图片')
        return
    filename = listbox.get(sel[0])
    try:
        out = process(filename)
        show_image(out)
    except Exception as e:
        messagebox.showerror('error', str(e))


root = tk.Tk()
root.title('ISW Detect GUI')

listbox = tk.Listbox(root, width=40)
for f in os.listdir(IMG_DIR):
    if f.lower().endswith(('.jpg', '.png', '.jpeg')):
        listbox.insert(tk.END, f)
listbox.pack(side='left', fill='y')

btn = tk.Button(root, text='处理', command=on_process)
btn.pack(side='top')

panel = tk.Label(root)
panel.pack(side='right')

root.mainloop()
