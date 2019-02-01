#!/usr/bin/python
# Check Kamailio Data Load Time Not Old Than 30 Days
# Jack.Su - PLAT-855

import json,datetime,time,os,sys

data_load = json.loads(os.popen("/usr/bin/sudo /usr/sbin/kamctl rpc netsip.stats").read())
uload_time = float(data_load['result']['load_timestamp'])
load_time = datetime.datetime.fromtimestamp(uload_time)
chk_time = datetime.datetime.now() - datetime.timedelta(days=30)
uchk_time = time.mktime(chk_time.timetuple())

if uload_time == '':
	print ("Warning: Kamailio service is reloading, load time is empty.")
	sys.exit(1)
if uload_time < uchk_time:
	print ("Error: age of data load is old than 30 days, data load time is %s" % load_time)
	sys.exit(1)
else:
	print ("OK: data load time is %s" % load_time)
	sys.exit(0)
