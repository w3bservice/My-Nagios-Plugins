#!/usr/bin/python
#check_lcr_error.py -- check netsip LCR hosts kamailio errors
#Jack.Su -- PLAT-961

import os,json,sys,re

cmd = "/usr/bin/sudo /usr/sbin/kamctl stats netsip"
netsip_stats = json.loads(os.popen(cmd).read())
err_dic = {}
error = 0

for i in range(0, len(netsip_stats['result'])):
	err_var = re.match(r'(.*)error(.*)', netsip_stats['result'][i].split(" = ")[0], re.I)
	if err_var:
		err_dic[netsip_stats['result'][i].split(" = ")[0]] = netsip_stats['result'][i].split(" = ")[1]
	i += 1

for key in err_dic:
	if err_dic[key] != "0":
		print "Warning: LCR error found!", key, "is", err_dic[key]
		error += 1

if error != 0:
	sys.exit(1)
else:
	print "OK: LCR check ok!"
	sys.exit(0)
