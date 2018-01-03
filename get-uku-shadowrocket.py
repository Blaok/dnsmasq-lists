#!/usr/bin/python3
import requests  
import re

pac=requests.get('https://pac.uku.im/pac.pac').text  
rexp='\,\"([a-z].+?[a-z])\"\:'  
sites=re.findall(rexp,pac)
sites = dict.fromkeys(sites).keys()

conf='''
[General]
bypass-system = false
skip-proxy = 
bypass-tun = 
dns-server = 

[Rule]

# blknet
IP-CIDR,7.0.0.0/8,PROXY
IP-CIDR,10.1.0.0/16,PROXY
IP-CIDR,10.10.0.0/16,PROXY

# UCLA
DOMAIN-SUFFIX,.cs.ucla.edu,PROXY
DOMAIN-SUFFIX,.seas.ucla.edu,PROXY
DOMAIN,cdsc0.cs.ucla.edu,DIRECT
DOMAIN,scorpio.cs.ucla.edu,DIRECT
DOMAIN,lion.cs.ucla.edu,DIRECT

# Youku
USER-AGENT,Youku*,ARC,force-remote-dns
DOMAIN-KEYWORD,.youku.com,ARC,force-remote-dns
DOMAIN-SUFFIX,.ykimg.com,ARC,force-remote-dns
IP-CIDR,103.41.140.0/22,ARC,force-remote-dns
IP-CIDR,106.11.0.0/16,ARC,force-remote-dns

'''
for site in sites:
    rule='DOMAIN,'+site+',ARC,force-remote-dns\n'
    conf+=rule

conf+='''
[Host]
localhost = 127.0.0.1
'''

print(conf)

