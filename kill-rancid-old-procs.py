#!/usr/bin/python
# Finds rancid user ssh or telnet processes that have run for more than 10 min then kills them
# Jack.Su -- PLAT-990

import os,sys,signal

def kill(pid):
    try:
        a = os.kill(pid,signal.SIGKILL)
        print ("Process %s killed" % pid)
    except Exception as ee:
        print("Process not exist!")

if __name__ == '__main__':
	pss = os.popen("ps -u rancid -o %c%p%t|egrep '^ssh|^telnet'").read().split()

	for i in range(0,len(pss)/3):
		if len(pss[i*3+2]) > 5:
			kill(int(pss[i*3+1]))
		elif len(pss[i*3+2]) == 5 and int(pss[i*3+2].split(":")[0]) > 10:
			kill(int(pss[i*3+1]))
