import os
log_path = '/home/medialab-313/bs/script/Script-of-Video-Codec/result/bytevca_passes_1/log'
log_list = [f for f in os.listdir(log_path)]
data_dic = {}
for log in log_list:
    with open(log_path + '/' + log, 'r') as fp:
        lines = fp.readlines()[-38:-4]
        #print(lines)
        for line in lines:
            data_list = line.strip().split(' ')
            #print(data_list)
            i = 0
            fun_name = data_list[0]
            rate = data_list[-1].split('%')[0]
            if '[' in rate:
                rate = rate.split('[')[1]
            rate = float(rate)
            if fun_name in data_dic:
                data_dic[fun_name] += float(rate)
            else:
                data_dic[fun_name] = float(rate)

for fun in data_dic:
    print('%50s %.02f'%(fun, data_dic[fun]/40))
#print(data_dic)            
            #fp.seek(-5000, 2)
