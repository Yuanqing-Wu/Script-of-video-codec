from config import read_cfg

def get_log_list(cfg):
    file_list = []
    for seq in cfg['test_seq']:
        if cfg['rate_control_mode'] == 0:
            for qp in cfg['qp']:
                file= cfg['output_path']  + '/' + 'log' + '/Enc_' + seq.split('.yuv')[0] + '_qp' + str(qp) + '.log'
                file_list.append(file)
        else:
            for br in cfg['bitrate']:
                file += '>' + cfg['output_path']  + '/' + 'log' + '/Enc_' + seq.split('.yuv')[0] + '_bitrate' + str(br) + '.log'
                file_list.append(file)
    return file_list

def get_metric(file_path):

    file = open(file_path, 'r')

    line = ' '
    while not line.startswith('Total Time:'):
        line = file.readline()
        line = line.strip()
        if not line.startswith('LayerId'):
            continue
        else:
            line = file.readline()
            line = file.readline()
            line = line.strip()
            nums = line.split()
            Bitrate = nums[2]
            Y_PSNR = nums[3]
            U_PSNR = nums[4]
            V_PSNR = nums[5]
            
            while True:
                line = file.readline()
                line = line.strip()
                if line.startswith('Total Time:'):
                    before, after = line.split('Total Time:')
                    time, after = after.split('sec. [user]')
                    EncT = time.strip()
                    break
    return Bitrate, Y_PSNR, U_PSNR, V_PSNR, EncT

def get_result(cfg, result_file):

    log_list = get_log_list(cfg)

    result_file.write("Seq,Bitrate,Y-PSNR,U-PSNR,V-PSNR,EncT\n")

    for log in log_list:
        name = log.split('/')[-1]
        Bitrate, Y_PSNR, U_PSNR, V_PSNR, EncT = get_metric(log)
        result_file.write("%s,%s,%s,%s,%s,%s\n"%(name, Bitrate, Y_PSNR, U_PSNR, V_PSNR, EncT))