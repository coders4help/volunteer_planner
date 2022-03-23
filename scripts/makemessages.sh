#!/usr/bin/env bash

default_locale_args() {
    locale_arg=0
    while [ $# -gt 0 ]; do
        arg="${1}"
        shift
        if [[ "${arg}" =~ ^-(a|l|-all|-locale)(=|$) ]]; then
            locale_arg=1
            break
        fi
    done

    if [ $locale_arg -eq 0 ]; then
        echo "--all"
    else
        echo ""
    fi
}

mkmsg_cmd="./manage.py"
mkmsg_args=(makemessages --no-wrap --no-location --no-obsolete "${@}")

default_locale="$(default_locale_args "${@}")"
if [ -n "${default_locale}" ]; then
    mkmsg_args+=("${default_locale}")
fi

echo
echo "================================================================================"
echo "Running Django management command 'makemessages' ..."
echo "--------------------------------------------------------------------------------"
echo "${mkmsg_cmd} ${mkmsg_args[*]}"
${mkmsg_cmd} "${mkmsg_args[@]}"
mkmsg_result=$?
echo "Done."
echo

exit $mkmsg_result
