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

# Getopt
while getopts ":drw:ui:hp:s:" opt; do
  case $opt in
    d)
      # Define
      BOOL_DEFINE=1
      ;;
    r)
      # Read 2048 Bytes # Need file
      BOOL_READ=1
      ;;
    w)
      # Write 2048 bytes # Need data
      INPUT_DATA="${OPTARG}"
      ;;
    u)
      # Release
      BOOL_RELEASE=1
      ;;
    p)
      OWNERPASS="${OPTARG}"
      ;;
    s)
      SIZE="${OPTARG}"
      ;;
    i)
      INDEX="${OPTARG}"
      ;;
    h)
      BOOL_HELP=1
      ;;
    \?)
      printf "Invalid option: -%s\n" "$OPTARG" >&2
      exit 1
      ;;
    :)
      printf "Option -%s requires an argument.\n" "$OPTARG" >&2
      exit 1
      ;;
  esac
done

function print_usage {
  printf "Usage: %s [ -d|r|u -i INDEX ] [ -w DATA -i INDEX ] [ -p ] [ -s ]\n" "$0" >&2
  printf "   -d    Define INDEX on TPM Chip (Attribute and Authorization in common.sh)\n" >&2
  printf "   -r    Read SIZE bytes from INDEX\n" >&2
  printf "   -w    Write DATA  (SIZE bytes block) to INDEX\n" >&2
  printf "   -u    Release INDEX\n" >&2
  printf "   -i    Index; 0x1240000 for exemple\n" >&2
  printf "   -s    Index size in bytes (default 2048)\n" >&2
  printf "   -p    Owner password. Omit to ask\n" >&2
  printf "   -h    Print this help\n" >&2
  exit 1
}

[ "$#" -eq 0 ] || [ ! -z ${BOOL_HELP+x} ] \
  && print_usage && exit 1

[ -z ${OWNERPASS+x} ] && OWNERPASS="$(_askpass)"
[ -z ${SIZE+x} ] && SIZE=2048

[ ! -z ${BOOL_DEFINE+x} ] && [ ! -z ${INDEX+x} ] \
  && _define \
  && exit 0

[ ! -z ${INPUT_DATA+x} ] && [ ! -z ${INDEX+x} ] \
  && _write \
  && exit 0

[ ! -z ${BOOL_READ+x} ] && [ ! -z ${INDEX+x} ] \
  && _read \
  && exit 0

[ ! -z ${BOOL_RELEASE+x} ] && [ ! -z ${INDEX+x} ] \
  && _release \
  && exit 0

print_usage && exit 1

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

exit 0
