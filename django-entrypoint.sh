#!/bin/sh

pid=0
_exit=0

shutdown() {
    echo "Got signal ${*}" >&2
    _exit=1
    if [ 0 -ne ${pid} ]
    then
        kill "-${1:-INT}" ${pid}
	case "${1:-INT}" in
	"HUP"|"FPE"|"SEGV"|"USR1"|"USR2")
	    echo "Non terminal signal received." >&2
	    _exit=0
	    ;;
	*)
	    echo "Waiting for child process ${pid} to exit." >&2
	    wait ${pid}
	    echo "Child exited. Bye." >&2
	    exit 0
	    ;;
	esac
    else
	echo "No specific child PID known. Terminating all." >&2
	killall -INT
	echo "Waiting for all children to exit." >&2
	wait
	exit 1
    fi
}

for sig in HUP INT QUIT FPE SEGV TERM USR1 USR2
do
    trap "shutdown ${sig}" "${sig}"
done

# determine about-to-run proccess
case "${1}x" in
    /*)
	echo "Absolute command given. Replacing Entrypoint with ${*}" >&2
	exec "${@}"
	# if we reach here, something wicked happened, therefore we exit
	exit 1
	;;
    *)
	if [ -z "${1}" ]
	then
	    set -- /usr/sbin/uwsgi --ini uwsgi.ini
	else
	    set -- python3 manage.py "${@}"
	fi
	;;
esac

if [ -z "${NO_CHECK}" ]
then
    echo "Checking django database connection." >&2
    python3 manage.py check_db_connection --sleep 5 --count 5
    retval=$?

    if [ 0 -ne ${retval} ]
    then
        exit ${retval}
    fi
fi

echo "Starting main command ${*}" >&2
"${@}" &
pid=$!

echo "Waiting for children to finish." >&2
while [ 0 -eq ${_exit} ]
do
    wait
done

echo "End of entrypoint. Bye." >&2
exit 0
