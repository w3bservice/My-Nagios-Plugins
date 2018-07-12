#!/usr/bin/python
#check_log_mysql.py - Check "Out of memory" error for mysql
#Jack.Su - INFRA-618
#User nagios must have premission to access /var/log/syslog

import subprocess,os,sys

logfile = "/var/log/syslog"
tmpfile = "/tmp/tmplog.mysqld"

if not os.path.exists(logfile):
    print("Log file not found!")
    sys.exit(1)

old_count = 0
if os.path.exists(tmpfile):
  old_count = os.popen('wc -l %s' % tmpfile).read().split()[0]
  old_count = int(old_count) 

class Shell(object) :
 def runCmd(self, cmd) :
  res = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
  sout ,serr = res.communicate() 
  return res.returncode, sout, serr, res.pid

log = open(logfile, 'r')
tmp = open(tmpfile, 'w')

shell = Shell()
result = shell.runCmd('egrep -a "(.*)mysqld(.*)Out of memory(.*)" ' + logfile)
tmp.write(result[1])

tmp.close()
log.close()

new_count = os.popen('wc -l %s' % tmpfile).read().split()[0]
new_count = int(new_count)

if (new_count != old_count and new_count != 0):
    print('Error: Mysql out of memory found!')
    errmsg = shell.runCmd('tail -n 1 ' + tmpfile)
    print(errmsg[1])
    sys.exit(2)
else:
    print("OK: No error found!")
    sys.exit(0)
