#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 11:34:32 2018

@author: rday

MIT License

Copyright (c) 2018 Ryan Patrick Day

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""

import numpy as np

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import TypeK_read as thermc

import tkinter as tk
from tkinter import filedialog

import datetime as dt
import time

class interface:

    def __init__(self):

        self.thermometer = thermc.type_K(9,23.7)

        self.running = False
        self.recur_id = None
        self.starttime = None
        self.T1 = []
        self.times = []
        self.interval = 1500
        self.filename  = 'HeaterFile.txt'
        self.starttime = dt.datetime.now()


        self.setup_gui()

    def savefile(self):
        self.filename = filedialog.asksaveasfilename()
        if self.filename[-4:]!='.txt':
            self.filename = self.filename + '.txt'
        write_string = 'Timestamp\tTemp 1 (C)\n'
        self.write(write_string,'w')
        self.starttime = dt.datetime.now()

    def do_quit(self):
        self.thermometer.device._disconnect()
        self.root.destroy()

    def startstop(self):

        if not self.running:
            self.running = True
            self.run_label.set('STOP')
            self.quit_button.config(state='disabled')
            self.save_button.config(state='disabled')
            self.recur_id = self.root.after(self.interval,self.do_task)
        else:
            self.run_label.set('START')
            self.quit_button.config(state='normal')
            self.save_button.config(state='normal')
            self.running = False
            
            self.root.after_cancel(self.recur_id)
            self.recur_id = None

    def write(self,write_string,mode):
        
        try:
            with open(self.filename,mode) as tofile:
                tofile.write(write_string)
        except FileNotFoundError:
            print('ERROR: Choose file destination!')
            self.startstop()

    def do_get_T(self):
        T1 = self.thermometer.measure_T()
        try:

            if abs(T1-self.T1[-1])>abs(self.T1[-1])*0.15:
                T1 = self.thermometer.measure_T()
        except IndexError:
            next
        return T1
    
    def do_task(self):

        self.time_now = dt.datetime.now()

        T1= self.do_get_T()

        self.T1.append(T1)
        
        self.times.append((self.time_now-self.starttime).total_seconds())
        write_string = '{:%H:%M:%S %d/%m/%Y}\t{:0.02f}\n'.format(self.time_now,T1)
        self.write(write_string,'a')
        self.update_plot()
        self.T1now.set('T1: {:0.2f} C'.format(self.T1[-1]))
        self.recur_id = self.root.after(self.interval,self.do_task)
        
    def update_plot(self):

        self.ax.cla()

        self.line1, = self.ax.plot(self.times,self.T1)

        self.fig.canvas.draw()
        

    def setup_gui(self):
        self.root = tk.Tk()
        self.root.configure(background='white')
        self.root.wm_title('MOORE HEATER PROFILER')
        self.run_label = tk.StringVar()
        self.run_label.set('START')

        self.fig = Figure(figsize=(5,3))
        self.ax = self.fig.add_subplot(111)
        self.line1, = self.ax.plot(self.times,self.T1)
        
        self.window = FigureCanvasTkAgg(self.fig,master=self.root)
        self.window.get_tk_widget().grid(row=0,column=0,columnspan=5,rowspan=3)


       
        self.T1now = tk.StringVar()

       
        print(self.T1now.get())

        self.T1_label = tk.Label(master=self.root,textvariable=self.T1now).grid(row=10,column=0,columnspan=5)
        self.T1now.set('T1:     C')

     
        self.run_button = tk.Button(master=self.root,textvariable = self.run_label,command=self.startstop,bg='white')
        self.run_button.grid(row=11,column=0)

        self.save_button = tk.Button(master=self.root,text='SAVE',command=self.savefile,bg='white')
        self.save_button.grid(row=11,column=2)

        self.quit_button = tk.Button(master=self.root,text='QUIT',command=self.do_quit,bg='white')
        self.quit_button.grid(row=11,column=4)
                              



if __name__ == "__main__":


    inter = interface()

    inter.root.mainloop()

