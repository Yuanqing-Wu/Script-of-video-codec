import os

def get_cmd_set_VTM_enc(cfg):
    cmd_set = []
    for seq in cfg['test_seq']:

        name, size, fps, bitdepth = seq.split('_')
        w, h = size.split('x')
        bitdepth = bitdepth.split('bit')[0]

        if cfg['rate_control_mode'] == 0:
            for qp in cfg['qp']:
                cmd = cfg['enc_path'] + ' '
                if 'config_path1' in cfg.keys():
                    cmd += '-c' + ' ' + cfg['config_path1'] + ' '
                if 'config_path2' in cfg.keys():
                    per_seq_config_path = cfg['config_path2'] + '/' + name + '.cfg'
                    cmd += '-c' + ' ' + per_seq_config_path + ' '
                cmd += '--InputFile=' + cfg['seq_path'] + '/' + seq + ' '
                cmd += '--BitstreamFile=' + cfg['output_path']  + '/' + 'bin' + '/' + seq.split('.yuv')[0] + '_qp' + str(qp) + '.bin' + ' '
                cmd += '--ReconFile=' + cfg['output_path']  + '/' + 'rec' + '/' + seq.split('.yuv')[0] + '_qp' + str(qp) + '.rec' + ' '
                cmd += '--SourceWidth=' + w + ' ' + '--SourceHeight=' + h + ' ' + '--FrameRate=' + fps + ' ' + '--QP=' + str(qp) + ' '
                cmd += '--InputBitDepth=' + bitdepth + ' '
                if len(cfg['extra_parameters']) > 0:
                    cmd += cfg['extra_parameters'] + ' '
                cmd += '>' + cfg['output_path']  + '/' + 'log' + '/Enc_' + seq.split('.yuv')[0] + '_qp' + str(qp) + '.log'
                cmd_set.append([cmd, seq, qp])
        else:
            for br in cfg['bitrate']:
                cmd = cfg['enc_path'] + ' '
                if 'config_path1' in cfg.keys():
                    cmd += '-c' + ' ' + cfg['config_path1'] + ' '
                if 'config_path2' in cfg.keys():
                    per_seq_config_path = cfg['config_path2'] + '/' + name + '.cfg'
                    cmd += '-c' + ' ' + per_seq_config_path + ' '
                cmd += '--InputFile=' + cfg['seq_path'] + '/' + seq + ' '
                cmd += '--BitstreamFile=' + cfg['output_path']  + '/' + 'bin' + '/' + seq.split('.yuv')[0] + '_bitrate' + str(br) + '.bin' + ' '
                cmd += '--ReconFile=' + cfg['output_path']  + '/' + 'rec' + '/' + seq.split('.yuv')[0] + '_bitrate' + str(br) + '.rec' + ' '
                cmd += '--SourceWidth=' + w + ' ' + '--SourceHeight=' + h + ' ' + '--FrameRate=' + fps + ' ' + '--TargetBitrate=' + str(br) + ' '
                cmd += '--InputBitDepth=' + bitdepth + ' '
                if len(cfg['extra_parameters']) > 0:
                    cmd += cfg['extra_parameters'] + ' '
                cmd += '>' + cfg['output_path']  + '/' + 'log' + '/Enc_' + seq.split('.yuv')[0] + '_bitrate' + str(br) + '.log'
                cmd_set.append([cmd, seq, br])

    if cfg['fake_proc']:

        name, size, fps, bitdepth = cfg['test_seq'][0].split('_')
        w, h = size.split('x')
        bitdepth = bitdepth.split('bit')[0]
        cmd = cfg['enc_path'] + ' '

        cmd = cfg['enc_path'] + ' '
        if 'config_path1' in cfg.keys():
                    cmd += '-c' + ' ' + cfg['config_path1'] + ' '
        if 'config_path2' in cfg.keys():
            per_seq_config_path = cfg['config_path2'] + '/' + name + '.cfg'
            cmd += '-c' + ' ' + per_seq_config_path + ' '
        cmd += '--InputFile=' + cfg['seq_path'] + '/' + cfg['test_seq'][0] + ' '
        cmd += '--SourceWidth=' + w + ' ' + '--SourceHeight=' + h + ' ' + '--FrameRate=' + fps + ' ' + '--QP=' + str(0) + ' '
        cmd += '--BitstreamFile=' + cfg['output_path']  + '/' + 'bin' + '/fake.bin' + ' '
        cmd += '--ReconFile=' + cfg['output_path']  + '/' + 'rec' + '/fake.yuv' + ' '
        cmd += '--InputBitDepth=' + bitdepth + ' '
        cmd += '1>/dev/null 2>&1'
        cmd_set.append(cmd)

    return cmd_set

def get_cmd_set_VTM_dec(cfg):

    cmd_set = []
    for seq in cfg['test_seq']:

        _, _, _, bitdepth = seq.split('_')
        bitdepth = bitdepth.split('bit')[0]

        if cfg['rate_control_mode'] == 0:
            for qp in cfg['qp']:
                cmd = cfg['dec_path'] + ' '
                cmd += '-b' + ' ' + cfg['output_path'] + '/' + 'bin' + '/' + seq.split('.yuv')[0] + '_qp' + str(qp) + '.bin' + ' '
                cmd += '-o' + ' ' + cfg['output_path'] + '/' + 'rec' + '/' + seq.split('.yuv')[0] + '_qp' + str(qp) + '.yuv' + ' '
                cmd += '--OutputBitDepth=' + bitdepth + ' '
                cmd += '>' + cfg['output_path'] + '/' + 'log' + '/Dec_' + seq.split('.yuv')[0] + '_qp' + str(qp) + '.log'
                cmd_set.append([cmd, seq, qp])
        else:
            for br in cfg['bitrate']:
                cmd = cfg['dec_path'] + ' '
                cmd += '-b' + ' ' + cfg['output_path'] + '/' + 'bin' + '/' + seq.split('.yuv')[0] + '_br' + str(br) + '.bin' + ' '
                cmd += '-o' + ' ' + cfg['output_path'] + '/' + 'rec' + '/' + seq.split('.yuv')[0] + '_br' + str(br) + '.yuv' + ' '
                cmd += '--OutputBitDepth=' + bitdepth + ' '
                cmd += '>' + cfg['output_path'] + '/' + 'log' + '/Dec_' + seq.split('.yuv')[0] + '_br' + str(br) + '.log'
                cmd_set.append([cmd, seq, qp])

    if cfg['fake_proc']:
        cmd = cfg['dec_path'] + ' '
        if cfg['rate_control_mode'] == 0:
            cmd += '-b' + ' ' + cfg['output_path'] + '/' + 'bin' + '/' + cfg['test_seq'][0].split('.yuv')[0] + '_qp' + str(cfg['qp'][0]) + '.bin' + ' '
        else:
            cmd += '-b' + ' ' + cfg['output_path'] + '/' + 'bin' + '/' + cfg['test_seq'][0].split('.yuv')[0] + '_br' + str(cfg['bitrate'][0]) + '.bin' + ' '
        cmd += '-o' + ' ' + cfg['output_path'] + '/' + 'rec' + '/' + 'fake.yuv'
        cmd += '--OutputBitDepth=' + bitdepth + ' '
        cmd_set.append(cmd)

    return cmd_set


def get_cmd_set_VTM(cfg, enc_dec='enc'):

    if enc_dec == 'enc':
        return get_cmd_set_VTM_enc(cfg)
    elif enc_dec == 'dec':
        return get_cmd_set_VTM_dec(cfg)

def get_cmd_set_AV1_enc(cfg):

    cmd_set = []
    for seq in cfg['test_seq']:

        _, size, fps, bitdepth = cfg['test_seq'][0].split('_')
        w, h = size.split('x')
        bitdepth = bitdepth.split('bit')[0]

        if cfg['rate_control_mode'] == 0:
            for qp in cfg['qp']:
                cmd = cfg['enc_path'] + ' '
                cmd += cfg['seq_path'] + '/' + seq + ' '
                if 'config_path1' in cfg.keys():
                    cmd += '-c' + ' ' + cfg['config_path1'] + ' '
                cmd += '--output=' + cfg['output_path']  + '/' + 'bin' + '/' + seq.split('.yuv')[0] + '_qp' + str(qp) + '.bin' + ' '
                cmd += '--width=' + w + ' ' + '--height=' + h + ' ' + '--fps=' + fps + '/1' + ' ' + '--cq-level=' + str(qp) + ' ' + '--end-usage=q' + ' '
                cmd += '--input-bit-depth=' + bitdepth + ' '
                if len(cfg['extra_parameters']) > 0:
                    cmd += cfg['extra_parameters'] + ' '
                cmd += '>' + cfg['output_path']  + '/' + 'log' + '/Enc_' + seq.split('.yuv')[0] + '_qp' + str(qp) + '.log' + ' '
                cmd += '2>&1'
                cmd_set.append([cmd, seq, qp])
        else:
            for br in cfg['bitrate']:
                cmd = cfg['enc_path'] + ' '
                cmd += cfg['seq_path'] + '/' + seq + ' '
                if 'config_path1' in cfg.keys():
                    cmd += '-c' + ' ' + cfg['config_path1'] + ' '
                cmd += '--output=' + cfg['output_path']  + '/' + 'bin' + '/' + seq.split('.yuv')[0] + '_bitrate' + str(br) + '.bin' + ' '
                cmd += '--width=' + w + ' ' + '--height=' + h + ' ' + '--fps=' + fps + '/1' + ' ' + '--target-bitrate=' + str(br) + ' ' + '--end-usage=vbr' + ' '
                cmd += '--input-bit-depth=' + bitdepth + ' '
                if len(cfg['extra_parameters']) > 0:
                    cmd += cfg['extra_parameters'] + ' '
                cmd += '>' + cfg['output_path']  + '/' + 'log' + '/Enc_' + seq.split('.yuv')[0] + '_bitrate' + str(br) + '.log' + ' '
                cmd += '2>&1'
                cmd_set.append([cmd, seq, br])

    if cfg['fake_proc']:

        _, size, fps, bitdepth = cfg['test_seq'][0].split('_')
        w, h = size.split('x')
        bitdepth = bitdepth.split('bit')[0]
        cmd = cfg['enc_path'] + ' '
        cmd += cfg['seq_path'] + '/' + seq + ' '
        if 'config_path1' in cfg.keys():
            cmd += '-c' + ' ' + cfg['config_path1'] + ' '
        cmd += '--output=' + cfg['output_path']  + '/' + 'bin' + '/fake.bin' + ' '
        cmd += '--width=' + w + ' ' + '--height=' + h + ' ' + '--fps=' + fps + '/1' + ' ' + '--cq-level=' + str(0) + ' ' + '--end-usage=cq' + ' '
        cmd += '--input-bit-depth=' + bitdepth + ' '
        cmd += '1>/dev/null 2>&1'
        cmd_set.append(cmd)

    return cmd_set

def get_cmd_set_AV1_dec(cfg):

    cmd_set = []
    for seq in cfg['test_seq']:

        _, _, _, bitdepth = seq.split('_')
        bitdepth = bitdepth.split('bit')[0]

        if cfg['rate_control_mode'] == 0:
            for qp in cfg['qp']:
                cmd = cfg['dec_path'] + ' '
                cmd += cfg['output_path'] + '/' + 'bin' + '/' + seq.split('.yuv')[0] + '_qp' + str(qp) + '.bin' + ' '
                cmd += '-o' + ' ' + cfg['output_path'] + '/' + 'rec' + '/' + seq.split('.yuv')[0] + '_qp' + str(qp) + '.yuv' + ' '
                cmd += '--rawvideo' + ' '
                cmd += '--output-bit-depth=' + bitdepth
                cmd_set.append([cmd, seq, qp])
        else:
            for br in cfg['bitrate']:
                cmd = cfg['dec_path'] + ' '
                cmd += '-b' + ' ' + cfg['output_path'] + '/' + 'bin' + '/' + seq.split('.yuv')[0] + '_br' + str(br) + '.bin' + ' '
                cmd += cfg['output_path'] + '/' + 'rec' + '/' + seq.split('.yuv')[0] + '_br' + str(br) + '.yuv' + ' '
                cmd += '--rawvideo' + ' '
                cmd += '--output-bit-depth=' + bitdepth + ' '
                cmd_set.append([cmd, seq, qp])

    if cfg['fake_proc']:
        cmd = cfg['dec_path'] + ' '
        if cfg['rate_control_mode'] == 0:
            cmd += cfg['output_path'] + '/' + 'bin' + '/' + cfg['test_seq'][0].split('.yuv')[0] + '_qp' + str(cfg['qp'][0]) + '.bin' + ' '
        else:
            cmd += cfg['output_path'] + '/' + 'bin' + '/' + cfg['test_seq'][0].split('.yuv')[0] + '_br' + str(cfg['bitrate'][0]) + '.bin' + ' '
        cmd += '-o' + ' ' + cfg['output_path'] + '/' + 'rec' + '/' + 'fake.yuv'
        cmd += '--rawvideo' + ' '
        cmd += '--output-bit-depth=' + bitdepth
        cmd_set.append(cmd)

    return cmd_set

def get_cmd_set_AV1(cfg, enc_dec='enc'):

    if enc_dec == 'enc':
        return get_cmd_set_AV1_enc(cfg)
    elif enc_dec == 'dec':
        return get_cmd_set_AV1_dec(cfg)

def get_cmd_set_HPM_enc(cfg):
    cmd_set = []
    for seq in cfg['test_seq']:

        name, size, fps, bitdepth = seq.split('_')
        w, h = size.split('x')
        bitdepth = bitdepth.split('bit')[0]

        if cfg['rate_control_mode'] == 0:
            for qp in cfg['qp']:
                cmd = cfg['enc_path'] + ' '
                if 'config_path1' in cfg.keys():
                    cmd += '-c' + ' ' + cfg['config_path1'] + ' '
                if 'config_path2' in cfg.keys():
                    per_seq_config_path = cfg['config_path2'] + '/' + name + '.cfg'
                    cmd += '-c' + ' ' + per_seq_config_path + ' '
                cmd += '--input ' + cfg['seq_path'] + '/' + seq + ' '
                cmd += '--output ' + cfg['output_path']  + '/' + 'bin' + '/' + seq.split('.yuv')[0] + '_qp' + str(qp) + '.bin' + ' '
                cmd += '--width ' + w + ' ' + '--height ' + h + ' ' + '--frame_rate ' + fps + ' ' + '--op_qp ' + str(qp) + ' '
                cmd += '--input_bit_depth ' + bitdepth + ' '
                if len(cfg['extra_parameters']) > 0:
                    cmd += cfg['extra_parameters'] + ' '
                cmd += '>' + cfg['output_path']  + '/' + 'log' + '/Enc_' + seq.split('.yuv')[0] + '_qp' + str(qp) + '.log'
                cmd_set.append([cmd, seq, qp])
        else:
            for br in cfg['bitrate']:
                cmd = cfg['enc_path'] + ' '
                if 'config_path1' in cfg.keys():
                    cmd += '-c' + ' ' + cfg['config_path1'] + ' '
                if 'config_path2' in cfg.keys():
                    per_seq_config_path = cfg['config_path2'] + '/' + name + '.cfg'
                    cmd += '-c' + ' ' + per_seq_config_path + ' '
                cmd += '--input ' + cfg['seq_path'] + '/' + seq + ' '
                cmd += '--output ' + cfg['output_path']  + '/' + 'bin' + '/' + seq.split('.yuv')[0] + '_bitrate' + str(br) + '.bin' + ' '
                cmd += '--width ' + w + ' ' + '--height ' + h + ' ' + '--frame_rate ' + fps + ' ' + '--TargetBitrate ' + str(br) + ' '
                cmd += '--InputBitDepth ' + bitdepth + ' '
                if len(cfg['extra_parameters']) > 0:
                    cmd += cfg['extra_parameters'] + ' '
                cmd += '>' + cfg['output_path']  + '/' + 'log' + '/Enc_' + seq.split('.yuv')[0] + '_bitrate' + str(br) + '.log'
                cmd_set.append([cmd, seq, br])

    if cfg['fake_proc']:

        name, size, fps, bitdepth = cfg['test_seq'][0].split('_')
        w, h = size.split('x')
        bitdepth = bitdepth.split('bit')[0]
        cmd = cfg['enc_path'] + ' '

        cmd = cfg['enc_path'] + ' '
        if 'config_path1' in cfg.keys():
                    cmd += '-c' + ' ' + cfg['config_path1'] + ' '
        if 'config_path2' in cfg.keys():
            per_seq_config_path = cfg['config_path2'] + '/' + name + '.cfg'
            cmd += '-c' + ' ' + per_seq_config_path + ' '
        cmd += '--input ' + cfg['seq_path'] + '/' + cfg['test_seq'][0] + ' '
        cmd += '--width ' + w + ' ' + '--height ' + h + ' ' + '--frame_rate ' + fps + ' ' + '--op_qp ' + str(0) + ' '
        cmd += '--output ' + cfg['output_path']  + '/' + 'bin' + '/fake.bin' + ' '
        cmd += '--input_bit_depth ' + bitdepth + ' '
        cmd += '1>/dev/null 2>&1'
        cmd_set.append(cmd)

    return cmd_set

def get_cmd_set_HPM_dec(cfg):

    cmd_set = []
    for seq in cfg['test_seq']:

        _, _, _, bitdepth = seq.split('_')
        bitdepth = bitdepth.split('bit')[0]

        if cfg['rate_control_mode'] == 0:
            for qp in cfg['qp']:
                cmd = cfg['dec_path'] + ' '
                cmd += '-i' + ' ' + cfg['output_path'] + '/' + 'bin' + '/' + seq.split('.yuv')[0] + '_qp' + str(qp) + '.bin' + ' '
                cmd += '-o' + ' ' + cfg['output_path'] + '/' + 'rec' + '/' + seq.split('.yuv')[0] + '_qp' + str(qp) + '.yuv' + ' '
                cmd += '>' + cfg['output_path'] + '/' + 'log' + '/Dec_' + seq.split('.yuv')[0] + '_qp' + str(qp) + '.log'
                cmd_set.append([cmd, seq, qp])
        else:
            for br in cfg['bitrate']:
                cmd = cfg['dec_path'] + ' '
                cmd += '-i' + ' ' + cfg['output_path'] + '/' + 'bin' + '/' + seq.split('.yuv')[0] + '_br' + str(br) + '.bin' + ' '
                cmd += '-o' + ' ' + cfg['output_path'] + '/' + 'rec' + '/' + seq.split('.yuv')[0] + '_br' + str(br) + '.yuv' + ' '
                cmd += '>' + cfg['output_path'] + '/' + 'log' + '/Dec_' + seq.split('.yuv')[0] + '_br' + str(br) + '.log'
                cmd_set.append([cmd, seq, qp])

    if cfg['fake_proc']:
        cmd = cfg['dec_path'] + ' '
        if cfg['rate_control_mode'] == 0:
            cmd += '-i' + ' ' + cfg['output_path'] + '/' + 'bin' + '/' + cfg['test_seq'][0].split('.yuv')[0] + '_qp' + str(cfg['qp'][0]) + '.bin' + ' '
        else:
            cmd += '-i' + ' ' + cfg['output_path'] + '/' + 'bin' + '/' + cfg['test_seq'][0].split('.yuv')[0] + '_br' + str(cfg['bitrate'][0]) + '.bin' + ' '
        cmd += '-o' + ' ' + cfg['output_path'] + '/' + 'rec' + '/' + 'fake.yuv'
        cmd_set.append(cmd)

    return cmd_set


def get_cmd_set_HPM(cfg, enc_dec='enc'):

    if enc_dec == 'enc':
        return get_cmd_set_HPM_enc(cfg)
    elif enc_dec == 'dec':
        return get_cmd_set_HPM_dec(cfg)

def get_cmd_set(cfg, enc_dec='enc'):
    if cfg['codec'] == 0:
        return get_cmd_set_VTM(cfg, enc_dec)
    elif cfg['codec'] == 1:
        return get_cmd_set_VTM(cfg, enc_dec)
    elif cfg['codec'] == 2:
        return get_cmd_set_AV1(cfg, enc_dec)
    elif cfg['codec'] == 3:
        return get_cmd_set_HPM(cfg, enc_dec)


