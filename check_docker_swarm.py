#!/usr/bin/python

import os,sys,json,getopt

def check_http_status(addr,obj):
	get_http = "/usr/bin/curl"
	result = os.popen(get_http + ' -s %s/healthcheck/' % addr).read()
	chk_status = json.loads(result)
	stat =  chk_status['status']
	if stat not in ("ok","success"):
		print ("Warning: %s status is %s" % (obj,stat))
		sys.exit(1)
	else:
		print ("OK: %s status is %s" % (obj,stat))
		sys.exit(0)
	
def usage():
    print """Usage: check_docker_swarm.py [-h] [-C swarmdeploy|optuspaf|apigateway|wideband|symbiopaf|gnaf|source|optusb2b]"""


def main():
	allargs = "hC:"

	try:
		  options, args = getopt.getopt(sys.argv[1:],allargs)
	except getopt.GetoptError:
			usage()
			sys.exit(3)

	for name, value in options:
		if name == "-h":
			usage()
			sys.exit(0)
		if name == "-C":
			if value == "swarmdeploy":
				chk_obj = value
				chk_addr = "http://swarmdeploy.docker.otw.net.au"
				check_http_status(chk_addr,chk_obj)
			if value == "optuspaf":
				chk_obj = value
				chk_addr = "http://optuspaf.docker.otw.net.au"
				check_http_status(chk_addr,chk_obj)
			if value == "apigateway":
				chk_obj = value
				chk_addr = "http://apigateway.docker.otw.net.au:8877"
				check_http_status(chk_addr,chk_obj)
			if value == "wideband":
				chk_obj = value
				chk_addr = "http://wideband.docker.otw.net.au"
				check_http_status(chk_addr,chk_obj)
			if value == "symbiopaf":
				chk_obj = value
				chk_addr = "http://symbiopaf.docker.otw.net.au"
				check_http_status(chk_addr,chk_obj)
			if value == "gnaf":
				chk_obj = value
				chk_addr = "http://gnaf.docker.otw.net.au:8500"
				check_http_status(chk_addr,chk_obj)
			if value == "source":
				chk_obj = value
				chk_addr = "http://source.overthewire.com.au"
				check_http_status(chk_addr,chk_obj)
			if value == "optusb2b":
				chk_obj = value
				chk_addr = "http://optusb2b.docker.overthewire.net.au"
				check_http_status(chk_addr,chk_obj)
			else:
				usage()
				sys.exit(3)

	if len(sys.argv) == 1:
		usage()
		sys.exit(3)

if __name__ == "__main__":
	main()
