#!/usr/bin/env python2
from sys import argv

# -1 for big endian, 1 for little endian
END=-1

# Poor man's getopt
if not 2<= len(argv) <=3:
    print "%s %s" % (argv[0], "0x2000A")
    print "%s -v %s" % (argv[0], "2,14,28")
    raise SystemExit
elif argv[1] == "-v":
    bit_array = argv[2].split(',')
    hex_array = 0x0
    for bit_pos in bit_array:
        hex_array = hex_array | int('1'.ljust(32-int(bit_pos), '0'),2)
    print '0x%s' % hex(hex_array)[2:][::END].upper()
else:
    hex_array = int('0x%s' % argv[1][2:][::END], 16)
    print [n for n,i in enumerate(bin(hex_array)[2:].zfill(32)) if i=='1']
