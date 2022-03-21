#!/usr/bin/env bash
cmd="./manage.py makemessages --all --no-wrap --no-location --no-obsolete"
echo "${cmd}"
${cmd}
