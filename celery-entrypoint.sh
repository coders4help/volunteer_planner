#!/bin/sh

kill_by_pidfile() {
    pidfile="${1}"

    if [ -z "${pidfile}" ]
    then
        return
    fi

    if [ -f "${pidfile}" ]
    then
        pid="$(cat "${pidfile}")"
        kill -TERM "${pid}"
        rm "${pidfile}"
    fi
}

shutdown() {
    echo "Stopping celery beat" >&2
    kill_by_pidfile /run/vp/celery-beat.pid

    echo "Stopping celery worker" >&2
    kill_by_pidfile /run/vp/celery-worker.pid
}

for sig in HUP INT QUIT FPE SEGV TERM USR1 USR2
do
    trap "shutdown ${sig}" "${sig}"
done

# cleanup old PID files
shutdown HUP

echo "Starting celery beat" >&2
python3 -m celery \
    --app worker \
    beat \
        --loglevel INFO \
        --pidfile /run/vp/celery-beat.pid \
        &

echo "Starting celery worker" >&2
python3 -m celery \
    --app worker \
    worker \
        --loglevel INFO \
        --concurrency 2 \
        --events \
        --statedb /run/vp/celery-worker \
        --pidfile /run/vp/celery-worker.pid \
        &

wait

echo "End of celery work ... CU next time" >&2
exit 0
