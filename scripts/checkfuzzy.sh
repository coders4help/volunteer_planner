#!/usr/bin/env bash

echo
echo "================================================================================"
echo "Checking for fuzzy translations..."
echo "--------------------------------------------------------------------------------"
grep_cmd="grep"
grep_args=(-rE '^#[,[:space:]]+fuzzy' locale/)
echo "${grep_cmd} ${grep_args[*]}"
${grep_cmd} "${grep_args[@]}"
grep_result=$?

[ $grep_result -ne 0 ]
has_fuzzy=$?

if [ $has_fuzzy -eq 0 ]; then
    echo "No fuzzy translations found."
fi
echo
exit $has_fuzzy
