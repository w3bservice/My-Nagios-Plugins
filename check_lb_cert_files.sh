#!/bin/bash
# check_lb_cert_files.sh
# Desc: Check for crt files that have not been modified in more than 70 dates
# See: INFRA-608

DIR=/etc/kamailio/tls
WARN_DAYS=70
CRIT_DAYS=83
error=0

if [ -d $DIR ]; then
   for i in `find $DIR -type f -name '*.net.au.crt' -mtime +${CRIT_DAYS}`;
     do
        echo "Critical! stale file found, more than ${CRIT_DAYS} days: " $i
        let error=2
     done

     if [[ $error = 2 ]]; then
 	exit ${error}

     else
        for ii in `find $DIR -type f -name '*.net.au.crt' -mtime +${WARN_DAYS}`;
        do
          echo "Warning! stale file found, more than ${WARN_DAYS} days: " $ii
          let error=1
        done
    fi

else
  echo "Directory not found: $DIR"
  exit 1
fi

if [ $error = 0 ]; then
  echo "No stale files found."
  exit ${error}
else
  exit ${error}
fi

