#!/usr/bin/python

from scapy.all import *
from argparse import ArgumentParser
from optparse import OptionParser

def sendPackets(dMAC,sMAC,etherType,serverint):
    packet=Ether(dst=dMAC,src=sMAC,type=etherType)
    sendp(packet,count=100,iface=serverint)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("--sMAC", dest="sourceMAC", default=None, action='store',
                         help="Source MAC address", metavar="SRC_MAC")
    parser.add_option("--dMAC", dest="destMAC", default=None, action='store',
                        help="Destination MAC address", metavar="DST_MAC")
    parser.add_option("--serverint", dest="serverint", default=None, action='store',
                        help="Server interface address to send packets", metavar="SER_INT")
    parser.add_option("--ethertype", dest="ethertype", default=None, type='int',action='store',
                        help="Server interface ad", metavar="SER_INT")


    (opts,args) = parser.parse_args()

    sendPackets(opts.destMAC,opts.sourceMAC,opts.ethertype,opts.serverint)
