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

if [ -z ${NO_CHECK} ]
then
    /usr/local/bin/python manage.py check_db_connection
    retval=$?

    if [ 0 -ne ${retval} ]
    then
        exit ${retval}
    fi
fi

/usr/local/bin/python manage.py $@ &
pid=$!
wait

exit 0
