#!/usr/bin/env bash

cmd="./manage.py makemessages --no-wrap --no-location --no-obsolete $@"
echo "${cmd}"
${cmd}
echo "Done."
echo
echo "Checking for changes in .po files..."
git diff --ignore-matching-lines=POT-Creation-Date --exit-code -- '***.po'

diff_result=$?
test $diff_result -eq 0 && echo "No changed messages found."
echo
exit $diff_result
