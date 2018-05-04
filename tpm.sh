#!/usr/bin/env bash

CUR_DIR="$(dirname "$(readlink -f "$0")")"

# <common.sh>
# Imported functions : 
# - print_success
# - print_failure
# - _askpass
source "${CUR_DIR}/common.sh"

# <api.sh>
# Imported functions :
# - _define
# - _write
# - _read
# - _release
# - _check
source "${CUR_DIR}/api.sh"

function send_data {
  #INDEX="0x1400001"
  #INPUT_DATA="Hi !"
  #SIZE="2048"
  INDEX="${1}"
  SIZE="${2}"
  INPUT_DATA="${3}"

  OWNERPASS="$(_askpass)" &&
  _define &&
  _write || _release &&
  _read &&
  _release &&
  _check &&
  return 0 || return 1
}

# 0x1000000 à 0x1ffffff
# 16777215 (2^24) bytes
# 2^24 * 2048 (2^35) bytes
# = 32MiB

printf "remiliascarlet" | send_data "0x1ffffff" 2048 "Hello !"

exit 0
