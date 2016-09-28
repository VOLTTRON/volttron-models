# -*- coding: utf-8 -*- {{{
# vim: set fenc=utf-8 ft=python sw=4 ts=4 sts=4 et:
#
# Copyright (c) 2016, Battelle Memorial Institute
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# The views and conclusions contained in the software and documentation are those
# of the authors and should not be interpreted as representing official policies,
# either expressed or implied, of the FreeBSD Project.
#

# This material was prepared as an account of work sponsored by an
# agency of the United States Government.  Neither the United States
# Government nor the United States Department of Energy, nor Battelle,
# nor any of their employees, nor any jurisdiction or organization
# that has cooperated in the development of these materials, makes
# any warranty, express or implied, or assumes any legal liability
# or responsibility for the accuracy, completeness, or usefulness or
# any information, apparatus, product, software, or process disclosed,
# or represents that its use would not infringe privately owned rights.
#
# Reference herein to any specific commercial product, process, or
# service by trade name, trademark, manufacturer, or otherwise does
# not necessarily constitute or imply its endorsement, recommendation,
# r favoring by the United States Government or any agency thereof,
# or Battelle Memorial Institute. The views and opinions of authors
# expressed herein do not necessarily state or reflect those of the
# United States Government or any agency thereof.
#
# PACIFIC NORTHWEST NATIONAL LABORATORY
# operated by BATTELLE for the UNITED STATES DEPARTMENT OF ENERGY
# under Contract DE-AC05-76RL01830

#}}}

class FirstOrderZone(object):
    
    
    def __init__(self):
        self.c0 = 0.3557725
        self.c1 = 0.9837171
        self.c2 = 0.002584267
        self.c3 = 0.0006142672
        self.c4 = 0.0006142672
        self.x0 = -162.6386
        self.x1 = -309.5303
        self.x2 = -4.800622
        self.x3 = 321.3943
        self.x4 = 0.9944429
        self.tOut = 20.
        self.tIn = 24.
        self.tSet = 21.11
        self.tDel = 0.25
        self.qHvacSens = 0.
        self.tMin = 22.
        self.tMax = 24.
        self.qMin = -1.
        self.qMax = -1000000.
        self.name = "FirstOrderZone"


    def getQ(self, T_new):
        qHvacNew = self.x0 + self.x1*self.tIn + self.x2*self.tOut + self.x3*T_new + self.x4*self.qHvacSens
        return qHvacNew
    
    
    def calcMinCoolPower(self):
        # q values are negative, so this is confusing
        t = max(min((self.tSet+self.tDel), self.tMax), self.tMin)
        q = max(min(self.getQ(t), self.qMin), self.qMax)
        return q


    def calcMaxCoolPower(self):
        # q values are negative, so this is confusing
        t = min(max((self.tSet-self.tDel), self.tMin), self.tMax)
        q = max(min(self.getQ(t), self.qMin), self.qMax)
        return q


    def getT(self, qHvac):
        return self.c0 + self.c1*self.tIn + self.c2*self.tOut + self.c3*qHvac + self.c4*self.qHvacSens

