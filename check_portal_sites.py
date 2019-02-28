#!/usr/bin/python
# Check Portal Websites
# Jack Su - PLAT-807

import sys,urllib2,ssl

portal_sites = ['https://portal.overthewire.com.au/login',
                'https://staging-portal.overthewire.com.au/login',
                'https://portal.faktortel.com.au/login',
                'https://staging-portal.faktortel.com.au/login']

gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
broken_sites = []
good_sites = []

for i in range(0,len(portal_sites)):
	try:
		res = urllib2.urlopen(portal_sites[i], context=gcontext)
	except Exception,e:
		print e
		print ("%s connect failed!" % portal_sites[i])
		sys.exit(2)
	state = res.code
	context = res.readlines()
	if state != 200:
		broken_sites.append(portal_sites[i])
	for li in range(0,len(context)):
		match = '<form class="login-form"' in context[li]
		if match:
			good_sites.append(portal_sites[i])
			break

if len(broken_sites) > 0:
	print("Critical: %s responded not 200!" % broken_sites)
	sys.exit(2)
elif len(good_sites) < len(portal_sites):
	print("Critical: %s login page error!" % set(portal_sites).difference(set(good_sites)))
	sys.exit(2)
else:
	print "OK: All portal sites are available."
	sys.exit(0)
