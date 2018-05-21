#!/bin/sh

pid=0

shutdown() {
    echo "Got shutdown signal" >&2
    if [ 0 -ne ${pid} ]
    then
        kill -TERM ${pid}
        wait ${pid}
        exit 0
    fi
    killall -TERM
    wait
    exit 1
}

trap shutdown TERM INT QUIT

# determine about-to-run proccess
if [ -z "${1}" ]
then
    set -- /usr/sbin/uwsgi --ini uwsgi.ini --single-interpreter --need-app
elif [ "${1:0:1}" = "/" ]
then
    exec "${@}"
else
    set -- /usr/local/bin/python manage.py "${@}"
fi

if [ -z "${NO_CHECK}" ]
then
    /usr/local/bin/python manage.py check_db_connection --sleep 5 --count 5
    retval=$?

    if [ 0 -ne ${retval} ]
    then
        exit ${retval}
    fi
fi

"${@}" &
pid=$!
wait

exit 0
