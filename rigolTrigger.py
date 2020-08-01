#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import time

import pyvisa

class rigolTrigger:

    def __init__(self, address):
        self.rm = pyvisa.ResourceManager()
        self.inst = self.rm.open_resource(f"TCPIP0::{address}::INSTR")
        self.inst.timeout = 2000

        self.source = None
        self.offset = None
        self.channel = 1
        self.state = None

        # Query IDN String, print it out
        self.id_str = self.inst.query("*IDN?")
        print(self.id_str)

        # Reset the device and set the time based on current workstation time.

    def reset(self):
        self.inst.write("*RST")
        time.sleep(3)
        # Set the time
        curdatetime = time.localtime()
        self.inst.write(f":SYST:DATE {curdatetime.tm_year},{curdatetime.tm_mon},{curdatetime.tm_mday}")
        self.inst.write(f":SYST:TIME {time.asctime().split(' ')[3].replace(':', ',')}")
        time.sleep(1)
