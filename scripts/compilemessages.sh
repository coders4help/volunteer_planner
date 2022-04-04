#!/usr/bin/env bash

compile_cmd="./manage.py"
compile_args=(compilemessages "${@}")

echo
echo "================================================================================"
echo "Running Django management command 'compilemessages' ..."
echo "--------------------------------------------------------------------------------"
echo "${compile_cmd} ${compile_args[*]}"
${compile_cmd} "${compile_args[@]}"
compile_result=$?

if [ $compile_result -eq 0 ]; then
    echo "Compiling messages done."
fi

echo
exit $compile_result
