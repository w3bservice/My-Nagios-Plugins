#!/usr/bin/python

import sys,os,getopt

def usage():
    print """Usage: check_asterisk_conn.py [-h|--help] [-c|--check Registered|Non-Registered|Non-Registered-IAX2]"""

def check_reg():
	count = []
	result = os.popen('sudo /usr/sbin/asterisk -rx "sip show registry" | grep -v ^Host | grep -v "\d* SIP registrations." | grep " Registered "')
	res = result.read()
	for line in res.splitlines():
		count.append(line)

	if len(count) == 0:
		print ("CRITICAL: No registered connection found!")
		sys.exit(0)
	elif len(count) < 10:
		print ("WARNING: %s Registered connections found, less than 10!" % len(count))
		sys.exit(1)
	else:
		print ("OK: %s Registered connections found." % len(count))
		sys.exit(0)

def check_non_reg():
	result = os.system('sudo /usr/sbin/asterisk -rx "sip show registry" | grep -v ^Host | grep -v "\d* SIP registrations." | grep -v " Registered "')

	if result == 0:
		print ("Error: Non-registered connection found!")
		sys.exit(1)
	else:
		print ("OK: No non-registered connection found.")
		sys.exit(0)

def check_non_reg_iax2():
	result = os.system('sudo /usr/sbin/asterisk -rx "iax2 show registry" | grep -v ^Host | grep -v "\d* IAX2 registrations." | grep -v " Registered "')

	if result == 0:
		print ("Error: Non-registered IAX2 connection found!")
		sys.exit(1)
	else:
		print ("OK: No non-registered IAX2 connection found.")
		sys.exit(0)

short_args = "hc:"
long_args = ["help","check="]

try:
    options, args = getopt.getopt(sys.argv[1:], short_args, long_args)
except getopt.GetoptError:
    usage()
    sys.exit(3)

for name, value in options:
	if name in ("-h", "--help"):
		usage()
		sys.exit(0)
	if name in ("-c", "--check"):
		if value == "Registered":
			check_reg()
		if value == "Non-Registered":
			check_non_reg()
		if value == "Non-Registered-IAX2":
			check_non_reg_iax2()
		else:
			usage()
			sys.exit(3)

if len(sys.argv) == 1:
	usage()
	sys.exit(3)
