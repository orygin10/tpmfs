#!/usr/bin/env bash

readonly NV_WORD="0x2000A"
readonly AUTH_OWNER="0x40000001"
LANG=C LC_ALL=C
CUR_DIR="$(dirname "$(readlink -f "$0")")"

OWNERPASS=""
INDEX="0x1400001"
AUTHORIZATION="${AUTH_OWNER}"
ATTRIBUTE="${NV_WORD}"
INPUT_FILE="${CUR_DIR}/nv.data"
OUTPUT_FILE="${CUR_DIR}/nv.read.data"
INPUT_DATA="Hi !"
SIZE="2048"

function print_success {
  printf "\033[32m[ OK ]\033[39m %s\n" "${1}" >&2
}

function print_failure {
  printf "\033[31m[ NOK ]\033[39m %s\n" "${1}" >&2
}

function print_info {
  printf "\033[33m[ INFO ]\033[39m %s\n" "${1}" >&2
}

function _askpass {
  read -s -p "Enter Password: " OWNERPASS
  printf "\n"
  [[ "${#OWNERPASS}" -gt 0 ]] && return 0 ||
    print_failure "Failed to set password" && return 1
}

function _define {
  tpm2_nvlist | grep "${INDEX}" -A 7 >/dev/null &&
    print_failure "Index ${INDEX} already exists. Cannot create\n" && return 1

  tpm2_nvdefine -x "${INDEX}" -a "${AUTHORIZATION}" -s "${SIZE}" -t "${ATTRIBUTE}" -P "${OWNERPASS}" &&
    print_success "Defined index ${INDEX} of size ${SIZE}" && return 0 ||
    print_failure "Failed to define index ${INDEX}" && return 1
}

function _write {
  print_info "Input data is ${#INPUT_DATA} bytes len"

  [[ "${#INPUT_DATA}" -gt "${SIZE}" ]] &&
    print_failure "Data larger than index size (${SIZE})" \
    && return 1


  PADDING="$(( ${SIZE} - ${#INPUT_DATA} ))"
  [[ "${#INPUT_DATA}" -lt "${SIZE}" ]] &&
    print_info "Padding with ${PADDING} null bytes to fit ${SIZE} bytes"

  printf "${INPUT_DATA}" > "${INPUT_FILE}"
  head -c ${PADDING} < /dev/zero >> "${INPUT_FILE}"
  print_info "${SIZE} bytes of data written to buffer ${INPUT_FILE}"

  tpm2_nvwrite -x "${INDEX}" -a "${AUTHORIZATION}" "${INPUT_FILE}" -P "${OWNERPASS}" &&
    print_success "Buffer written to index ${INDEX}" && return 0 ||
    print_failure "Failed writing buffer to index ${INDEX}" && return 1
}

function _read {
  tpm2_nvread -x "${INDEX}" -a "${AUTHORIZATION}" -s "${SIZE}" -P "${OWNERPASS}" -f "${OUTPUT_FILE}" &&
    print_success "Read ${SIZE} bytes from index ${INDEX} to ${OUTPUT_FILE}" && return 0 ||
    print_failure "Failed to read ${SIZE} bytes from index ${INDEX} to ${OUTPUT_FILE}" && return 1
}

function _check {
  [[ "$(tpm2_hash -H e -g sha256 "${INPUT_FILE}")" = "$(tpm2_hash -H e -g sha256 "${OUTPUT_FILE}")" ]]&& 
    print_success "Input and output file are the same" && return 0 || 
    print_failure "Failed, input file is different from output file" && return 1
}

function _release {
  tpm2_nvrelease -x "${INDEX}" -a "${AUTHORIZATION}" -P "${OWNERPASS}" &&
    print_success "Index ${INDEX} released" && return 0 ||
    print_failure "Failed to release index ${INDEX}" && return 1
}

_askpass &&
_define &&
_write &&
_read &&
_release &&
_check

exit 0
