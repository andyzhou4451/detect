import os
import csv
from netCDF4 import Dataset

# 指定文件夹路径
csv_folder = 'D:/Desktop/内波遥感数据/识别结果/nc_out/'  # 替换为你的CSV文件所在文件夹路径
nc_folder = 'D:/Desktop/内波遥感数据/识别结果/nc_out/'  # 指定生成的NetCDF文件存放文件夹路径

# 确保输出文件夹存在
if not os.path.exists(nc_folder):
    os.makedirs(nc_folder)

# 遍历文件夹中的所有CSV文件
for csv_filename in os.listdir(csv_folder):
    if csv_filename.endswith('.csv'):  # 确保是CSV文件
        # 读取CSV文件
        with open(os.path.join(csv_folder, csv_filename), 'r', newline='', encoding='utf-8') as csvfile:
            csvreader = csv.reader(csvfile)
            rows = list(csvreader)
            CoordinateX = [float(row[0]) for row in rows]
            CoordinateY = [float(row[1]) for row in rows]

        # 创建对应的NetCDF文件名
        nc_filename = os.path.join(nc_folder, csv_filename[:-4] + '.nc')

        # 创建NetCDF文件
        nc_file = Dataset(nc_filename, 'w', format='NETCDF4')

        # 创建维度
        nc_file.createDimension('points', len(CoordinateX))

        # 创建变量
        var_x = nc_file.createVariable('CoordinateX', 'f4', ('points',))
        var_y = nc_file.createVariable('CoordinateY', 'f4', ('points',))

        # 将数据写入变量
        var_x[:] = CoordinateX
        var_y[:] = CoordinateY

        # 关闭NetCDF文件
        nc_file.close()

        print(f'已转换：{csv_filename} -> {nc_filename}')
