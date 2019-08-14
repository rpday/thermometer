#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 22 13:33:23 2019

@author: ryanday
"""
import numpy as np
from scipy.interpolate import interp1d
#import HPGPIB
import dummy_HPIB as HPGPIB

filename = 'TypeK_Calibration.txt'

class type_K:
    '''
    This class is a stand-in for a type-c thermocouple. Using a text-file
    based calibration table, a voltage reading, given a fixed temperature reference,
    can be used to then extract an evaluation of the temperature probed by the 
    thermocouple. A reliable reference temperature must be given to trust the output.
    
    '''
    def __init__(self,address,Tref):
        self.Tdata,self.Vdata = load_calibration(filename)
        self.Tinterp_exec = self.temp_interp()
        
        self.Vinterp_exec = self.volt_interp()
        
        self.Tref = Tref
        self.Vref = self.Vinterp_exec(self.Tref)
        
        self.V_to_T = self.V_exec()
        self.device = HPGPIB.HP3478A(address)
        
        
        
        
    
    def temp_interp(self):
        '''
        Define an executable spline function converting 
        an input voltage to an output temperature. 
        '''
        
        return interp1d(self.Vdata,self.Tdata)
        
    def volt_interp(self):
        '''
        Define an executable spline function converting 
        an input temperature to an output voltage. 
        '''
        
        return interp1d(self.Tdata,self.Vdata)
    
    def V_exec(self):
        '''
        Define the executable function which will be used in practice.
        The multimeter reading is combined with the reference temperature
        to provide an accurate measure of the thermocouple temperature. 
        '''
        return lambda x: self.Tinterp_exec(x+self.Vref)
    
    def measure_T(self):
        '''
        
        '''
        
        return self.V_to_T(self.device._do_dcv_measure()*1000)
        
        
        

def load_calibration(filename):
    '''
    Load Type-K calibration curve, as from NIST. Had to manually fix
    two incorrect datapoints which were off by an integer # of degrees C.

    *args*:
        - **filename**: string, data file
        
    *return*:
        - **temperatures**, **voltages**: lists of float, indicating the temperatures
        and voltages on the calibration curve.
    '''
    temperatures = []
    voltages = []
    with open(filename,'r') as origin:
        for line in origin:
            try:
                numbers = [float(li) for li in line.split()[:-1]]
            except:
                continue
            if len(numbers) == 12:
                temperatures = temperatures + [numbers[0] + ii for ii in range(10)]
                voltages = voltages + [ni for ni in numbers[1:-1]]
    return np.array(temperatures),np.array(voltages)



if __name__ == "__main__":
    
    my_thermometer = type_K(9,0)
