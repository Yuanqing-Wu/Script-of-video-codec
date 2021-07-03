import os
import subprocess
import time

def check_proc(sub_proc):
    for p in sub_proc:
        if p.poll() == 0:
            sub_proc.remove(p)
    return sub_proc

def multi_processor(cfg, cmd_set):

    sub_proc = []
    NumTotalProc = len(cmd_set)
    if cfg['fake_proc']:
        NumTotalProc = NumTotalProc - 1

    StartedProc = 0
    
    while(StartedProc < NumTotalProc):

        sub_proc = check_proc(sub_proc)
        #print(len(sub_proc))
        if len(sub_proc) < cfg['processes']:
            cmd, seq, qp_or_br = cmd_set[StartedProc]
            print("==> Start running %50s %d"%(seq, qp_or_br))
            p = subprocess.Popen(cmd, shell=True)
            sub_proc.append(p)
            StartedProc = StartedProc + 1                               
        time.sleep(0.1)
    
    if cfg['fake_proc']:
        fake_proc = []
        while len(check_proc(sub_proc)) > 0:  # Ensure real proc is done
            if len(check_proc(sub_proc)) + len(check_proc(fake_proc)) < cfg['processes']:
                cmd = cmd_set[StartedProc]
                p = subprocess.Popen(cmd, shell=True)
                fake_proc.append(p)
            time.sleep(0.1)
        subprocess.Popen("kill -9 $(pidof " + cfg['enc_name'] + ")", shell=True)
    
    else:
        while len(check_proc(sub_proc)) > 0:
            time.sleep(0.1)

        
def single_processor(cmd_set):
    for cmd in cmd_set:
        print("==> Start encoding %50s %d"%(cmd[1], cmd[2]))
        os.system(cmd[0])
        