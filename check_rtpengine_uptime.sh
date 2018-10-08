#!/bin/bash
# check_rtpengine_uptime.sh - Check RTPEngine uptime
# Jack Su - INFRA-651

UPTIME=$(sudo /usr/sbin/rtpengine-ctl list totals|grep Uptime|cut -f2 -d':' | cut -f1 -d' ')

if [ "$UPTIME" = "" ]; then
		echo "RTPEngine is not running."
		exit 2
fi

UPTIME_DAYS=$(expr $UPTIME \/ 24 \/ 60 \/ 60)
UPTIME_HOURS=$(expr $UPTIME \/ 60 \/ 60 \- $UPTIME_DAYS \* 24)
UPTIME_MINS=$(expr $UPTIME \/ 60 \- $UPTIME_HOURS \* 60 \- $UPTIME_DAYS \* 24 \* 60)

if [ "$UPTIME" -le "900" ]; then
  echo "CRITICAL: RTPEngine uptime is $UPTIME_MINS minutes"
  exit 2
elif [ "$UPTIME" -le "1800" ]; then
    echo "WARNING: RTPEngine uptime is $UPTIME_HOURS hours, $UPTIME_MINS minutes"
    exit 1
elif [ "$UPTIME" -gt "1800" ]; then
  echo "OK: RTPEngine uptime is $UPTIME_DAYS days, $UPTIME_HOURS hours, $UPTIME_MINS minutes"
  exit 0
else
  echo "CRITICAL: RTPEngine uptime is $UPTIME"
  exit 2
fi

