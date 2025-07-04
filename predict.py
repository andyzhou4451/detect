import cv2
import numpy as np
import os
import sys

def predict_image(image_path, output_dir='img_out'):
    """Simple edge based prediction.

    Args:
        image_path (str): path to input image.
        output_dir (str): directory to save result.

    Returns:
        str: path to saved output image.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    out = np.zeros_like(img)
    out[edges != 0] = (0, 255, 0)
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, os.path.basename(image_path))
    cv2.imwrite(out_path, out)
    return out_path


def main(argv=None):
    argv = argv or sys.argv[1:]
    if argv:
        for path in argv:
            print('predict', path)
            predict_image(path)
    else:
        for name in os.listdir('img'):
            if name.lower().endswith(('.jpg', '.png')):
                predict_image(os.path.join('img', name))


if __name__ == '__main__':
    main()
