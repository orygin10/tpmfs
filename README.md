You didn't misread. It's not tmpfs. It's tpmfs !

# TPM File System

Use your TPM chip at its fullest extent ! Store up to 32 MiB of raw data.

## My specs
- Laptop : `UX510UW`
- TPM Version : `2.0`
- TPM Manufacturer : `Infineon`
- Operating system : `Fedora rawhide`

## Misc

- `TPM Version 2.0` is a different implementation from `TPM Version 1.2`. This set of tools only works on `2.0`.
- Indexes from `0x1000000` to `Ox1ffffff` can be set (`2^24`)
- Up to 2048 bytes of data can be written to an index (`2^11`). Total = `2^35` bytes (32 MiB)

## Features

- Store a n-bytes block to a chosen index (`1<=n<=2048`)
- Load a n-bytes block from a chosen index

## Todo

- Store a chunk (>2048-bytes) on multiple index by dividing it into blocks
