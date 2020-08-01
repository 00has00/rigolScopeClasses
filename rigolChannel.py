#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import time

import pyvisa


class RigolChannel:

    def __init__(self, address):
        self.rm = pyvisa.ResourceManager()
        self.inst = self.rm.open_resource(f"TCPIP0::{address}::INSTR")
        self.inst.timeout = 2000

        self.scale = None
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

    def set_offset(self, offset):
        self.offset = offset

    def set_scale(self, scale):
        self.scale = scale

    def set_channel(self, channel):
        self.channel = channel

    def set_state(self, state):
        self.state = state

    def get_scale(self):
        print(f"Scale: {self.scale}")

    def configure(self):
        if self.state is not None:
            self.inst.write(f":CHAN{self.channel}:DISP {self.state}")
            self.inst.write(f":CHAN{self.channel}:COUP DC")
            self.inst.write(f":CHAN{self.channel}:PROB 1")
        if self.scale is not None:
            self.inst.write(f":CHAN{self.channel}:SCAL {self.scale}")
        if self.offset is not None:
            self.inst.write(f":CHAN{self.channel}:OFFS {self.offset}")
        time.sleep(1)

    def status(self):
        state = self.inst.query(f":CHAN{self.channel}:DISP?")
        coup = self.inst.query(f":CHAN{self.channel}:COUP?")
        prob = self.inst.query(f":CHAN{self.channel}:PROB?")
        scale = self.inst.query(f":CHAN{self.channel}:SCAL?")
        offset = self.inst.query(f":CHAN{self.channel}:OFFS?")
        if state.strip() == '1':
            state = 'on'
        else:
            state = 'off'

        print(
            f"Channel: {self.channel} - {state} - Scale: {scale.strip()} - Offset: {offset.strip()} - Attenuation: {prob.strip()} - Coupling: {coup.strip()}")

    def finish(self):
        self.inst.close()

def main():
    # Commands line arguments
    argpar = argparse.ArgumentParser()
    argpar.add_argument('-v', action='store_true', help='Display channel status.')
    argpar.add_argument('-r', action='store_true', help='Reset the device.')
    argpar.add_argument('-o', type=float, help='Set vertical offset.')
    argpar.add_argument('-s', type=float, help='Scale - per division (in volts).')
    argpar.add_argument('-c', choices=['1', '2', '3', '4', 'a'], help='Select channel to affect')
    argpar.add_argument('-a', dest='hostname', default='10.1.1.146', help='Hostname or IP address of printer.')
    argpar.add_argument('state', nargs='?', action='store', choices=['on', 'off'], help='channel state - on|off')

    args = argpar.parse_args()

    myscope = RigolChannel(args.hostname)

    if args.r:
        myscope.reset()

    if args.o:
        if (args.o > 0) | (args.o <= 50):
            myscope.set_offset(args.o)

    if args.s:
        if (args.s > 0) | (args.s <= 50):
            myscope.set_scale(args.s)

    myscope.set_state(args.state)

    if args.c == 'a':
        for i in range(1, 5):
            myscope.set_channel(i)
            myscope.configure()
    elif int(args.c) in range(1, 5):
        myscope.set_channel(args.c)
        myscope.configure()
    else:
        myscope.configure()

    # print(f"Scale: {args.s}")
    # print(f"Offset: {args.o}")
    # print(f"channel: {args.c}")
    # print(f"state: {args.state}")
    if args.v:
        if args.c == 'a':
            for i in range(1, 5):
                myscope.set_channel(i)
                myscope.status()
        elif int(args.c) in range(1, 5):
            myscope.set_channel(args.c)
            myscope.status()
        else:
            myscope.status()

    myscope.finish()


if __name__ == "__main__":
    main()
