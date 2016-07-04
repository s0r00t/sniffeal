A scanner interface that use Bhoreal led matrix.


For cool educative purpose a network interface scanner light up the Bhoreal RGB Leds.
The color depends on the IP packet port. So you can see the actual http, ftp, irc, imap,...  flow of a computer.
You can also visually check if all packet go through your favorite VPN !

If you have network sniff error, consider install pypcap python module.
The interface name like en0 can be changed in the last line.

Needs pyOSC and scapy.

Run :

Launch bhoreal.pd in Pure Date
sudo python sniffealosc.py

Sniffealosc send led commands as OSC messages to bhoreal.pd

bhoreal.pd is an OSC <-> MIDI translator for Bhoreal.
/bhoreal/in 
/bhoreal/out
/bhoreal/rgb 
/bhoreal/led
 

Termeal is the loloster version that does square colors inside the terminal. Check the arguments there https://github.com/loloster/termeal


