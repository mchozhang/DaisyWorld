#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
run the program for multiple times to obtain numerous output results
"""

from subprocess import call

for i in range(20):
    output_name = 'result{}.csv'.format(i)
    call(['python', 'main.py', 'standard.json', output_name], shell=False)
