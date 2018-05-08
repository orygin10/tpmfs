#!/usr/bin/env python2
import sys

def print_stderr(msg):
    sys.stderr.write(str(msg))
    sys.stderr.flush()
    return True
