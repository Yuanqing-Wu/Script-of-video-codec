import pandas as pd
from config import read_cfg
import numpy as np

# cfg_file_path = 'bytevca.cfg'
# cfg = read_cfg(cfg_file_path)

# log_pathes = []

# for seq in cfg['test_seq']:
#     for qp in cfg['qp']:
#         log_path = seq.split('.yuv')[0] + '_qp' + str(qp) + '.bin2.log'
#         log_pathes.append(log_path)

# first_read = 1
# for log_path in log_pathes:
#     print(log_path)
#     seq_name, _, _, _, qp = log_path.split('_') 
#     qp = qp.split('.')[0]
#     qp = qp.split('qp')[1]
#     df = pd.read_csv(cfg['output_path'] + '/bin/' + log_path)
#     # df['seq'] = seq_name
#     # df['qp'] = int(qp)
#     if first_read:
#         data = df
#         first_read = 0
#     else:
#         #data = pd.concat((data, df),axis=0)
#         data = data.add(df)


# data.to_csv('bytevca/data.csv')
# print(data)

# data = pd.read_csv('bytevca/THR_MODES_RDO.csv')
# data = data[data['seq'] == 's2']
# print(data['mode'].value_counts(1))

data = pd.read_csv('bytevca/partition_all.csv')
df = data[['decision_0', 'decision_1', 'decision_2', 'decision_3', 'decision_4', 'decision_5', 'decision_6', 'decision_7', 'decision_8', 'decision_9']]
for i in df.index:
    df.iloc[i, :] = df.iloc[i, :] / df.iloc[i, :].sum()
#df['bsize'] = df['bsize'].div(40)
print(df)
df.to_csv('bytevca/data.csv')