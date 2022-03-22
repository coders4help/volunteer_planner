#!/usr/bin/env bash
set -e

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

cmd="./manage.py"
args=(makemessages --no-wrap --no-location --no-obsolete "${@}")

default_locale="$(default_locale_args "${@}")" 
if [ -n "${default_locale}" ]; then
    args+=("${default_locale}")
fi

echo "${cmd} ${args[*]}"
${cmd} "${args[@]}"
echo "Done."

echo
echo "Checking for changes in .po files..."
git diff --ignore-matching-lines=POT-Creation-Date --exit-code -- '***.po'
diff_result=$?

if [ $diff_result -eq 0 ]; then
    echo "No changed messages found."
fi

echo
exit $diff_result
