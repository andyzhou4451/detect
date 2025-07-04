from netCDF4 import Dataset

# 读取 NetCDF 文件
input_file = 'snapshot-2012-09-10T00_00_00Z_lengths.nc'
with Dataset(input_file, 'r') as nc:
    # 读取变量
    cluster = nc.variables['cluster'][:]
    peak_length = nc.variables['peak_length'][:]

# 显示内容
print("Cluster\t\tPeak Length (kilometers)")
print("----------------------------------")
for c, pl in zip(cluster, peak_length):
    print(f"{c}\t\t{pl}")

