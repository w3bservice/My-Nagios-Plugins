#!/usr/bin/python
#check_log_mysql.py - Check "Out of memory" error for mysql
#Jack.su - INFRA-618

import sys,os,re

log_file = '/var/log/syslog'
tmp_file = '/tmp/tmplog'

if not os.path.exists(log_file):
    print("Log file not found!")
    sys.exit(1)

logfile = open(log_file,"r")
loglines = logfile.readlines()
old_count = 0

if os.path.exists(tmp_file):
  old_count = os.popen('wc -l %s' % tmp_file).read().split()[0]
  old_count = int(old_count)  

tmpfile = open(tmp_file,"w")

for line in loglines:
    mysqldlog = re.compile(r'(.*)mysqld(.*)Out of memory(.*?).*')
    match = mysqldlog.match(line)
    if match:
	tmpfile.write(line)
		
tmpfile.close()
logfile.close()

new_count = os.popen('wc -l %s' % tmp_file).read().split()[0]
new_count = int(new_count)

if (new_count != old_count and new_count != 0):
    print('Error: Mysql out of memory found!')
    sys.exit(2)
elif new_count == 0:
    print("OK: No error found!")
    sys.exit(0)
else:
    print("OK: No error found!")
    sys.exit(0)
