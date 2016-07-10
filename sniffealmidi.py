#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Sniff packets from interface en0 using python module scapy (2.3.1)
and generate led color for bhoreal in usb midi mode depending on packet port number

Led are midi notes (0 to 63)
Color is a midi parameter (velocity) so 0 to 127.

To modify the network interface (wifi/ethernet), change it in the last code line.

Uses mido to send MIDI messages directly in python.

v0.3
By Sam Neurohack
LICENCE : CC
'''

import argparse
import mido
import sys
from time import sleep
from scapy.all import *

def print_summary(pkt):
    global counter
    out = 0
    if IP in pkt:
        ip_src=pkt[IP].src
        ip_dst=pkt[IP].dst

    if TCP in pkt:
        tcp_sport=pkt[TCP].sport
        tcp_dport=pkt[TCP].dport

        if tcp_sport < 50000:
            print " IP src " + str(ip_src) + " TCP sport " + str(tcp_sport)
            out = tcp_sport
        if tcp_dport < 50000:
            print " IP dst " + str(ip_dst) + " TCP dport " + str(tcp_dport)
            out = tcp_dport

    if UDP in pkt:
        udp_sport=pkt[UDP].sport
        udp_dport=pkt[UDP].dport

        if udp_sport < 50000:
            print " IP src " + str(ip_src) + " UDP sport " + str(udp_sport)
            out = udp_sport

        if udp_dport < 50000:
            print " IP dst " + str(ip_dst) + " UDP dport " + str(udp_dport)
            out = udp_dport

    if ARP in pkt and pkt[ARP].op in (1,2):
        print " ARP"
        out = 67

    outport.send(mido.Message('note_on', note=counter, velocity=out%127))
    sleep(0.001)
    counter += 1
    if counter > 63:
        counter = 0

if __name__ == "__main__":
    parse = argparse.ArgumentParser(description="Sniff traffic on a network interface and send it to BHOREAL MIDI controller")
    parse.add_argument("-i", "--interface", help="network interface to be sniffed", default="en0")
    parse.add_argument("-d", "--device", help="MIDI device", default="Arduino Leonardo")
    args = parse.parse_args()

    try:
        outport = mido.open_output(args.device)
    except IOError:
        print "error: MIDI device not found"
        sys.exit(1)

    global counter
    counter = 0
    sniff(iface=args.interface, prn=print_summary, store=0)
