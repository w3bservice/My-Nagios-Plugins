#!/usr/bin/python3
# -*- coding:utf-8 -*-
# Check the list of puppet agents who had not talk to server more than 1 week
# Jack Su - INFRA-642

import os,datetime

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
wrtmp.close()

mailto = "jack.su@overthewire.com.au, jason.bingham@overthewire.com.au"
os.popen('/usr/bin/mail -s "Weekly puppet agents check" ' + '%s < %s' % (mailto, tmpfile)) 

#os.remove(tmpfile)
