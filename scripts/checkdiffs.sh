#!/usr/bin/env bash

echo
echo "================================================================================"
echo "Checking for changes in .po files..."
echo "--------------------------------------------------------------------------------"
diff_cmd="git"
diff_args=(diff --ignore-matching-lines=POT-Creation-Date --exit-code -- ':/:locale/**/*.po')
echo "${diff_cmd} ${diff_args[*]}"
${diff_cmd} "${diff_args[@]}"
diff_result=$?

if [ $diff_result -eq 0 ]; then
    echo "No changed messages found."
fi
echo
exit $diff_result

