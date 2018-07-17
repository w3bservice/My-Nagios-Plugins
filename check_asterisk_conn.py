#!/usr/bin/python
# Simple script to check some of asterisk connections
# Jack Su - INFRA-614

import sys,os,getopt

def usage():
    print """Usage: check_asterisk_conn.py [-h|--help] [-w|--warning <connections_number>] [-c|--critical <connections_number>\
 [-C|--check Registered|Unregistered|Unregistered-IAX2]"""

def check_reg(warn,crit):
	count = []
	result = os.popen('sudo /usr/sbin/asterisk -rx "sip show registry" | grep -v ^Host | grep -v "\d* SIP registrations." | grep " Registered "')
	res = result.read()
	for line in res.splitlines():
		count.append(line)

	warn = int(warn)
	crit = int(crit)

	if warn < crit:
		usage()
		print ('Parameter inconsistency: "warning connections" is less than "critical connections"!')
		sys.exit(3)

	if len(count) == 0:
		print ("CRITICAL: No registered connection found!")
		sys.exit(2)
	if len(count) < crit:
		print ("CRITICAL: %s Registered connections found, less than %s !" % (len(count),crit))
		sys.exit(2)
	if len(count) < warn:
		print ("WARNING: %s Registered connections found, less than %s !" % (len(count),warn))
		sys.exit(1)
	else:
		print ("OK: %s Registered connections found." % len(count))
		sys.exit(0)

def check_non_reg():
	count = []
	result = os.popen('sudo /usr/sbin/asterisk -rx "sip show registry" | grep -v ^Host | grep -v "\d* SIP registrations." | grep -v " Registered "')
	res = result.read()
	for line in res.splitlines():
		count.append(line)

	if len(count) != 0:
		print ("Error: %s Unregistered connection found!" % len(count))
		sys.exit(1)
	else:
		print ("OK: No Unregistered connection found.")
		sys.exit(0)

def check_non_reg_iax2():
	count = []
	result = os.popen('sudo /usr/sbin/asterisk -rx "iax2 show registry" | grep -v ^Host | grep -v "\d* IAX2 registrations." | grep -v " Registered"')
	res = result.read()
	for line in res.splitlines():
		count.append(line)

	if len(count) != 0:
		print ("Error: %s Unregistered IAX2 connection found!" % len(count))
		sys.exit(1)
	else:
		print ("OK: No Unregistered IAX2 connection found.")
		sys.exit(0)

short_args = "hw:c:C:"
long_args = ["help","check=","warning=","critical="]

try:
    options, args = getopt.getopt(sys.argv[1:], short_args, long_args)
except getopt.GetoptError:
    usage()
    sys.exit(3)

warn_val = 0
crit_val = 0

for name, value in options:
	if name in ("-h", "--help"):
		usage()
		sys.exit(0)
	if name in ("-w", "--warning"):
		warn_val = value
	if name in ("-c", "--critical"):
		crit_val = value
	if name in ("-C", "--check"):
		if value == "Registered":
			check_reg(warn_val,crit_val)
		if value == "Unregistered":
			check_non_reg()
		if value == "Unregistered-IAX2":
			check_non_reg_iax2()
		else:
			usage()
			sys.exit(3)

if len(sys.argv) == 1:
	usage()
	sys.exit(3)
