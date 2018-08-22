#!/usr/bin/python

from scapy.all import *
from argparse import ArgumentParser
from optparse import OptionParser

def sendPackets(dMAC,sMAC,vlanid,dstIP,srcIP,serverint):
    packet=Ether(dst=dMAC,src=sMAC)/Dot1Q(vlan=vlanid)/IP(src=srcIP,dst=dstIP)
    sendp(packet,count=100,iface=serverint)


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("--sMAC", dest="sourceMAC", default=None, action='store',
                         help="Source MAC address", metavar="SRC_MAC")
    parser.add_option("--dMAC", dest="destMAC", default=None, action='store',
                        help="Destination MAC address", metavar="DST_MAC")
    parser.add_option("--vlanid", dest="VlanID", default=None, action='store', type='int',
                        help="Vlan id", metavar="VLAN_ID")
    parser.add_option("--dstIP", dest="destIP", default=None, action= 'store',
                        help="Destination IP address", metavar="DST_IP")
    parser.add_option("--srcIP", dest="srcIP", default=None, action="store",
                        help="Source IP address", metavar="SRC_IP")
    parser.add_option("--serverint", dest="serverint", default=None, action='store',
                        help="Server interface address to send packets", metavar="SER_INT")

    (opts,args) = parser.parse_args()

    sendPackets(opts.destMAC,opts.sourceMAC,opts.VlanID,opts.destIP,opts.srcIP,opts.serverint)
