import os
import cv2
import numpy as np

INPUT_DIR = os.path.join('样例', 'img')
OUTPUT_DIR = os.path.join('样例', 'img_out')

os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_image(in_path, out_path):
    img = cv2.imread(in_path)
    if img is None:
        return
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    output = np.zeros_like(img)
    # draw detected edges in red on a black background
    output[edges > 0] = (0, 0, 255)
    cv2.imwrite(out_path, output)

if __name__ == '__main__':
    for fname in os.listdir(INPUT_DIR):
        if not fname.lower().endswith(('.jpg', '.png', '.jpeg', '.bmp', '.tif')):
            continue
        in_path = os.path.join(INPUT_DIR, fname)
        out_path = os.path.join(OUTPUT_DIR, fname)
        process_image(in_path, out_path)
