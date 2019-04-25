#!/usr/bin/python

from scapy.all import *
import argparse

def sendPackets(dstIP, srcIP):
    packet = IPv6(dst=dstIP, src=srcIP) / TCP(dport=300, sport=97)
    print
    packet.show()
    send(packet, count=100)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--dstIP', dest='dstIP', default=None, action='store',
                        help='Destination IP address', metavar='DST_IP')
    parser.add_argument('--srcIP', dest='srcIP', default=None, action='store',
                        help='Source IP address', metavar='SRC_IP')

    args = parser.parse_args()

    sendPackets(args.dstIP, args.srcIP)