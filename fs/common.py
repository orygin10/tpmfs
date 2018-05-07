#!/usr/bin/env python2
VERBOSE=True
VERBOSE=False

def print_success(msg):
    if VERBOSE:
        print "\033[32m[ OK ]\033[39m %s" % msg

def print_failure(msg):
    if VERBOSE:
        print "\033[31m[ NOK ]\033[39m %s" % msg

def print_info(msg):
    if VERBOSE:
        print "\033[33m[ INFO ]\033[39m %s" % msg
