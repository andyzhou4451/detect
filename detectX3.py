import cv2
import csv
import numpy as np
import os

def loadtxtmethod(filename):
    """Load numeric data from a comma separated text file."""
    return np.loadtxt(filename, dtype=np.float32, delimiter=',')


def process_image(img_path, txt_path, out_csv=None):
    """Process a single image and corresponding coordinate text.

    Parameters
    ----------
    img_path : str
        Path to the processed image.
    txt_path : str
        Path to the text file containing geographic information.
    out_csv : str, optional
        If given, detected coordinates will be written to this CSV file.

    Returns
    -------
    tuple of lists
        Lists of detected longitude and latitude values.
    """

    data = loadtxtmethod(txt_path)

    b = float(data[0])
    a = float(data[3])
    d = float(data[2])
    c = float(data[1])
    e = float(data[4])
    f = float(data[5])

    CoordinateX = []  # X coordinate collection
    CoordinateY = []  # Y coordinate collection

    img = cv2.imread(img_path)
    grid_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    grid_HSV = cv2.cvtColor(grid_RGB, cv2.COLOR_RGB2HSV)

    lower1 = np.array([0, 43, 46])
    upper1 = np.array([10, 255, 255])
    mask1 = cv2.inRange(grid_HSV, lower1, upper1)

    lower2 = np.array([156, 43, 46])
    upper2 = np.array([180, 255, 255])
    mask2 = cv2.inRange(grid_HSV, lower2, upper2)

    lower3 = np.array([35, 43, 46])
    upper3 = np.array([77, 255, 255])
    mask3 = cv2.inRange(grid_HSV, lower3, upper3)

    mask4 = mask1 + mask2 + mask3

    xy = np.column_stack(np.where(mask4 == 255))

    for t in xy:
        CoordinateX.append(c + int(t[1]) * ((a - c) / e))
        CoordinateY.append(d - int(t[0]) * ((d - b) / f))

    if out_csv is not None:
        with open(out_csv, "w", encoding="utf8", newline="") as csvFile:
            writer = csv.writer(csvFile)
            for x, y in zip(CoordinateX, CoordinateY):
                writer.writerow([x, y])

    return CoordinateX, CoordinateY

if __name__ == "__main__":

    path = "img_out/"

    path2 = os.path.join("样例", "txt_out")

    for filename in os.listdir(path):
        if not filename.lower().endswith((".jpg", ".png", ".jpeg", ".bmp", ".tif")):
            continue
        img_path = os.path.join(path, filename)
        txt_path = os.path.join(path2, f"{os.path.splitext(filename)[0]}.txt")
        out_csv = f"{os.path.splitext(filename)[0]}.csv"
        xs, ys = process_image(img_path, txt_path, out_csv=out_csv)
        print(xs)
        print(ys)




