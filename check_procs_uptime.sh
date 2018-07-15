#!/bin/bash
# INFRA-615
# Check process older than 24 hours - Jack.Su

# Usage
if [ $# != 1 ]; then
echo "Usage: $0  <PROCESS WITH FULL PATH>"
echo "Example: $0  /use/sbin/sshd"
exit 3
fi

PROC=$1

#GET PID
CMD="ps -eo pid,etime,cmd|grep $PROC |grep -v $0 |grep -v grep |awk '{ print \$1 }'|head -n1"
P=`eval $CMD`

if [ -z $P ];then
	echo "UNKOWN - $PROC PID $P not found"
	exit 3
fi

#GET UPTIME 
TIME=`ps -p $P -o etime=`

if [ -z $TIME ];then
	echo "UNKOWN - $PROC PID $P utime $TIME not found"
	exit 3
fi

# GET DAYS (ONLY IF THERE)
if [[ $TIME == *"-"* ]]
then
	D=`echo $TIME|awk -F"-" '{ print $1 }'`
	H=`echo $TIME|awk -F"-" '{ print $2 }'`
	echo "$PROC running more than 24HRS, running time is $D days $H"
	exit 2
else
	echo "Process $P $PROC uptime is $TIME"
fi
