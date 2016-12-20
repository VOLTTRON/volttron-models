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

class RtuSimple(object):
    
    
    HEATING = 'heating'
    COOLING = 'cooling'
    CPAIR = 1006.0 #J/kg-K
    
    
    def __init__(self):
        self.nominalCoolingCapacity = 10.0 #W
        self.nominalCoolingPower = 2.0 #W
        self.nominalHeatingCapacity = 10.0 #W
        self.nominalHeatingPower = 2.5 #W
        self.nominalFanPower = 0.5 #W
        self.nominalFlowRate = 1.0 #kg/s
        self.nominalAuxCapacity = 10.0 #W
        self.nominalAuxPower = 10.0 #W
        self.oaFraction = 0.4
        self.isCompressorRunning = True
        self.isFanRunning = True
        self.mode = RtuSimple.COOLING
        self.isAuxOn = False
        self.runTime = 0.0
        self.minRunTime = 0.0
        self.offTime = 0.0
        self.minOffTime = 0.0
        self.tIn = 22.0
        self.tOut = 24.0
        
    
    def calcCoolPower(self):
        return self.nominalCoolingPower
    
    
    def calcCoolCapacity(self):
        return -self.nominalCoolingCapacity
    
    
    def calcMinCoolCapacity(self, timeStep):
        onFraction = self.calcMinCoolRunFraction(timeStep)
        offFraction = 1-onFraction
        return self.calcCoolCapacity()*onFraction + self.calcVentilationCapacity()*offFraction
    
    
    def calcMaxCoolCapacity(self, timeStep):
        onFraction = self.calcMaxCoolRunFraction(timeStep)
        offFraction = 1-onFraction
        return self.calcCoolCapacity()*onFraction + self.calcVentilationCapacity()*offFraction
    
    
    # calculate the minimum power based on power * min run time
    def calcMinCoolPower(self, timeStep):
        onFraction = self.calcMinCoolRunFraction(timeStep)
        offFraction = 1-onFraction
        return self.calcCoolPower()*onFraction + self.nominalFanPower*offFraction
    
    
    # calculate the maximum power based on power * max run time
    def calcMaxCoolPower(self, timeStep):
        onFraction = self.calcMaxCoolRunFraction(timeStep)
        offFraction = 1-onFraction
        return self.calcCoolPower()*onFraction + self.nominalFanPower*offFraction
    
    
    def calcMinCoolRunFraction(self, timeStep):
        t = 0.0
        if self.isCompressorRunning and self.runTime < self.minRunTime:
            t = min(timeStep, self.minRunTime-self.runTime)
        return t/timeStep
        
        
    def calcMaxCoolRunFraction(self, timeStep):
        t = timeStep
        if not self.isCompressorRunning and self.offTime < self.minOffTime:
            t = min(timeStep, self.minOffTime-self.offTime)
        return t/timeStep
        
        
    def calcHeatPower(self):
        power = self.nominalHeatingPower
        if self.isAuxOn:
            power += self.nominalAuxPower
        return power
    
    
    def calcHeatCapacity(self):
        capacity = self.nominalHeatingCapacity
        if self.isAuxOn:
            capacity += self.nominalAuxCapacity
        return capacity
    
    
    def calcMinHeatCapacity(self, timeStep):
        onFraction = self.calcMinHeatRunFraction(timeStep)
        offFraction = 1-onFraction
        return self.calcHeatPower()*onFraction + self.calcVentilationCapacity()*offFraction
    
    
    def calcMaxHeatCapacity(self, timeStep):
        onFraction = self.calcMaxHeatRunFraction(timeStep)
        offFraction = 1-onFraction
        return self.calcHeatPower()*onFraction + self.calcVentilationCapacity()*offFraction
    
    
    # calculate the minimum power based on power * min run time
    def calcMinHeatPower(self, timeStep):
        onFraction = self.calcMinHeatRunFraction(timeStep)
        offFraction = 1-onFraction
        return self.calcHeatPower()*onFraction + self.nominalFanPower*offFraction
    
    
    # calculate the maximum power based on power * max run time
    def calcMaxHeatPower(self, timeStep):
        onFraction = self.calcMaxHeatRunFraction(timeStep)
        offFraction = 1-onFraction
        return self.calcHeatPower()*onFraction + self.nominalFanPower*offFraction
    
    
    # this may use a different flag at some point
    def calcMinHeatRunFraction(self, timeStep):
        return self.calcMinCoolRunFraction(timeStep)
        
        
    # this may use a different flag at some point
    def calcMaxHeatRunFraction(self, timeStep):
        return self.calcMaxCoolRunFraction(timeStep)
    
    
    def calcVentilationCapacity(self):
        return self.nominalFlowRate*RtuSimple.CPAIR*(self.tIn-self.tOut)*self.oaFraction
