from config import read_cfg

def get_log_list(cfg):
    file_list = []
    for seq in cfg['test_seq']:
        q = [i for i in seq.split()]
        del(q[0])

        if cfg['rate_control_mode'] == 0 or cfg['rate_control_mode'] == 3:
            if cfg['rate_control_mode'] == 0:
                rc = 'q'
            else:
                rc = 'crf'
            for qp in q:
                file= cfg['output_path']  + '/' + 'log' + '/Enc_' + seq.split('.yuv')[0] + '_' + rc + qp + '.log'
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

def get_metric_BVC2Live(file_path):

    file = open(file_path, 'r')

    line = ' '
    while not line.startswith('frame count:'):
        line = file.readline()
        line = line.strip()
        if not line.startswith('psnrm=2:'):
            continue
        else:
            line = file.readline()
            line = file.readline()
            line = file.readline()
            line = file.readline()
            line = line.strip()
            nums = line.split()
            Y_PSNR = nums[1]
            U_PSNR = nums[2]
            V_PSNR = nums[3]
            AVG = nums[4]
            
            line = file.readline()
            line = file.readline()
            line = file.readline()
            line = line.strip()
            nums = line.split()
            Bitrate = nums[0].split(':')[1]

            line = file.readline()
            line = file.readline()
            line = line.strip()
            nums = line.split()

            tt = nums[5].split('s')[0]
            et = nums[8].split('s')[0]
    return Bitrate, Y_PSNR, U_PSNR, V_PSNR, AVG, tt, et

def get_result(cfg, result_file):

    log_list = get_log_list(cfg)

    result_file.write("Seq,Bitrate,Y-PSNR,U-PSNR,V-PSNR,AVG,tt,et\n")

    for log in log_list:
        name = log.split('/')[-1]
        Bitrate, Y_PSNR, U_PSNR, V_PSNR, AVG, tt, et = get_metric_BVC2Live(log)
        result_file.write("%s,%s,%s,%s,%s,%s,%s,%s\n"%(name, Bitrate, Y_PSNR, U_PSNR, V_PSNR, AVG, tt, et))