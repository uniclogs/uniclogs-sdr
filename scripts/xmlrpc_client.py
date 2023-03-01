#!/usr/bin/env python3
'''$0 set_tx_gain 20'''

import sys, re
from xmlrpc.client import ServerProxy

xml_addr = ('localhost', 10080)
xo = ServerProxy('http://%s:%i' % xml_addr)

command = sys.argv[1]
func = xo.__getattr__(command)
args = []
if func:
    for a in sys.argv[2:]:
        if a.isdecimal():
            args.append(int(a))
        elif a:
            args.append(a)
    if re.match(r'^set_', command):
        func(*args)
        l = list(command)
        l[0] = 'g'
        func = xo.__getattr__(''.join(l))
    print(func())
