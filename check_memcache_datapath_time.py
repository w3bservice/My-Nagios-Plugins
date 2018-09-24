#!/usr/bin/python

import memcache,sys,datetime

memcache_server="numown.docker.otw.net.au:8008"

conn = memcache.Client([memcache_server])
status = conn.get_stats()
if status == []:
	print ("%s connect failed!" % memcached_server)
	sys.exit(1)
else:
	datapath_timestamp = float(status[0][1]['datapath'])
	datapath_time = datetime.datetime.fromtimestamp(datapath_timestamp)
	chk_time = datetime.datetime.now() - datetime.timedelta(days=1)
	exist_time = (str(datetime.datetime.now() - datapath_time)).split(".")[0]

	if chk_time < datapath_time:
		print ("OK: datapath time is %s" % exist_time)
		sys.exit(0)
	else:
		print ("Error: datapath time is %s" % exist_time)
		sys.exit(2)
