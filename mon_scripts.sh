#!/bin/bash

# sleep for 60 seconds
SLEEP_TIME=60

ROTATE_TIME="00:00"
OUT_PREFIX=$(date "+%Y-%m-%d%Z%H:%M:%S")

function format-out-files(){
	PS_MON_OUT="ps_mon.out.${OUT_PREFIX}"
	VMSTAT_MON_OUT="vmstat_mon.out.${OUT_PREFIX}"
	TOP_MON_OUT="top.out.${OUT_PREFIX}"
	MPSTAT_MON_OUT="mpstat.out.${OUT_PREFIX}"
	PIDSTAT_MON_OUT="pidstat.out.${OUT_PREFIX}"
	echo > $PS_MON_OUT
	echo > $VMSTAT_MON_OUT
	echo > $TOP_MON_OUT
	echo > $MPSTAT_MON_OUT
	echo > $PIDSTAT_MON_OUT
}

format-out-files

while true
do

	if [[ $ROTATE_TIME == $(date "+%H:%M") ]]; 
	then
		OUT_PREFIX=$(date "+%Y-%m-%d%Z%H:%M:%S")
		format-out-files
	fi

	uptime_str=$(uptime)
	echo "$(date "+%Y-%m-%d"): $uptime_str"
	# load_avg=$(echo $uptime_str|cut -d "," -f 4|cut -d ":" -f 2|sed s/[[:space:]]//g)
	load_avg=$(echo $uptime_str | awk -F' *,? *' '{print $(NF-2)}')
	# while [ $i -le "$LIMIT" ];
	# lavg=$((load_avg+0))
	if [[ "${load_avg%.*}" -ge "2" ]];
	then
			date >> $PS_MON_OUT;
			ps -eLf >> $PS_MON_OUT;
			date >> $VMSTAT_MON_OUT;
			vmstat 5 12 >> $VMSTAT_MON_OUT & 
			top -bc -d 30 -n 6 >> $TOP_MON_OUT 2>&1 &
			mpstat -P ALL 5 2 >> $MPSTAT_MON_OUT 2>&1 &
			pidstat -duIl 5 2 >> $PIDSTAT_MON_OUT 2>&1 &
	fi
	sleep $SLEEP_TIME;
done

# sudo bash linmon.sh > linmon.out 2>&1 &
# sudo bash linmon.sh > linmon.out.$(date "+%Y-%m-%d%Z%H:%M:%S") 2>&1 &
