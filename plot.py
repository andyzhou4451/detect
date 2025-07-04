import numpy as np
import matplotlib.pyplot as plt

# Step 1: 读取数据文件
# 文件路径
coordinate_file = "D:\Desktop\新建文件夹\wavePos\wavePos0020.txt"  # 替换为你的经纬度文件路径
image_file = "img_out\snapshot-2020-09-06T00_00_00Z.jpg"  # 替换为你的遥感图像文件路径

# 经纬度范围和图像尺寸
lat_min, lon_min, lat_max, lon_max = 19.5548, 116.2884, 22.1848, 119.1146
width, height = 4934, 4339

# 从文件读取经纬度点
lon_lat_data = []
with open(coordinate_file, "r") as file:
    for line in file:
        parts = line.strip().split()
        if len(parts) >= 2:  # 确保每行至少有两个数值
            lon, lat = float(parts[0]), float(parts[1])
            lon_lat_data.append((lon, lat))

# Step 2: 经纬度转换为像素坐标，并过滤超出范围的点
def lonlat_to_pixel(lon, lat, lon_min, lon_max, lat_min, lat_max, width, height):
    if lon_min <= lon <= lon_max and lat_min <= lat <= lat_max:  # 判断点是否在范围内
        x = (lon - lon_min) / (lon_max - lon_min) * width
        y = (lat_max - lat) / (lat_max - lat_min) * height
        return int(x), int(y)
    return None  # 返回None表示点超出范围

# 转换并过滤
pixel_points = [
    lonlat_to_pixel(lon, lat, lon_min, lon_max, lat_min, lat_max, width, height)
    for lon, lat in lon_lat_data
]
pixel_points = [point for point in pixel_points if point is not None]  # 去除None的点

# Step 3: 标记红色点
# 加载遥感图像
image = plt.imread(image_file)

# 创建绘图
plt.figure(figsize=(10, 10))
plt.imshow(image)

# 绘制点（红色小圆点）
for x, y in pixel_points:
    plt.scatter(x, y, color='red', s=10)  # s是点的大小，调整为合适的值

# 保存结果
plt.axis('off')
plt.savefig("image_with_points_filtered.png", bbox_inches='tight', pad_inches=0)
plt.show()