#!/usr/bin/python
# -*- coding: utf-8 -*
# check_mysql_slave.py - Check MySQL slave and replication stauts.
# Jack Su - INFRA-532|INFRA-664

import os,sys,getopt,socket

def usage():
    print """Usage: check_mysql_slave.py [-h] [-H hostname or ipaddr] [-u username] [-p password]\
 [-w seconds] [-c seconds]"""

allargs = "hH:u:p:w:c:"

try:
    options, args = getopt.getopt(sys.argv[1:],allargs)
except getopt.GetoptError:
    usage()
    sys.exit(3)

warn_val = 0
crit_val = 0

for name, value in options:
	if name == "-h":
		usage()
		sys.exit(0)
	elif name == "-H":
		host = value
	elif name == "-u":
		username = value
	elif name == "-p":
		passwd = value
	elif name == "-w":
		warn_val = value
	elif name == "-c":
		crit_val = value

if len(sys.argv) == 1:
	usage()
	sys.exit(3)

warn_val = int(warn_val)
crit_val = int(crit_val)

if warn_val > crit_val:
	usage()
	print ('Parameter inconsistency: "warning time" is greater than "critical time"!')
	sys.exit(3)

mysqlbase='/usr/bin/mysql'

testdb = os.system(mysqlbase + ' -h %s -u%s -p%s -e exit' % (host, username, passwd))
if testdb != 0:
	print ('Connect MySQL DB failed! - Check your username or password')
	sys.exit(3)

info = os.popen(mysqlbase + ' -h %s -u%s -p%s -e "show slave status\G"|grep -E\
 "Master_Host|Slave_IO_Running|Slave_SQL_Running|Seconds_Behind_Master|Master_Log_File|Read_Master_Log_Pos|Seconds_Behind_Master|Last_Errno"'\
 % (host, username, passwd)).read()
info_list = info.split()
info_tup = {}
js = 0
_idx = 0
pd = len(info_list) / 2
for idx, item in enumerate(info_list):
    js += 1
    if js > pd:
        continue
    info_tup[info_list[_idx]] = info_list[_idx + 1]
    _idx += 2

hostname = os.popen("/bin/hostname -f").read().strip('\n')
slave_sec = int(info_tup['Seconds_Behind_Master:'])

if info_tup['Slave_IO_Running:'] != 'Yes' or info_tup['Slave_SQL_Running:'] != 'Yes':
	print ("Critical: %s MySQL Master-Slave status: Down " % (hostname) + str(info_list))
	sys.exit(2)
if warn_val == 0 and crit_val == 0:
	print ("OK: %s MySQL Master-Slave status: "% (hostname) + str(info_list))
	sys.exit(0)
if slave_sec > crit_val:
	print ("Critical: Seconds Behind Master large than %s Seconds," % str(crit_val)\
	+ " Seconds_Behind_Master is: " + info_tup['Seconds_Behind_Master:']) 
	sys.exit(2)
if slave_sec > warn_val:
	print ("Warning: Seconds Behind Master large than %s Seconds," % str(warn_val)\
	+ " Seconds_Behind_Master is: " + info_tup['Seconds_Behind_Master:']) 
	sys.exit(1)
else:
	print ("OK: %s MySQL Master-Slave status: "% (hostname) + str(info_list))
	sys.exit(0)
