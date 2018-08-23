#!/usr/bin/python

import sys,json,getopt,requests,socket,memcache,re

def usage():
    print """Usage: check_docker_service.py [-h|--help] [-i|--id service_id] [-k|--key memcache_key] [-v|--value memcache_value]
    Service ID:
    1 - Swarm Deploy Server
    2 - Swarm Deploy Celery
    3 - Optus PAF
    4 - API Gateway
    5 - Docker Proxy
    6 - Wideband
    7 - Job Scheduler
    8 - Redis
    9 - Number Lookup (Netsip)
    9a - Number Lookup (Netsip) TCP Port
    9b - Number Lookup (Netsip) Memcached
    10 - Symbio PAF
    11 - Address to geocode (GNAF)
    12 - Source Production
    13 - Swarm Event Trigger
    16 - logspout
    17 - Source Production Staging
    18 - Docker Node API
    19 - Source Celery
    20 - Optus B2B
    21 - Memcached
    21a - Memcached TCP Port
    22 - BGP Anycast
    23 - Xero API
    sys - system"""

def check_tcp_port(addr,port):
	port = int(port)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	result = sock.connect_ex((addr,port))
	if result == 0:
		print("OK: %s port %d is open" % (addr,port))
		sock.close()
		sys.exit(0)
	else:
		print("Warning: %s port %d is not open" % (addr,port))
		sock.close()
		sys.exit(1)

def check_memcache_key(memcached_server,key,value):
	phone_num = re.compile('^0\d{9}$|^61\d{9}$')
	res = re.search(phone_num, key)
	if res:
		conn = memcache.Client([memcached_server])
		result = conn.get(key)
		if conn.stats == {}:
			print ("%s connect failed!" % memcached_server)
			sys.exit(1)
		else:
			chk_status = json.loads(result)
			chk_key = chk_status['E164_number']
			chk_value = chk_status['CAC']
			if chk_value == value:
				print ("OK: memcached query on specific key. E164_number: %s CAC: %s" % (chk_key,chk_value))
				sys.exit(0)
			else:
				print ("Fail: memcached query on specific key is not match! E164_number: %s CAC: %s" % (chk_key,chk_value))
				sys.exit(1)
	else:
		print ("Error: The mamcache_key you input %s is not a Australian phone number!" % key)
		sys.exit(3)

def check_service(chk_id):
	global headers
	chk_url = "http://swarmdeploy.docker.otw.net.au/api/monitoring/service/%s/" % chk_id
	
	r_session  = requests.Session()
	result = r_session.get(chk_url, headers=headers)
	res = json.loads(result.content)

	service_name = res['name']
	if res['external_health_check_json_response'] == '':
		ext_health_chk = {'status':res['state']}
	else:
		ext_health_chk = json.loads(res['external_health_check_json_response'])
	conf_insync = res['status']['configuration_insync']
	det_scale = res['status']['detected_scale']
	exp_scale = res['status']['expected_scale']
	service_status = ext_health_chk['status']
	if service_status in ("Active", "success"):
		if conf_insync:
			if det_scale != exp_scale:
				print "Error: Service %s, status is %s, detected_scale is %d, expected_scale is %d, not same!" % (service_name,service_status,det_scale,exp_scale)
				sys.exit(2)
			else:
				print "OK: Service %s, status is %s, detected_scale is %d, expected_scale is %d, configuration_insync is %s" % (service_name,service_status,det_scale,exp_scale,conf_insync)
				sys.exit(0)
		else:
			print "Error: Service %s config is not in sync, status is %s" % (service_name,conf_insync)
			sys.exit(2)
	else:
		print "Error: Service %s status is %s" % (service_ame,ext_health_chk)
		sys.exit(2)
	
def check_system():
	global headers
	chk_url = "http://swarmdeploy.docker.otw.net.au/api/monitoring/system/"

	r_session  = requests.Session()
	result = r_session.get(chk_url, headers=headers)
	res = json.loads(result.content)

	exp_nodes = res['nodes']['expected_nodes']
	det_nodes = res['nodes']['detected_nodes']
	nodes = []
	for i in range(0,len(res['bgp'])):
		nodes.append(res['bgp'][i]['hostname'])
	nodes_name = json.dumps(nodes, ensure_ascii=False)

	if exp_nodes == det_nodes:
		print "OK: expected_nodes is %d, detected_nodes is %d, nodes: %s" % (exp_nodes,det_nodes,nodes_name)
		sys.exit(0)
	else:
		print "Error: expected_nodes is %d, detected_nodes is %d, nodes: %s" % (exp_nodes,det_nodes,nodes_name)
		sys.exit(2)

def main():	
	short_args = "hk:v:i:"
	long_args = ["help","key=","value=","id="]
	
	try:
		options, args = getopt.getopt(sys.argv[1:], short_args, long_args)
	except getopt.GetoptError:
		usage()
		sys.exit(3)

	for name, value in options:
		if name in ("-h", "--help"):
			usage()
			sys.exit(0)
		if name in ("-k", "--key"):
			memcache_key = value
		if name in ("-v", "--value"):
			memcache_value = value
		if name in ("-i","--id"):
			chk_id = value
		
	if len(sys.argv) == 1:
		usage()
		sys.exit(3)
	
	service_id = ["1","2","3","4","5","6","7","8","9","9a","9b","10","11","12","13","16","17","18","19","20","21","21a","22","23","sys"]
	if chk_id not in service_id:
		print "Service ID not found!"
		sys.exit(3)
	if chk_id == "9a":
		chk_port = 8008
		chk_addr = "numown.docker.otw.net.au"
		check_tcp_port(chk_addr,chk_port)
	if chk_id == "9b":
		memcached_server = "numown.docker.otw.net.au:8008"
		check_memcache_key(memcached_server,memcache_key,memcache_value)
	if chk_id == "21a":
		chk_port = 11211
		chk_addr = "memcache.docker.otw.net.au"
		check_tcp_port(chk_addr,chk_port)
	if chk_id == "sys":
		check_system()
	else:
		check_service(chk_id)
		
if __name__ == "__main__":
	headers = {
    		'Contert-Type':"application/json",
    		'Authorization': "token XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
	}
	main()
