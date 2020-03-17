#!/usr/bin/env python


import sys
import os

from tkinter import *
from tkinter.ttk import *
import matplotlib.pylab as plt
import matplotlib


class ClickClickPlotGui():

    def __init__(self,tab):
        window = Tk()

        window.title("Click Click Plot")

        window.geometry('350x200')

        cols = tab.get_colnames(vectors=False,rawonly=False)

        x_label = Label(window, text="X-Axis")
        x_label.grid(column=0, row=0)
        self.xcol = Combobox(window)
        self.xcol['values']=cols
        self.xcol.current(0) 
        self.xcol.grid(column=1, row=0)

        y_label = Label(window, text="Y-Axis")
        y_label.grid(column=0, row=1)
        self.ycol = Combobox(window)        
        self.ycol['values']=cols
        self.ycol.current(1)
        self.ycol.grid(column=1, row=1)

        btn = Button(window, text="Plot", command=self.make_plot)
        btn.grid(column=1, row=2)

        btn = Button(window, text="Clear", command=self.clear_plot)
        btn.grid(column=2, row=2)

        # Add Combobox's for line style, spin for line width
        # Add Comobbox's for marker face, spin for symbol size
        # Add combobox for log/linear, x&y
        # color chooser

        self.window=window
        self.crate = tab

        
    def make_plot(self):
        xx=self.xcol.get()
        yy=self.ycol.get()
        
        matplotlib.use("TkAgg")
        matplotlib.interactive(True)
        xvals = self.crate.get_column(xx).values
        yvals = self.crate.get_column(yy).values
        plt.xlabel(xx)
        plt.ylabel(yy)
        plt.title(infile)

        plt.plot( xvals, yvals)
        plt.show()
        
    def clear_plot(self):
        plt.clf()

    def run(self):
        self.window.mainloop()

    def __del__(self):
        plt.close()



if __name__ == "__main__":
    
    assert len(sys.argv)==2, "Usage: click_click_plot infile"
    
    infile=sys.argv[1]
    #infile="pcadf072039163N004_asol1.fits"

    from pycrates import TABLECrate
    tab = TABLECrate(infile, mode="r")

    app = ClickClickPlotGui(tab)
    app.run()
