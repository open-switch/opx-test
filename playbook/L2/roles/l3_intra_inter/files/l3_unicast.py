#!/usr/bin/python

from scapy.all import *
from argparse import ArgumentParser
from optparse import OptionParser

def sendPackets(dstIP,srcIP):
    packet=IP(dst=dstIP,src=srcIP)/TCP(dport=300,sport=97)
    print packet.show()                                           
    send(packet,count=100)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("--dstIP", dest="destIP", default=None, action= 'store',
                        help="Destination IP address", metavar="DST_IP")
    parser.add_option("--srcIP", dest="srcIP", default=None, action="store",
                        help="Source IP address", metavar="SRC_IP")

    (opts,args) = parser.parse_args()

    sendPackets(opts.destIP,opts.srcIP)
