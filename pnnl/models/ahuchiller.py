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

class AhuChiller(object):
    
    
    def __init__(self):
        self.tAirReturn = 20.
        self.tAirSupply = 10.
        self.tAirMixed = 20.
        self.cpAir = 1006. # J/kg
        self.c0 = 0 # coefficients are for SEB fan
        self.c1 = 2.652E-01
        self.c2 = -1.874E-02
        self.c3 = 1.448E-02
        self.c4 = 0.
        self.c5 = 0.
        self.pFan = 0.
        self.mDotAir = 0.
        self.staticPressure = 0.
        self.coilLoad = 0.
        self.COP = 6.16
        self.name = 'AhuChiller'
        
        
    def calcAirFlowRate(self, qLoad):
        if self.tAirSupply == self.tAirReturn:
            self.mDotAir = 0.0
        else:
            self.mDotAir = abs(qLoad/self.cpAir/(self.tAirSupply-self.tAirReturn)) # kg/s


    def calcFanPower(self):
        self.pFan = (self.c0 + self.c1*self.mDotAir + self.c2*pow(self.mDotAir,2) + self.c3*pow(self.mDotAir,3) + self.c4*self.staticPressure + self.c5*pow(self.staticPressure,2))*1000. # watts


    def calcCoilLoad(self):
        coilLoad = self.mDotAir*self.cpAir*(self.tAirSupply-self.tAirMixed) # watts
        if coilLoad > 0: #heating mode is not yet supported!
            self.coilLoad = 0.0
        else:
            self.coilLoad = coilLoad
        
        
    def calcTotalLoad(self, qLoad):
        self.calcAirFlowRate(qLoad)
        return self.calcTotalPower()
    
    
    def calcTotalPower(self):
        self.calcFanPower()
        self.calcCoilLoad()
        return abs(self.coilLoad)/self.COP + self.pFan

