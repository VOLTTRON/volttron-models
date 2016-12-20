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

from rtusimple import RtuSimple


class RtuRegression(RtuSimple):
    
    
    def __init__(self):
        RtuSimple.__init__(self)
        self.coolingCapacityCoeff = None
        self.coolingPowerCoeff = None
        self.heatingCapacityCoeff = None
        self.heatingPowerCoeff = None
        
        
    def calcCoolPower(self):
        power = self.nominalCoolingPower
        if self.coolingPowerCoeff is not None:
            c = self.coolingPowerCoeff
            power =  c[0] + c[1]*self.tOut + c[2]*self.tIn + c[3]*pow(self.tOut,2) + c[4]*pow(self.tIn,2) + c[5]*self.tOut*self.tIn
        return power
    
    
    def calcCoolCapacity(self):
        capacity = -self.nominalCoolingCapacity
        if self.coolingCapacityCoeff is not None:
            c = self.coolingCapacityCoeff
            capacity = -(c[0] + c[1]*self.tOut + c[2]*self.tIn + c[3]*pow(self.tOut,2) + c[4]*pow(self.tIn,2) + c[5]*self.tOut*self.tIn)
        return capacity
        
        
    def calcHeatPower(self):
        power = self.nominalHeatingPower
        if self.heatingPowerCoeff is not None:
            c = self.heatingPowerCoeff
            power = c[0] + c[1]*self.tOut + c[2]*self.tIn + c[3]*pow(self.tOut,2) + c[4]*pow(self.tIn,2) + c[5]*self.tOut*self.tIn
        if self.isAuxOn:
            power += self.nominalAuxPower
        return power
    
    
    def calcHeatCapacity(self):
        capacity = self.nominalHeatingCapacity
        if self.heatingCapacityCoeff is not None:
            c = self.heatingCapacityCoeff
            capacity = (c[0] + c[1]*self.tOut + c[2]*self.tIn + c[3]*pow(self.tOut,2) + c[4]*pow(self.tIn,2) + c[5]*self.tOut*self.tIn)
        if self.isAuxOn:
            capacity += self.nominalAuxCapacity
        return capacity
        
        