heck Kamailio Data Load Time Not Old Than 30 Days
# Jack.Su - PLAT-855

import json,datetime,os,sys

data_load = json.loads(os.popen("/usr/sbin/kamctl rpc netsip.stats").read())
load_time = data_load['result']['load_timestamp']
chk_time = (datetime.datetime.now() - datetime.timedelta(days=30)).strftime("%Y%m%d%H%M%S")

if load_time > chk_time:
	print ("Error: age of data load is old than 30 days, data load time is %s" % load_time)
	sys.exit(2)
else:
	print ("OK: data load time is %s" % load_time)
	sys.exit(0)
