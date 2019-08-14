#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Created Wed 22 May 15:18:00 2019

@author:rday

"""
import visa


rm = visa.ResourceManager()

class HP3478A:
    
    def __init__(self,HPIB_address):
        
        self.address = 'GPIB0::{:d}::INSTR'.format(HPIB_address)
        self.instrument = self._connect()
        
        
    
        
        
    def _connect(self):
        
        return rm.open_resource(self.address)
    
    
    def _read_screen(self):
        
        print(self.instrument.query("*IDN?"))
        
        
        
    def _disconnect(self):
        
        self.instrument.before_close()
        self.instrument.close()
        
    def _do_acv_measure(self):
        '''
        AC voltage measurement (F2)
        Autorange (RA)
        Autozero on (Z1)
        4.5 digits (N4) -- F2RAZ1N4: returns an ac voltage measurement
        '''
        return float(self.instrument.query("F2RAZ1N4"))
    
    
    def _do_dcv_measure(self):    
        '''
        DC voltage measurement (F1)
        Autorange (RA)
        Autozero on (Z1)
        4.5 digits (N4) -- F1RAZ1N4: returns a dc voltage measurement.
        '''
        return float(self.instrument.query("F1RAZ1N4"))