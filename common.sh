#!/usr/bin/env bash

# TPM CONSTANTS
readonly TPM_RH_OWNER="0x40000001"

# TPM VARIABLES
AUTHORIZATION="${TPM_RH_OWNER}"
ATTRIBUTE="0x2000A" # ownerwrite|policywrite|ownerread (0xA0002)

LANG=C LC_ALL=C # Needed to measure size of str in bytes 

function print_success {
  printf "\033[32m[ OK ]\033[39m %s\n" "${1}" >&2
  return 0
}

function print_failure {
  printf "\033[31m[ NOK ]\033[39m %s\n" "${1}" >&2
  exit 1
}

function print_info {
  printf "\033[33m[ INFO ]\033[39m %s\n" "${1}" >&2
}

function _askpass {
  local ownerpass=""
  read -s -p "Enter Password: " ownerpass
  printf "\n" >&2
  [[ "${#ownerpass}" -gt 0 ]] && printf "${ownerpass}" && return 0 ||
    print_failure "Failed to set password"
}
