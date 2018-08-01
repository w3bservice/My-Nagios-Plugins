#!/usr/bin/python
# check_docker_swarm.py - Check Docker Swarm Services
# Jack Su - INFRA-674|INFRA-682

import sys,json,getopt,requests,socket,memcache

def check_http_status(addr,obj):
	result = requests.get(addr)
	chk_status = json.loads(result.text)
	stat =  chk_status['status']
	if stat not in ("ok","success"):
		print ("Warning: %s status is %s" % (obj,stat))
		sys.exit(1)
	else:
		print ("OK: %s status is %s" % (obj,stat))
		sys.exit(0)
	
def check_tcp_port(addr,port):
	port = int(port)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = sock.connect_ex((addr,port))
	if result == 0:
		print("%s port %d is open" % (addr,port))
		sock.close()
		sys.exit(0)
	else:
		print("%s port %d is not open" % (addr,port))
		sock.close()
		sys.exit(1)

def check_memcache_key(memcached_server,key,value):
	conn = memcache.Client([memcached_server])
	result = conn.get(key)
	chk_status = json.loads(result)
	chk_key = chk_status['E164_number']
	chk_value = chk_status['CAC']
	if chk_value == value:
		print ("OK: memcached query on specific key. E164_number: %s CAC: %s" % (chk_key,chk_value))
		sys.exit(0)
	else:
		print ("Fail: memcached query on specific key is not match! E164_number: %s CAC: %s" % (chk_key,chk_value))
		sys.exit(1)

def usage():
    print """Usage: check_docker_swarm.py [-h] [-k memcache_key] [-v memcache_value]\
 [-C swarmdeploy|optuspaf|apigateway|wideband|symbiopaf|gnaf|source|optusb2b|numown|memcache]numown_memcache]"""


def main():
	allargs = "hk:v:C:"

	try:
		  options, args = getopt.getopt(sys.argv[1:],allargs)
	except getopt.GetoptError:
			usage()
			sys.exit(3)

	for name, value in options:
		if name == "-h":
			usage()
			sys.exit(0)
		if name == "-k":
			memcache_key = value
		if name == "-v":
			memcache_value = value
		if name == "-C":
			if value == "swarmdeploy":
				chk_obj = value
				chk_addr = "http://swarmdeploy.docker.otw.net.au/healthcheck/"
				check_http_status(chk_addr,chk_obj)
			if value == "optuspaf":
				chk_obj = value
				chk_addr = "http://optuspaf.docker.otw.net.au/healthcheck/"
				check_http_status(chk_addr,chk_obj)
			if value == "apigateway":
				chk_obj = value
				chk_addr = "http://apigateway.docker.otw.net.au:8877/healthcheck/"
				check_http_status(chk_addr,chk_obj)
			if value == "wideband":
				chk_obj = value
				chk_addr = "http://wideband.docker.otw.net.au/healthcheck/"
				check_http_status(chk_addr,chk_obj)
			if value == "symbiopaf":
				chk_obj = value
				chk_addr = "http://symbiopaf.docker.otw.net.au/healthcheck/"
				check_http_status(chk_addr,chk_obj)
			if value == "gnaf":
				chk_obj = value
				chk_addr = "http://gnaf.docker.otw.net.au:8500/healthcheck/"
				check_http_status(chk_addr,chk_obj)
			if value == "source":
				chk_obj = value
				chk_addr = "http://source.overthewire.com.au/healthcheck/"
				check_http_status(chk_addr,chk_obj)
			if value == "optusb2b":
				chk_obj = value
				chk_addr = "http://optusb2b.docker.overthewire.net.au/healthcheck/"
				check_http_status(chk_addr,chk_obj)
			if value == "numown":
				chk_port = 8008
				chk_addr = "numown.docker.otw.net.au"
				check_tcp_port(chk_addr,chk_port)
			if value == "memcache":
				chk_port = 11211
				chk_addr = "memcache.docker.otw.net.au"
				check_tcp_port(chk_addr,chk_port)
			if value == "numown_memcache":
				chk_addr = "numown.docker.otw.net.au:8008"
				check_memcache_key(chk_addr,memcache_key,memcache_value)
			else:
				usage()
				sys.exit(3)

	if len(sys.argv) == 1:
		usage()
		sys.exit(3)

if __name__ == "__main__":
	main()
