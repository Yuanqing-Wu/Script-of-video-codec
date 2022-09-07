
def read_cfg(config_file):

    cfg_dict = {}
    cfg_dict['test_seq'] = []

    line = ''

    with open(config_file, 'r') as fp:

        while True:                

            line = fp.readline()

            if line.startswith('#'):
                continue

            if '#' in line:
                line = line.split('#')[0]

            if line.startswith('codec:'):
                cfg_dict['codec'] = int(line.split('codec:')[1])
                continue
            
            if line.startswith('enc path:'):
                cfg_dict['enc_path'] = line.split('enc path:')[1].strip()
                cfg_dict['enc_name'] = cfg_dict['enc_path'].split('/')[1]
                continue

            if line.startswith('dec path:'):
                cfg_dict['dec_path'] = line.split('dec path:')[1].strip()
                continue

            if line.startswith('config path1:'):
                cfg_dict['config_path1'] = line.split('config path1:')[1].strip()
                continue
            
            if line.startswith('config path2:'):
                cfg_dict['config_path2'] = line.split('config path2:')[1].strip()
                continue
            
            if line.startswith('rate control mode:'):
                cfg_dict['rate_control_mode'] = int(line.split('rate control mode:')[1])
                continue
            
            if line.startswith('QP:'):
                cfg_dict['qp'] = [int(i) for i in line.split('QP:')[1].strip().split(' ')]
                continue
            
            if line.startswith('bite-rate:'):
                cfg_dict['bitrate'] = [int(i) for i in line.split('bite-rate:')[1].strip().split(' ')]
                continue
            
            if line.startswith('extra parameters:'):
                cfg_dict['extra_parameters'] = line.split('extra parameters:')[1].strip()
                continue
            
            if line.startswith('output path:'):
                cfg_dict['output_path'] = line.split('output path:')[1].strip()
                continue
            
            if line.startswith('time stamp:'):
                cfg_dict['time_stamp'] = int(line.split('time stamp:')[1].strip())
                continue

            if line.startswith('processes:'):
                cfg_dict['processes'] = int(line.split('processes:')[1])
                continue
            
            if line.startswith('fake processe:'):
                cfg_dict['fake_proc'] = int(line.split('fake processe:')[1])
                continue

            if line.startswith('log:'):
                cfg_dict['log'] = int(line.split('log:')[1])
                continue

            if line.startswith('PSNR:'):
                cfg_dict['psnr'] = int(line.split('PSNR:')[1])
                continue
            
            if line.startswith('SSIM:'):
                cfg_dict['ssim'] = int(line.split('SSIM:')[1])
                continue

            if line.startswith('VMAF:'):
                cfg_dict['vmaf'] = int(line.split('VMAF:')[1])
                continue

            if line.startswith('seq path:'):
                cfg_dict['seq_path'] = line.split('seq path:')[1].strip()
                continue
            
            if line.startswith('test seq'):
                
                while True:
                    line = fp.readline()
                    if line.startswith('#'):
                        continue
                    if line.startswith('}'):
                        break
                    if '#' in line:
                        line = line.split('#')[0]
                    cfg_dict['test_seq'].append(line)
                break
    return cfg_dict

if __name__ == '__main__':
    cfg_file_path = 'config.cfg'
    cfg = read_cfg(cfg_file_path)
    print(cfg)