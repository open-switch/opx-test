#!/usr/bin/python

from scapy.all import *
from argparse import ArgumentParser
from optparse import OptionParser


def sendPackets(dstIP,srcIP,serverint):
    packet=Ether(IP(src=srcIP,dst=dstIP))
    send(packet,count=10,iface=serverint)
 

if __name__ == '__main__':

    parser = OptionParser()

    parser.add_option("--dstIP", dest="destIP", default=None, action= 'store',
                        help="Destination IP address", metavar="DST_IP")
    parser.add_option("--srcIP", dest="srcIP", default=None, action="store",
                        help="Source IP address", metavar="SRC_IP")
    parser.add_option("--serverint", dest="serverint", default=None, action='store',
                        help="Server interface address to send packets", metavar="SER_INT")
    
    (opts,args) = parser.parse_args()

    sendPackets(opts.destIP,opts.srcIP,opts.serverint)
