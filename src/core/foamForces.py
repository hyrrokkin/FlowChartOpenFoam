#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 09:22:09 2013

@author: pete
"""

import matplotlib.pyplot as plt
import re
import numpy as np

forceRegex = r"([0-9.eE\-+]+)\s+\(+([0-9.eE\-+]+)\s([0-9.eE\-+]+)\s([0-9.eE\-+]+)\)"
forceRegex += r"\s\(([0-9.eE\-+]+)\s([0-9.eE\-+]+)\s([0-9.eE\-+]+)\)"
forceRegex += r"\s\(([0-9.eE\-+]+)\s([0-9.eE\-+]+)\s([0-9.eE\-+]+)\)+"
forceRegex += r"\s+\(+([0-9.eE\-+]+)\s([0-9.eE\-+]+)\s([0-9.eE\-+]+)\)"
forceRegex += r"\s\(([0-9.eE\-+]+)\s([0-9.eE\-+]+)\s([0-9.eE\-+]+)\)"
forceRegex += r"\s\(([0-9.eE\-+]+)\s([0-9.eE\-+]+)\s([0-9.eE\-+]+)\)+"

pattern = re.compile(forceRegex)

t = []
fpx = []; fpy = []; fpz = []
fpox = []; fpoy = []; fpoz = []
fvx = []; fvy = []; fvz = []
mpx = []; mpy = []; mpz = []
mpox = []; mpoy = []; mpoz = []
mvx = []; mvy = []; mvz = []


def GetAveragedForces(fName):
    pipefile = open(fName,'r')
    lines = pipefile.readlines()
    for line in lines:
            match = re.search(forceRegex,line)
            if match:
                    t.append(float(match.group(1)))
                    fpx.append(float(match.group(2)))
                    fpy.append(float(match.group(3)))
                    fpz.append(float(match.group(4)))
                    fvx.append(float(match.group(5)))
                    fvy.append(float(match.group(6)))
                    fvz.append(float(match.group(7)))
                    fpox.append(float(match.group(8)))
                    fpoy.append(float(match.group(9)))
                    fpoz.append(float(match.group(10)))
                    mpx.append(float(match.group(11)))
                    mpy.append(float(match.group(12)))
                    mpz.append(float(match.group(13)))
                    mvx.append(float(match.group(14)))
                    mvy.append(float(match.group(15)))
                    mvz.append(float(match.group(16)))
                    mpox.append(float(match.group(17)))
                    mpoy.append(float(match.group(18)))
                    mpoz.append(float(match.group(19)))
    avPx = np.sum(fpx[-10:])/10
    avPy = np.sum(fpy[-10:])/10
    avPz = np.sum(fpz[-10:])/10
    avMpx = np.sum(mpx[-10:])/10
    avMpy = np.sum(mpy[-10:])/10
    avMpz = np.sum(mpz[-10:])/10        
    return [avPx,avPy,avPz, avMpx, avMpy,avMpz]

