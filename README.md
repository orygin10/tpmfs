You didn't misread. It's not tmpfs. It's tpmfs !

# TPM File System

Use your TPM chip at its fullest extent ! Store up to 5.832 KiB of raw data.

**Features**

- Tons of space
- High throughput (up to 48 Kbit/s)

## My specs
- Laptop : `UX510UW`
- TPM Version : `2.0`
- TPM Manufacturer : `Infineon`
- Operating system : `Fedora rawhide`

## Misc

- `TPM Version 2.0` is a different implementation from `TPM Version 1.2`. This set of tools only works on `2.0`.

## Features

- Store a n-bytes block to a chosen index (`1<=n<=2048`)
- Load a n-bytes block from a chosen index
- Push a file

## Todo

- Pull a file
- Optimise space (avoid filling block with empty space)

## Please tell me more
```
                                    +-------------+
                                    |             |
             +---------------------->  TPM Chip   <----------------------+
             |                      |             |                      |
             |                      +---^-----^---+                      |
             |                          |     |                          |
             |                          |     |                          |
             |                          |     |                          |
    +--------+--------+ +---------------+-+ +-+---------------+ +--------+--------+
    |                 | |                 | |                 | |                 |
    |  tpm2-nvdefine  | |  tpm2-nvwrite   | |   tpm2-nvread   | |  tpm2-nvrelease |
    |                 | |                 | |                 | |                 |
    +--------+--------+ +--------+--------+ +--------+--------+ +--------+--------+
             |                   |                   |                   |
             |                   |                   |                   |
+------------+-------------------+-------------------+-------------------+------------+
|                                                                                     |
|                                                                                     |
|         _define             _write             _read               _release         |
|                                                                                     |
|                                    +---------+                                      |
|                                    |   API   |                                      |
+------------------------------------+----+----+--------------------------------------+
                                          |
                                          |
                    +----------------+----+----+-------------------+
                    |                | TPM FS  |                   |
                    |                +---------+                   |
                    |                                              |
                    |          push     pull     delete            |
                    |                                              |
                    +----------------------------------------------+

```

## Again

```
                      _define        tpm2_nvdefine
     push             _write         tpm2_nvwrite        /dev/tpm0

+-------------+   +-------------+   +-------------+   +-------------+
|             |   |             |   |             |   |             |
|    fs.py    +--->   tpm.sh    +--->  tpm2-tools +--->  TPM Chip   |
|             |   |             |   |             |   |             |
+-------------+   +-------------+   +-------------+   +-------------+
```

## Once more

```
                        +-------------+   +-------------+   +-------------+   +-------------+
                        |             |   |             |   |             |   |             |
                   +----> Interface() +--->   tpm.sh    +--->   api.sh    +--->TPM 2.0 Chip |
                   |    |             |   |             |   |             |   |             |
+-------------+    |    +-------------+   +-------------+   +-------------+   +-------------+
|             |    |
|    FS()     +----+
|             |    |
+-------------+    |    +-------------+   +-------------+
                   |    |             |   |             |
                   +----> Filetable() +--->filetable.yml|
                        |             |   |             |
                        +-------------+   +-------------+
```
