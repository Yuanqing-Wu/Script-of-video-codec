import os
import time
from config import read_cfg
from command import get_cmd_set
from processor import multi_processor, single_processor


cfg_file_path = 'hpm.cfg'
cfg = read_cfg(cfg_file_path)

if os.path.exists(cfg['output_path']) == 0:
    os.mkdir(cfg['output_path'])
if os.path.exists(cfg['output_path'] + '/' + 'bin') == 0:
    os.mkdir(cfg['output_path'] + '/' + 'bin')
if os.path.exists(cfg['output_path'] + '/' + 'rec') == 0:
    os.mkdir(cfg['output_path'] + '/' + 'rec')
if os.path.exists(cfg['output_path'] + '/' + 'log') == 0:
    os.mkdir(cfg['output_path'] + '/' + 'log')

cmd_set = get_cmd_set(cfg, enc_dec='enc')

# start encoding
print('==> Start encoding.')
start_time = time.time()
if cfg['processes'] <= 1:
    single_processor(cmd_set)
else:
    multi_processor(cfg, cmd_set)

#finish encodeing
end_time = time.time()
print('==> Finish encoding. || Run time: {:.2f} sec.'.format(end_time - start_time))

cmd_set = get_cmd_set(cfg, enc_dec='dec')
# start decoding
print('==> Start decoding.')
start_time = time.time()
if cfg['processes'] <= 1:
    single_processor(cmd_set)
else:
    multi_processor(cfg, cmd_set)

#finish decodeing
end_time = time.time()
print('==> Finish decoding. || Run time: {:.2f} sec.'.format(end_time - start_time))




