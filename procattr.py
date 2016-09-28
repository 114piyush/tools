#!/usr/bin/python
import sys
import os
import re
import argparse

def get_proc_stat(pid):
    f_name = os.path.join('/proc', pid, 'stat')
    f_data = None
    with open(f_name, 'r') as f:
        f_data = f.read()
    f_data = f_data.split()
    return f_data

def get_proc_maps(pid):
    f_name = os.path.join('/proc', pid, 'maps')
    f_data = None
    with open(f_name, 'r') as f:
        f_data = f.read()
    return f_data

def get_proc_status(pid):
    f_name = os.path.join('/proc', pid, 'status')
    f_data = None
    result = dict()
    with open(f_name, 'r') as f:
        f_data = f.readlines()
    for line in f_data:
        key, val = re.sub('[\n]', '', line).split(':')
        result[key] = ' '.join(val.split())
    return result

def get_proc_attr(pid):
    stat = get_proc_stat(pid)
    status = get_proc_status(pid)
    attr = dict()
    attr['Identifiers'] = dict()
    attr['Identifiers']['PID'] = stat[0]
    attr['Identifiers']['PPID'] = stat[5]
    attr['Identifiers']['EUID'] = stat[3]
    attr['Identifiers']['EGID'] = stat[4]
    attr['Identifiers']['RUID'] = status['Uid'].split()[0]
    attr['Identifiers']['RGID'] = status['Gid'].split()[0]
    attr['Identifiers']['FSUID'] = status['Uid'].split()[3]
    attr['Identifiers']['FSGID'] = status['Gid'].split()[3]
    attr['State'] = stat[2]
    attr['Thread Information'] = status['Tgid']
    attr['Priority'] = dict()
    attr['Priority']['Priority Number'] = stat[17]
    attr['Priority']['Niceness Value'] = stat[18]
    attr['Time Information'] = dict()
    attr['Time Information']['stime'] = stat[14]
    attr['Time Information']['utime'] = stat[13]
    attr['Time Information']['cstime'] = stat[16]
    attr['Time Information']['cutime'] = stat[15]
    attr['Address Space'] = dict()
    attr['Address Space']['Startcode'] = stat[25]
    attr['Address Space']['Endcode'] = stat[26]
    attr['Address Space']['ESP'] = stat[28]
    attr['Address Space']['EIP'] = stat[29]
    attr['Resource'] = dict()
    attr['Resource']['File Handles'] = status['FDSize']
    attr['Resource']['Context Switches'] = status['voluntary_ctxt_switches']
    attr['Processors'] = dict()
    attr['Processors']['Allowed processors'] = status['Cpus_allowed']
    attr['Processors']['Last used'] = stat[38]
    attr['Memory Map'] = get_proc_maps(pid)
    return attr

def main():
    parser = argparse.ArgumentParser(description='Get process attributes')
    parser.add_argument('-p', '--pid', help='Input process id', required=True)
    args = parser.parse_args()
    proc_info = get_proc_attr(args.pid)
    import pprint
    pprint.pprint(proc_info)
    

if __name__ == '__main__':
    #print get_proc_status('4915')
    main()
