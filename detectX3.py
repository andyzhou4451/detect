import cv2
import csv
import numpy as np
import os

__all__ = [
    "loadtxtmethod",
    "extract_coordinates_from_image",
    "main",
]

def loadtxtmethod(filename):
    data = np.loadtxt(filename,dtype=np.float32,delimiter=',')
    return data

def extract_coordinates_from_image(img_path, txt_dir="txt_out", csv_dir=None):
    """Extract geographic coordinates from a predicted image.

    Parameters
    ----------
    img_path : str
        Path to the predicted image.
    txt_dir : str, optional
        Folder containing txt files with geographic metadata.
    csv_dir : str, optional
        Output folder for csv file. If ``None`` csv will be saved next to
        ``img_path`` using the same base name.

    Returns
    -------
    str
        Path to the csv file created.
    list
        List of ``(lon, lat)`` tuples extracted from the image.
    """
    base = os.path.basename(img_path)
    txt_path = os.path.join(txt_dir, base[:-4] + ".txt")
    data = loadtxtmethod(txt_path)

    b = float(data[0])
    a = float(data[3])
    d = float(data[2])
    c = float(data[1])
    e = float(data[4])
    f = float(data[5])

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

    CoordinateX = []
    CoordinateY = []
    for t in xy:
        CoordinateX.append(c + int(t[1]) * ((a - c) / e))
        CoordinateY.append(d - int(t[0]) * ((d - b) / f))

    coords = list(zip(CoordinateX, CoordinateY))

    csv_dir = csv_dir or os.path.dirname(img_path)
    os.makedirs(csv_dir, exist_ok=True)
    csv_path = os.path.join(csv_dir, base[:-4] + ".csv")
    with open(csv_path, "w", encoding="utf8", newline="") as csvFile:
        writer = csv.writer(csvFile)
        for x, y in coords:
            writer.writerow([x, y])

    return csv_path, coords


def main(path="img_out", txt_dir="txt_out"):
    for filename in os.listdir(path):
        if not filename.lower().endswith((".jpg", ".png")):
            continue
        img_path = os.path.join(path, filename)
        print("processing", filename)
        extract_coordinates_from_image(img_path, txt_dir)


if __name__ == "__main__":
    main()
