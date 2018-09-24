#!/usr/bin/python
# Check client access NAT server

import urllib2,sys

url="http://abc.com/"

try:
	res = urllib2.urlopen(url)
except Exception,e:
	print e
	sys.exit(2)

reslines = res.readlines()
resdict = {}

for i in range(0,len(reslines)):
	key = reslines[i].strip("\n").split(" ")[0]
	value = reslines[i].strip("\n").split(" ")[1]
	resdict[key] = value
	i += 1

invalid_clients = int(resdict['nat_gateway_containers{state="running",configuration="invalid"}'])
stopped_clients = int(resdict['nat_gateway_containers{state="stopped"}'])
running_clients = int(resdict['nat_gateway_containers{state="running",configuration="valid"}'])
ppp_sessions = int(resdict['nat_gateway_ppp_sessions'])
healthcheck = int(resdict['nat_gateway_bgp_healthcheck'])
neighbour_down = int(resdict['nat_gateway_bgp_neighbour{state="down",neighbour_ip="XXX.XXX.XXX.XXX"}'])

if invalid_clients > 0:
	print ("Error: %s invalid containers found!" % invalid_clients)
	sys.exit(2)
if stopped_clients > 0:
	print ("Error: %s stopped containers found!" % stopped_clients)
	sys.exit(2)
if running_clients != ppp_sessions:
	print ("Error: Running containers is not same as ppp_sessions! Running containers is %s, ppp_sessions is %s" % (running_clients,ppp_sessions))
	sys.exit(2)
if healthcheck == 0:
	print ("Error: bgp healthcheck failed!")
	sys.exit(2)
if neighbour_down > 0:
	print ("Error: %s down neighbour found!" % neghbour_down)
	sys.exit(2)
else:
	print ("OK: All clients access NAT server good!")
	sys.exit(0)
