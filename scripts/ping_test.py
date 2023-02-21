#!/usr/bin/env -S python3 -u

from time import sleep  
import threading
import socket
import select
import sys
from datetime import datetime as dt

edl_addr = ('localhost', 10025)
beacon_addr = ('0.0.0.0', 10035) # Be sure the beacon receiver sends to this port
packet = 'c4f53822000900e501'
timeout=2

packet = bytes.fromhex(packet)
tx_count = int(sys.argv[1])
delay = float(sys.argv[2])

c = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.settimeout(timeout)
s.setblocking(0)
s.bind(beacon_addr)

def pinger(count=10, delay=.5):
    print(f'Dots are pings without response. 30 pings per line.      ', end='')
    for i in range(count):
        if (i % 30 == 0):
            print(f' |\n{dt.now()} ', end='')
        print('.', end='')
        c.sendto(packet, edl_addr)
        sleep(delay)

t = threading.Thread(target=pinger, args=(tx_count, delay))
t.daemon = True
t.start()

rx_count = 0
keep_trying = True
while keep_trying and rx_count < tx_count:
    keep_trying = t.is_alive()
    if select.select([s], [], [], timeout)[0]:
        d, a = s.recvfrom(1024)
        print('\b ', end='')
        rx_count += 1
        keep_trying = True

print(f' |\nReceived {rx_count} of {tx_count} ({rx_count/tx_count*100:.2f}%)')
