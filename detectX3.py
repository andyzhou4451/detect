import cv2
import sys
import csv
import numpy as np
import os

def loadtxtmethod(filename):
    data = np.loadtxt(filename,dtype=np.float32,delimiter=',')
    return data

if __name__ == "__main__":

    path = "img_out/"
    path2 = "txt_out/"

    for filename in os.listdir(path):  # listdir的参数是文件夹的路径
        print(filename)  # 此时的filename是文件夹中文件的名称

        img_path = path + '/' + filename
        txt_path = path2 + '/' + str(filename[:-4])+".txt"

        data = loadtxtmethod(txt_path)
        print(data)

        b = float(data[0])
        a = float(data[3])
        d = float(data[2])
        c = float(data[1])
        e = float(data[4])
        f = float(data[5])

        CoordinateX = []  # 选中点的X坐标集合
        CoordinateY = []  # 选中点的Y坐标集合

        img = cv2.imread(img_path)
        # 在彩色图像的情况下，解码图像将以b g r顺序存储通道。
        grid_RGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # 从RGB色彩空间转换到HSV色彩空间
        grid_HSV = cv2.cvtColor(grid_RGB, cv2.COLOR_RGB2HSV)

        # H、S、V范围一：
        lower1 = np.array([0, 43, 46])
        upper1 = np.array([10, 255, 255])
        mask1 = cv2.inRange(grid_HSV, lower1, upper1)  # mask1 为二值图像
        # res1 = cv2.bitwise_and(grid_RGB, grid_RGB, mask=mask1)

        # H、S、V范围二：
        lower2 = np.array([156, 43, 46])
        upper2 = np.array([180, 255, 255])
        mask2 = cv2.inRange(grid_HSV, lower2, upper2)
        # res2 = cv2.bitwise_and(grid_RGB, grid_RGB, mask=mask2)

        # H、S、V范围三：
        lower3 = np.array([35, 43, 46])
        upper3 = np.array([77, 255, 255])
        mask3 = cv2.inRange(grid_HSV, lower3, upper3)
        # res2 = cv2.bitwise_and(grid_RGB, grid_RGB, mask=mask2)

        # 将三个二值图像结果 相加
        mask4 = mask1 + mask2 + mask3

        xy = np.column_stack(np.where(mask4 == 255))
        print(xy)

        for t in xy:

            # CoordinateX = c + int(t[1]) * ((a - c) / e)
            # CoordinateY = d - int(t[0]) * ((d - b) / f)
            CoordinateX.append(c + int(t[1]) * ((a - c) / e))
            CoordinateY.append(d - int(t[0]) * ((d - b) / f))



            # print(CoordinateX)
            # print(CoordinateY)


        print(CoordinateX)
        print(CoordinateY)

        # 坐标:c[1]是x,c[0]是y
        # print(int(t[1]), int(t[0]))
        # cv2.namedWindow("mask3", cv2.WINDOW_NORMAL)

        cv2.waitKey(0)
        cv2.destroyAllWindows()

        csvFile = open(str(filename[:-4])+".csv", "w", encoding='utf8', newline='')  # 创建csv文件
        writer = csv.writer(csvFile)  # 创建写的对象
        for i in range(len(CoordinateX)):
            writer.writerow([CoordinateX[i], CoordinateY[i]])
        csvFile.close()




