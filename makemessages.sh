#!/usr/bin/env bash
cmd="python3 manage.py makemessages --all --no-wrap --no-location --no-obsolete"
echo $cmd
${cmd}
