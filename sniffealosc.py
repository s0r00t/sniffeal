#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
sniff packets from interface en0 using python module scapy (2.3.1)
generate led color for bhoreal in usb midi mode depending on packet port number
send led number + color to PD patch boreal.pd
in OSC format : /bhoreal/in lednumber ledcolor
color is midi parameter so 0 to 127.
v0.2
By Sam Neurohack
LICENCE : CC 
'''
 
from OSC import OSCClient, OSCMessage
from time import sleep
import types
import random
from scapy.all import *

client = OSCClient()
msg = OSCMessage()

counter = 0

def sendled(zzzport):
	global counter
	
	zzz = zzzport % 127			
								# zzz = led color
	msg = OSCMessage()
	msg.setAddress("/bhoreal/in")
	msg.append(counter)
	msg.append(zzz)
	try:
		client.sendto(msg, ('127.0.0.1', 9002))
		msg.clearData()
	except:
		print 'Connection refused'
		pass
	sleep(0.001)
	counter += 1
	if counter > 63:
		counter = 0



def print_summary(pkt):
    if IP in pkt:
        ip_src=pkt[IP].src
        ip_dst=pkt[IP].dst
        
        
    	if TCP in pkt:
        	tcp_sport=pkt[TCP].sport
        	tcp_dport=pkt[TCP].dport

        	if tcp_sport < 50000:
        		print " IP src " + str(ip_src) + " TCP sport " + str(tcp_sport) 
        		sendled(tcp_sport)
        	if tcp_dport < 50000:
        		print " IP dst " + str(ip_dst) + " TCP dport " + str(tcp_dport)
        		sendled(tcp_dport)
        if UDP in pkt:
        	udp_sport=pkt[UDP].sport
        	udp_dport=pkt[UDP].dport

        	if udp_sport < 50000:
        		print " IP src " + str(ip_src) + " UDP sport " + str(udp_sport) 
        		sendled(udp_sport)
        	
        	if udp_dport < 50000:
        		print " IP dst " + str(ip_dst) + " UDP dport " + str(udp_dport)
        		sendled(udp_dport)


	if ARP in pkt and pkt[ARP].op in (1,2):
		print " ARP"
		sendled(67)
        	


def handle_error(self,request,client_address):		# All callbacks
    pass

sniff(iface='en0', prn=print_summary, store=0)
