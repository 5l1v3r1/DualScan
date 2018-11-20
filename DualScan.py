#!/usr/bin/python3.6

import subprocess as ps
import os
import sys
import time 
from threading import Thread

# DualScan: python script for scanning targets in parallel saving some time
# This script requires nmap preinstalled and to be executed with sudo (nmap things ¯\_(ツ)_/¯)
#
# This is the initial version and still on beta. Some features will be added
# in the future. Feel free to modify or add what you want.
#
# Changelog:
#            --- Version 0.0.1 by Sapphire
#                ---  Initial release -- https://github.com/sapphirex00
# 
# Tested in ubuntu 16.04

class bcolor:
    ok = '\033[92m'
    f = '\033[91m'
    ye = '\033[93m'
    end = '\033[0m'

def banner():
    print('''
    ________               __    _________
    \______ \ __ _______  |  |  /   _____/  ____  _____   ____    
    |    |  \|  |  \__  \ |  |  \_____  \_ / __ \ \__  \ /    \   
    |    `   \  |   / _^_\|  |__/         \  \___ / __  \   |  \  
    /_______  /____/(____  /____/_______  /\___  >____  /___|  /  
            \/           \/             \/     \/     \/     \/ 
    ''')
    print('[*] DualScan 0.0.1 (beta): 2 scans, 2 protocols, 1 command. By Sapphire ')

def helper():
    print("{}[!] DualScan needs two arguments: -t $target -o $outputext{}".format(c.ye, c.end))
    return sys.exit(1)

def info():
    print('''{}Changelog:
            --- Version 0.0.1 by Sapphire
                ---  Initial release -- https://github.com/sapphirex00{}
    '''.format(c.ok,c.end ))


class multiscan:
    
    def params(self):
        if sys.argv[1] ==  "-t" or sys.argv[1] == "--target":
            self.target = sys.argv[2]
            if sys.argv[3] ==  "-o" or sys.argv[3] == "--output":
                self.filet = 'tcp_{0}'.format(sys.argv[4])
                self.fileu = 'udp_{0}'.format(sys.argv[4])
        elif sys.argv[1] == "--help":
            helper()
            sys.exit(1)
        elif sys.argv[1] == "--info":
            info()
            sys.exit()
        else:
            helper()
            sys.exit(1)

    def tcpscan(self):
        t_scan =  'nmap -sSV -Pn -O -sC -n -A -T4 -oA {} {}'.format(self.filet, self.target)
        print("[*] Starting TCP scan... ")
        try:
            with open(os.devnull, 'w') as dv:
                ps.run([t_scan], shell=True, stdout=dv,stderr=dv)
                print("{}[+] TCP scan report saved{}".format(c.ok, c.end))
        except:
            print("{}[!] TCP scan has failed{}".format(c.f, c.end))
            sys.exit(2)
        return 0

    def udpscan(self):
        u_scan =  'nmap -sUV -Pn -O -sC -n -A -T4 -oA {} {}'.format(self.fileu, self.target)
        print("[*] Starting UDP scan... ")
        time.sleep(2)
        try:
            with open(os.devnull, 'w') as dv:
                ps.run([u_scan], shell=True, stdout=dv, stderr=dv)
                print("{}[+] UDP scan report saved{}".format(c.ok, c.end))
        except:
            print("{}[!] UDP scan has failed{}".format(c.f, c.end))
            sys.exit(2)
        return 0


if __name__ == '__main__':
    banner()
    print("[*] Starting")
    if len(sys.argv) < 2:
        helper()
    else:
        scan = multiscan()
        c =  bcolor()
        scan.params()
        try:
            th1 = Thread(target = scan.tcpscan, args=())
            th2 = Thread(target = scan.udpscan, args=())
            # start the functions:
            scan_t = th1.start()
            scan_u = th2.start()
        except:
            print("{}[!] Error: Unable to start threads D:{}".format(c.f, c.end))
            print("--> If this happens continuously, please contact me via github")
            info()
            sys.exit(2)
           
