#!/usr/bin/python

# Copyright (C) International Business Machines Corp., 2005
# Author: Dan Smith <danms@us.ibm.com>

from XmTestLib import *

# The current device model, qemu-dm, only supports 8 MAX_NICS currently.
if ENABLE_HVM_SUPPORT:
    MAX_NICS = 8
    nic = "type=ioemu, bridge=xenbr0"
else:
    MAX_NICS = 10
    nic = ''

for i in range(0,MAX_NICS):
    config = {"vif": [ nic ] * i}
    domain = XmTestDomain(extraConfig=config)

    try:
        domain.start()
    except DomainError, e:
        FAIL("(%i nics) " % i + str(e))

    try:
        console = XmConsole(domain.getName())
        console.sendInput("input")
        console.runCmd("ls")
    except ConsoleError, e:
        FAIL("(%i nics) Console didn't respond: probably crashed!" % i)

    domain.destroy()
