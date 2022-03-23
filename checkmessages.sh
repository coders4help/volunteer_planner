#!/usr/bin/env bash
#set -e

./scripts/makemessages.sh "${@}"
./scripts/checkdiffs.sh
./scripts/checkfuzzy.sh
./scripts/compilemessages.sh "${@}"
