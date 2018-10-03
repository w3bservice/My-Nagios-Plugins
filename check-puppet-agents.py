#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Check the list of puppet agents who had not talk to server more than 1 week
# Jack Su - INFRA-642,PLAT-767

import os,datetime,re

def get_ndays_ago(n):
    today = datetime.date.today()
    old_day = today - datetime.timedelta(n)
    Date = old_day.strftime("%Y-%m-%d")
    return Date

weekago = get_ndays_ago(7)

base_dir = '/var/lib/puppet/reports'
dir_list = os.listdir(base_dir)

dirlist = []
info = {}
for i in range(0, len(dir_list)):
    path = os.path.join(base_dir,dir_list[i])
    if os.path.isdir(path):
        dirlist.append(dir_list[i])

for i in range(0, len(dirlist)):
    path = os.path.join(base_dir,dirlist[i])
    if os.path.isfile(path):
        continue
    timestamp = os.path.getmtime(path)
    date = datetime.datetime.fromtimestamp(timestamp)
    dir_mtime = date.strftime("%Y-%m-%d")
    if dir_mtime < weekago:
        info.update({dirlist[i]:dir_mtime})

sort_info = sorted(info.items(),key = lambda item:item[1])
tmpfile = '/tmp/check-agents.tmp'
wrtmp = open(tmpfile, 'w')
for i in range(0, len(sort_info)):
    print (sort_info[i][1],sort_info[i][0],file=wrtmp)

nodes_pp = "/etc/puppet/code/environments/production/manifests/nodes.pp"
nodes_file = open(nodes_pp,"r")
nodes_file_lines = nodes_file.readlines()
nodes_list = []

for line in nodes_file_lines:
	nodeline = re.compile(r'^\s*node.*')
	node_line = nodeline.match(line)
	if node_line:
		nodes_list.append(line.split(" ")[1].strip("\'"))

nodes_file.close()

for i in range(0,len(dir_list)):
	if dir_list[i] not in nodes_list:
		print ("Not in nodes.pp %s" % dir_list[i] ,file=wrtmp)
for i in range(0,len(nodes_list)):
	if nodes_list[i] not in dir_list:
		print ("No report %s" % nodes_list[i] ,file=wrtmp)

wrtmp.close()

mailto = "jack.su@overthewire.com.au, jason.bingham@overthewire.com.au, john.mizuno@overthewire.com.au"
os.popen('/usr/bin/mail -s "Weekly puppet agents check" ' + '%s < %s' % (mailto, tmpfile)) 

#os.remove(tmpfile)
