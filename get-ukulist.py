#!/usr/bin/env python
#coding=utf-8
# requires tld

import urllib2
import re
import os
import shutil
import stat
import sys
import tempfile
import time
import tld

mydnsip = '114.114.114.114'
mydnsport = '53'
myipset = 'uku'

if len(sys.argv) != 4:
    sys.stderr.write("Usage: "+sys.argv[0]+" server.conf ipset.conf ipset.sh\n")
    sys.exit(0)

server_file = tempfile.mkstemp()[1]
ipset_conf_file = tempfile.mkstemp()[1]
ipset_sh_file = tempfile.mkstemp()[1]

server_fs = open(server_file, 'w')
ipset_conf_fs = open(ipset_conf_file, 'w')
ipset_sh_fs = open(ipset_sh_file, 'w')

baseurl = 'https://raw.githubusercontent.com/Unblocker/Unblock-Youku/master/shared/urls.js'
comment_pattern = '^\s*\/\/.*$'
valid_pattern = '\s*["\']https?://[\*\-\w\.]*/'
domain_pattern = '([\w\-\_]+\.[\w\.\-\_]+)[\/\*]*'
ip_pattern = '(?:[0-9]{1,3}\.){3}[0-9]{1,3}'

info_str = '# updated on ' + time.strftime("%Y-%m-%d %H:%M:%S %Z", time.localtime()) + '\n'
server_fs.write(info_str)
ipset_conf_fs.write(info_str)
ipset_sh_fs.write(info_str)

content = urllib2.urlopen(baseurl, timeout=15).read()

# remember all blocked domains, in case of duplicate records
domainlist = []

for line in content.splitlines():
    comment_found = re.findall(comment_pattern, line)
    if comment_found:
        continue
    domain_found = re.findall(valid_pattern, line)
    if domain_found:
        ip_found = re.findall(ip_pattern, domain_found[0])
        if ip_found:
            is_ip = True
            domain = ip_found[0]
        else:
            is_ip = False
            domain = re.findall(domain_pattern, domain_found[0])
            domain = domain[0]
        try:
            found = domainlist.index(domain)
        except ValueError:
            domainlist.append(domain)
            if is_ip:
                ipset_sh_fs.write('ipset add %s %s\n'%(myipset,domain))
            else:
                server_fs.write('server=/%s/%s#%s\n'%(domain,mydnsip,mydnsport))
                ipset_conf_fs.write('ipset=/%s/%s\n'%(domain,myipset))

server_fs.close()
ipset_conf_fs.close()
ipset_sh_fs.close()

os.chmod(server_file,stat.S_IRUSR|stat.S_IWUSR|stat.S_IRGRP|stat.S_IWGRP|stat.S_IROTH)
os.chmod(ipset_conf_file,stat.S_IRUSR|stat.S_IWUSR|stat.S_IRGRP|stat.S_IWGRP|stat.S_IROTH)
os.chmod(ipset_sh_file,stat.S_IRUSR|stat.S_IWUSR|stat.S_IRGRP|stat.S_IWGRP|stat.S_IROTH)

shutil.move(server_file, sys.argv[1])
shutil.move(ipset_conf_file, sys.argv[2])
shutil.move(ipset_sh_file, sys.argv[3])

