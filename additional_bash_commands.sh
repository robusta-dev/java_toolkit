alias get_java_pid='ps aux | grep java | grep -v grep | cut -d" " -f6'
alias push_jdk='mkdir -p /proc/$(ps aux | grep java | grep -v grep | cut -d" " -f6)/cwd/mnt/robusta;\
cp -r /app/openjdk /proc/$(ps aux | grep java | grep -v grep | cut -d" " -f6)/cwd/mnt/robusta'
alias cleanup='rm -r /proc/$(ps aux | grep java | grep -v grep | cut -d" " -f6)/cwd/mnt/robusta'
alias podns_shell='nsenter -t $(ps aux | grep java | grep -v grep | cut -d" " -f6) -m -p /bin/sh'

function nsjdk(){
	local NSENTER_CMD='nsenter -t $(ps aux | grep java | grep -v grep | cut -d" " -f6) -m -p /mnt/robusta/openjdk/bin/'
	COMMAND=""
	if [ "$1" = "jmap" ]; then COMMAND="jmap $2";
	elif [ "$1" = "jstack" ]; then COMMAND="java-toolkit jstack $2";
	elif [ "$1" = "-h" ];
		then
			echo 'Usages:'
			echo 'nsjdk jmap LOCAL_PROCESS_PID'
			echo 'nsjdk jstack LOCAL_PROCESS_PID'
			return
	else
		echo "'Unrecognized command $1 for help run 'nsjdk -h'"
		return
	fi
	echo push_jdk
  eval push_jdk
	local FULL_COMMAND="$NSENTER_CMD$COMMAND"
	echo $FULL_COMMAND
	eval $FULL_COMMAND
	echo cleanup
	eval cleanup
}