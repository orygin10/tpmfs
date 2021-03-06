#!/usr/bin/env bash

function _define {
  tpm2_nvlist | grep "${INDEX}" -A 7 >/dev/null &&
    print_failure "Index ${INDEX} already exists. Cannot create"

  tpm2_nvdefine -x "${INDEX}" -a "${AUTHORIZATION}" -s "${SIZE}" -t "${ATTRIBUTE}" -P "${OWNERPASS}" \
    && print_success "Defined index ${INDEX} of size ${SIZE}" \
    || print_failure "Failed to define index ${INDEX}"
}

function _write {
  print_info "Input data is ${#INPUT_DATA} bytes len"

  [[ "${#INPUT_DATA}" -gt "${SIZE}" ]] \
    && print_failure "Data larger than index size (${SIZE})"

  printf "${INPUT_DATA}" > "${INPUT_FILE}"

  [[ "${#INPUT_DATA}" -lt "${SIZE}" ]] \
    && PADDING="$(( ${SIZE} - ${#INPUT_DATA} ))" \
    && print_info "Padding with ${PADDING} null bytes to fit ${SIZE} bytes" \
    && head -c ${PADDING} < /dev/zero >> "${INPUT_FILE}"

  print_info "${SIZE} bytes of data written to buffer ${INPUT_FILE}"

  tpm2_nvwrite -x "${INDEX}" -a "${AUTHORIZATION}" "${INPUT_FILE}" -P "${OWNERPASS}" \
    && print_success "Buffer written to index ${INDEX}" \
    || print_failure "Failed writing buffer to index ${INDEX}"
}

function _write_file {
  local filesize="$(wc -c ${INPUT_FILE} | cut -f1 -d' ')"
  print_info "Input file is ${filesize} len"

  [[ "${filesize}" -gt "${SIZE}" ]] \
    && print_failure "Data larger than index size (${SIZE})"

  [[ "${filesize}" -lt "${SIZE}" ]] \
    && PADDING="$(( ${SIZE} - ${filesize} ))" \
    && print_info "Padding with ${PADDING} null bytes to fit ${SIZE} bytes" \
    && head -c ${PADDING} < /dev/zero >> "${INPUT_FILE}"

  tpm2_nvwrite -x "${INDEX}" -a "${AUTHORIZATION}" "${INPUT_FILE}" -P "${OWNERPASS}" \
    && print_success "${INPUT_FILE} written to index ${INDEX}" \
    || print_failure "Failed writing ${INPUT_FILE} to index ${INDEX}"
}

function _read {
  tpm2_nvread -x "${INDEX}" -a "${AUTHORIZATION}" -s "${SIZE}" -P "${OWNERPASS}" \
    && print_success "Read ${SIZE} bytes from index ${INDEX}" \
    || print_failure "Failed to read ${SIZE} bytes from index ${INDEX}"
}

function _check {
  function _hash {
    tpm2_hash -H e -g sha256 "${1}"
  }
  [[ $(_hash "${INPUT_FILE}") = $(_hash "${OUTPUT_FILE}") ]] \
    && print_success "Input and output file are the same" \
    || print_failure "Failed, input file is different from output file"
}

function _release {
  tpm2_nvrelease -x "${INDEX}" -a "${AUTHORIZATION}" -P "${OWNERPASS}" \
    && print_success "Index ${INDEX} released" \
    || print_failure "Failed to release index ${INDEX}"
}
