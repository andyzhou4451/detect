import pandas as pd

# 读取两个CSV文件
df1 = pd.read_csv("snapshot-2024-08-27T00_00_00Z.csv", header=None, delimiter='\t')
df2 = pd.read_csv("snapshot-2024-08-27T00_00_00Z1.csv", header=None, delimiter='\t')
# df3 = pd.read_csv("snapshot-2024-08-07T00_00_00Z1.csv", header=None, delimiter='\t')
# df4 = pd.read_csv("snapshot-2024-08-05T00_00_00Z3.csv", header=None, delimiter='\t')
# df5 = pd.read_csv("snapshot-2024-08-05T00_00_00Z4.csv", header=None, delimiter='\t')
# df4 = pd.read_csv("D:\Desktop\新建文件夹\snapshot-2024-05-12T00_00_00Z3.csv", header=None, delimiter='\t')


# 使用concat函数按行合并DataFrame
merged_df = pd.concat([df1, df2], ignore_index=True)
# merged_df = pd.concat([df1, df2], ignore_index=True)

# 将合并后的DataFrame保存到新的CSV文件中
merged_df.to_csv("snapshot-2024-08-27T00_00_00Z3.csv", index=False, header=False, sep='\t')
