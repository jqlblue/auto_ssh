#!/usr/bin/env python
#-*- coding: utf-8 -*-


from __future__ import print_function

from __future__ import absolute_import

import signal, fcntl, termios, struct, sys
import pexpect
import argparse

global_pexpect_instance = None # Used by signal handler

def main():


    parser = argparse.ArgumentParser("^_^")
    #parser = parser.add_mutually_exclusive_parser()
    parser.add_argument("--host", action='store', dest='_host', default="", help="set host or ip of servers")
    parser.add_argument("--user", action='store', dest='_user', default="", help="set username")
    parser.add_argument("--port", action='store', dest='_port', default="", help="set the host port")
    parser.add_argument("--pass", action='store', dest='_pass', default="", help="set user password")
    args = parser.parse_args()

    ssh_newkey = 'Are you sure you want to continue connecting'
    ssh_command = "ssh -l %s -p %s %s" % (args._user, args._port, args._host)
    p=pexpect.spawn("/bin/bash", ['-c', ssh_command], env = {"TERM": "xterm"})
    i=p.expect([ssh_newkey,'password:',pexpect.EOF,pexpect.TIMEOUT],1)
    
    if i==0:
        print("I say yes")
        p.sendline('yes')
        i=p.expect([ssh_newkey,'password:',pexpect.EOF])
    if i==1:
        print("I give password")
        p.sendline("%s" % args._pass)
    elif i==2:
        print("I either got key or connection timeout")
        pass
    elif i==3: #timeout
        pass
    
    p.sendline("\r")
    global global_pexpect_instance
    global_pexpect_instance = p
    signal.signal(signal.SIGWINCH, sigwinch_passthrough)

    winsizes = getwinsize()
    try:
        p.setwinsize(winsizes[0], winsizes[1])
        p.interact()
        sys.exit(0)
    except:
        sys.exit(1)

def sigwinch_passthrough (sig, data):

    a = getwinsize()

    global global_pexpect_instance
    global_pexpect_instance.setwinsize(a[0],a[1])

def getwinsize():
    if 'TIOCGWINSZ' in dir(termios):
        TIOCGWINSZ = termios.TIOCGWINSZ
    else:
        TIOCGWINSZ = 1074295912L # Assume
    s = struct.pack('HHHH', 0, 0, 0, 0)
    x = fcntl.ioctl(sys.stdout.fileno(), TIOCGWINSZ, s)
    return struct.unpack('HHHH', x)[0:2]

if __name__ == "__main__":
    main()
