#!/usr/bin/env bash

echo
echo "================================================================================"
echo "Checking for fuzzy translations..."
echo "--------------------------------------------------------------------------------"
grep_cmd="grep"
grep_args=(-r '#, fuzzy' locale/)
echo "${grep_cmd} ${grep_args[*]}"
${grep_cmd} "${grep_args[@]}"
grep_result=$?

if [ $grep_result -ne 0 ]; then
    echo "No fuzzy translations found."
    has_fuzzy=0
else
    has_fuzzy=1
fi
echo
exit $has_fuzzy
