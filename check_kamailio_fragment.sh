#! /bin/bash
# Usage: check_kamailio_fragment.sh
# Script to check for 'Free fragment' error message in syslog and alert with warning.
# Jack.Su PLAT-1035

chk_time=$(date -d "15mins ago" +%s)
check_cmd=$(egrep "Free fragment not found" /var/log/syslog| grep -v puppet | tail -n 1 | awk '{print $1" "$2" "$3}')
err_time=$(date -d "$check_cmd" +%s)
show_last10=$(egrep "Free fragment not found" /var/log/syslog| grep -v puppet | tail -n 10)

if [ ! -n "$check_cmd" ]; then
	echo "OK: free fragment error not found"
	exit 0
elif [ "$err_time" -gt "$chk_time" ]; then
	echo '"Free fragment not found" error found!'
	echo $show_last10
	exit 2
else
	echo "OK: free fragment error not found"
	exit 0
fi
