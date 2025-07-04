import pandas as pd

# 读取CSV文件
data = pd.read_csv('snapshot-2024-09-25T00_00_00Z.csv', header=None, delimiter='\t')

# 计算数据总共有多少条
total_samples = len(data)

# 计算采样步长
step = total_samples // 900

# 从数据的开头开始按照采样步长取样，直到取满1000条数据为止
sampled_data = data.iloc[::step]

# 将采样后的数据保存到文件
sampled_data.to_csv('D:\Desktop\内波信息提取\y服务器csv\snapshot-2024-09-25T00_00_00Z.csv', index=False, header=False, sep='\t')

print("采样完成，共采样了 %d 条数据" % len(sampled_data))
