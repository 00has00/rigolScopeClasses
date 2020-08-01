#!/usr/bin/env bash

PATH=$PATH:.

rigolChannel.py -r -c a -s 5 on
rigolChannel.py -c 1 -o 15
rigolChannel.py -c 2 -o 5
rigolChannel.py -c 3 -o -5
rigolChannel.py -c 4 -o -15