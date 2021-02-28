# -*- coding: utf-8 -*-

import subprocess
import json
from xbutil_gui import CU_STATUS_DICT


def get_mem_usages(pids, host='localhost'):
    if host == 'localhost':
        # ps -o pid,rss,cmd 273899
        command = ['ps', '-o', 'pid,rss,cmd'] + pids
    else:
        command = ['ssh', host, 
                    'ps', '-o', 'pid,rss,cmd'] + pids

    #print('command=', command)
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    ps_dump = p.stdout.read().decode('utf-8')
    #print(ps_dump)
    ps_lines = ps_dump.strip().split('\n')
    rss = 0
    for l in ps_lines[1:]:
        #print('line', l)
        ps_fields = l.split()
        pid = ps_fields[0]
        #print('before', ps_fields[1], rss)
        rss = rss + int(ps_fields[1])
        #print('after', ps_fields[1], rss)

    mem_usage_dict = {pid: rss}
    #print(mem_usage_dict)
    return mem_usage_dict

