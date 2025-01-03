#!/usr/bin/env python

'A Simple plot GUI'

import sys
import os
from tkinter import *
from tkinter.ttk import *
from tkinter.colorchooser import askcolor
from tkinter import filedialog as fd
import matplotlib.pylab as plt
import matplotlib

matplotlib.use("TkAgg")
matplotlib.interactive(True)

__all__ = ["ClickClickPlotGui", ]

class FinalPlot():
    'PNG of final plot'
    
    def __init__(self):
        from io import BytesIO
        outfile = BytesIO()
        plt.savefig( outfile, format="png")
        outfile.seek(0)  # rewind to beginning
        self.dd = outfile.read()
    
    def _repr_png_(self):
        return self.dd



class ClickClickPlotGui():
    'Plot GUI'

    def pick_col(self, txt, c0):
        """Pick column from crate"""
        _label = Label(self.main_frame, text=txt)
        _label.grid(column=c0, row=self._row, padx=(5, 5), pady=(5, 5))
        col = Combobox(self.main_frame, state="readonly")
        col.grid(column=c0+1, row=self._row, padx=(5, 5), pady=(5, 5))
        return col

    def pick_columns(self):

        self.xcol = self.pick_col("X-axis", 0)
        self.ycol = self.pick_col("Y-axis", 2)
        self.errcol = self.pick_col("Y-Error", 4)

    def pick_scaling(self, txt, c0):
        """Pick axis scaling"""
        lab = Label(self.main_frame, text=txt)
        lab.grid(column=c0, row=self._row, padx=(5, 5), pady=(5, 5))
        _scale = Combobox(self.main_frame, state="readonly")
        _scale['values'] = ["linear", "log"]
        _scale.current(0)
        _scale.grid(column=c0+1, row=self._row, padx=(5, 5), pady=(5, 5))
        return _scale

    def pick_axes_scaling(self):
        self.x_scale = self.pick_scaling("X-axis scaling", 0)
        self.y_scale = self.pick_scaling("Y-axis scaling", 2)

    def pick_line_properties(self):
        """Set line properties"""
        _default_line_width = 2

        lab = Label(self.main_frame, text="Line Style")
        lab.grid(column=0, row=self._row, padx=(5, 5), pady=(5, 5))
        self.line_style = Combobox(self.main_frame, state="readonly")
        self.line_style['values'] = ["None", "solid", "dotted", "dashdot", "dashed"]
        self.line_style.current(1)
        self.line_style.grid(column=1, row=self._row, padx=(5, 5), pady=(5, 5))

        lab = Label(self.main_frame, text="Line Color")
        lab.grid(column=2, row=self._row, padx=(5, 5), pady=(5, 5))
        self.line_color = Button(self.main_frame, text="#1f77b4", command=self.p_line)
        self.line_color.grid(column=3, row=self._row, padx=(5, 5), pady=(5, 5))

        lab = Label(self.main_frame, text="Line Width")
        lab.grid(column=4, row=self._row, padx=(5, 5), pady=(5, 5))
        v = StringVar(self.main_frame)
        v.set(_default_line_width)
        self.line_width = Spinbox(self.main_frame, from_=1, to=10, width=3)
        self.line_width.grid(column=5, row=self._row, padx=(5, 5), pady=(5, 5))
        if hasattr(self.line_width, "set"):
            self.line_width.set(_default_line_width)
        else:
            self.line_width.config(textvariable=v)

    def p_line(self):
        """Replace hex code with a nice name if one exists"""

        c = askcolor(color=self.line_color["text"],
                     parent=self.window, title='Pick a line color')
        if c[1] in self.color_map:
            self.line_color["text"] = self.color_map[c[1]]
        else:
            self.line_color["text"] = c[1]

    def pick_marker_properties(self):
        """Set marker properties"""
        _default_marker_size = 3

        lab = Label(self.main_frame, text="Marker Style")
        lab.grid(column=0, row=self._row, padx=(5, 5), pady=(5, 5))
        self.marker_style = Combobox(self.main_frame, state="readonly")
        self.marker_style['values'] = ["none", "cross", "diamond",
                                       "downtriangle", "circle", "plus",
                                       "square", "point", "uptriangle"]
        self.marker_style.current(0)
        self.marker_style.grid(column=1, row=self._row, padx=(5, 5), pady=(5, 5))

        lab = Label(self.main_frame, text="Marker Color")
        lab.grid(column=2, row=self._row, padx=(5, 5), pady=(5, 5))
        self.marker_color = Button(self.main_frame, text="black", command=self.p_marker)
        self.marker_color.grid(column=3, row=self._row, padx=(5, 5), pady=(5, 5))

        lab = Label(self.main_frame, text="Marker Size")
        lab.grid(column=4, row=self._row, padx=(5, 5), pady=(5, 5))
        v = StringVar(self.main_frame)
        v.set(_default_marker_size)
        self.marker_size = Spinbox(self.main_frame, from_=1, to=10, width=3)
        self.marker_size.grid(column=5, row=self._row, padx=(5, 5), pady=(5, 5))
        if hasattr(self.marker_size, "set"):
            # Something diff between py3.5 and py3.7
            self.marker_size.set(_default_marker_size)
        else:
            self.marker_size.configure(textvariable=v)

    def p_marker(self):
        """Replace hex code with a nice name if one exists"""

        c = askcolor(color=self.marker_color["text"],
                     parent=self.window, title='Pick a marker color')
        if c[1] in self.color_map:
            self.marker_color["text"] = self.color_map[c[1]]
        else:
            self.marker_color["text"] = c[1]

    def pick_errbar_properties(self):
        _default_errbar_size = 0

        lab = Label(self.main_frame, text="ErrorBar Color")
        lab.grid(column=2, row=self._row, padx=(5, 5), pady=(5, 5))
        self.errbar_color = Button(self.main_frame, text="black", command=self.p_errbar)
        self.errbar_color.grid(column=3, row=self._row, padx=(5, 5), pady=(5, 5))

        lab = Label(self.main_frame, text="ErrorBar Cap Size")
        lab.grid(column=4, row=self._row, padx=(5, 5), pady=(5, 5))
        v = StringVar(self.main_frame)
        v.set(_default_errbar_size)
        self.errbar_size = Spinbox(self.main_frame, from_=0, to=10, width=3)
        self.errbar_size.grid(column=5, row=self._row, padx=(5, 5), pady=(5, 5))
        if hasattr(self.errbar_size, "set"):
            # Something diff between py3.5 and py3.7
            self.errbar_size.set(_default_errbar_size)
        else:
            self.errbar_size.configure(textvariable=v)

    def p_errbar(self):
        """Replace hex code with a nice name if one exists"""

        c = askcolor(color=self.errbar_color["text"],
                     parent=self.window, title='Pick a marker color')
        if c[1] in self.color_map:
            self.errbar_color["text"] = self.color_map[c[1]]
        else:
            self.errbar_color["text"] = c[1]

    def add_title(self):
        lab = Label(self.main_frame, text="Plot Title")
        lab.grid(column=0, row=self._row, padx=(5, 5), pady=(5, 5))
        self.title = Entry(self.main_frame, width=50)
        self.title.grid(column=1, columnspan=2, row=self._row, padx=(5, 5), pady=(5, 5))

    def add_xlabel(self):
        lab = Label(self.main_frame, text="X Label")
        lab.grid(column=0, row=self._row, padx=(5, 5), pady=(5, 5))
        self.xlabel = Entry(self.main_frame, width=50)
        self.xlabel.grid(column=1, columnspan=2, row=self._row, padx=(5, 5), pady=(5, 5))

    def set_xlabel(self, *args):
        lab = self.xcol.get()
        col = self.crate.get_column(lab)
        units = col.unit
        if units and len(units) > 0:
            lab = "{} ({})".format(lab, units)

        self.xlabel.delete(0, END)
        self.xlabel.insert(END, lab)

    def add_ylabel(self):
        lab = Label(self.main_frame, text="Y Label")
        lab.grid(column=0, row=self._row, padx=(5, 5), pady=(5, 5))
        self.ylabel = Entry(self.main_frame, width=50)
        self.ylabel.grid(column=1, columnspan=2, row=self._row, padx=(5, 5), pady=(5, 5))

    def set_ylabel(self, *args):
        lab = self.ycol.get()
        col = self.crate.get_column(lab)
        units = col.unit
        if units and len(units) > 0:
            lab = "{} ({})".format(lab, units)

        self.ylabel.delete(0, END)
        self.ylabel.insert(END, lab)

    def add_buttons(self):
        self.plot_btn = Button(self.main_frame, text="Plot", command=self.make_plot)
        self.plot_btn.grid(column=1, row=self._row, padx=(5, 5), pady=(5, 5))
        self.plot_btn["state"] = "disabled"

        self.clear_btn = Button(self.main_frame, text="Clear", command=self.clear_plot)
        self.clear_btn.grid(column=2, row=self._row, padx=(5, 5), pady=(5, 5))
        self.clear_btn["state"] = "disabled"

        btn = Button(self.main_frame, text="Quit", command=self.quit)
        btn.grid(column=3, row=self._row, padx=(5, 5), pady=(5, 5))

    @staticmethod
    def map_marker_names(face):
        """Map nice names to matplotlib token"""
        _valid = {"none": "None",
                  "cross": "X",
                  "diamond": "D",
                  "downtriangle": "v",
                  "circle": "o",
                  "plus": "+",
                  "square": "s",
                  "point": ".",
                  "uptriangle": "^",
                  }
        assert face in _valid, "ERROR: Unknown marker style"
        return _valid[face]

    def next_row(self):
        self._row = self._row+1

    @staticmethod
    def make_X11_color_map():
        """
        Convert hex code to nice name, if one exists
        """
        from matplotlib.colors import cnames
        colormap = {cnames[k].lower(): k for k in cnames}
        return colormap

    def __init__(self, tab=None, open_func=None):
        'Create GUI based on a TABLECrate'

        self.open_func = open_func
        self.color_map = self.make_X11_color_map()
        self.render_ui()
        self.fp = None

        if tab is not None:
            self.populate_from_crate(tab)
        if open_func is not None:
            self.file_menu.entryconfig("Open", state="normal")

    def populate_from_crate(self, tab):
        'Fill in UI w/ info from crate'

        self.crate = tab
        self.cols = self.crate.get_colnames(vectors=False, rawonly=False)
        self.xcol['values'] = self.cols
        self.xcol.current(0)
        self.ycol['values'] = self.cols
        self.ycol.current(1)
        self.cols.insert(0, "")
        self.errcol['values'] = self.cols
        self.errcol.current(0)
        self.title.delete(0, END)
        self.title.insert(END, self.crate.get_filename())
        self.set_xlabel()
        self.set_ylabel()
        self.plot_btn["state"] = "normal"
        self.clear_btn["state"] = "normal"

    def menu_bar(self):
        menu = Menu(self.main_frame)
        self.file_menu = Menu(menu, tearoff=0)
        self.file_menu.add_command(label="Open", command=self.open, state="disabled")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Quit", command=self.quit)
        menu.add_cascade(label='File', menu=self.file_menu)
        self.window.config(menu=menu)

    def render_ui(self):
        window = Tk()
        s = Style(window)
        s.theme_use("clam")

        self.window = window

        self.window.title("Click Click Plot")
        self.main_frame = Frame(self.window)
        self.main_frame.grid(row=0,column=0,padx=5,pady=5)

        self.menu_bar()

        self._row = 0
        self.pick_columns()

        self.next_row()
        self.pick_axes_scaling()

        self.next_row()
        self.pick_line_properties()

        self.next_row()
        self.pick_marker_properties()

        self.next_row()
        self.pick_errbar_properties()

        self.next_row()
        self.add_title()

        self.next_row()
        self.add_xlabel()
        self.next_row()
        self.add_ylabel()

        self.next_row()
        self.add_buttons()

        self.xcol.bind("<<ComboboxSelected>>", self.set_xlabel)
        self.ycol.bind("<<ComboboxSelected>>", self.set_ylabel)

    def make_plot(self):
        """
        These are the actual matplotlib commands
        """
        xx = self.xcol.get()
        yy = self.ycol.get()
        yerr = self.errcol.get()

        xvals = self.crate.get_column(xx).values
        yvals = self.crate.get_column(yy).values
        plt.xlabel(self.xlabel.get())
        plt.ylabel(self.ylabel.get())
        plt.title(self.title.get())

        if "" == yerr:
            plt.plot(xvals, yvals,
                     color=self.line_color["text"],
                     linewidth=self.line_width.get(),
                     linestyle=self.line_style.get(),
                     mfc=self.marker_color["text"],
                     mec=self.marker_color["text"],
                     marker=self.map_marker_names(self.marker_style.get()),
                     markersize=self.marker_size.get()
                     )
        else:
            errvals = self.crate.get_column(yerr).values
            plt.errorbar(xvals, yvals, yerr=errvals,
                         color=self.line_color["text"],
                         linewidth=float(self.line_width.get()),
                         linestyle=self.line_style.get(),
                         mfc=self.marker_color["text"],
                         mec=self.marker_color["text"],
                         marker=self.map_marker_names(self.marker_style.get()),
                         markersize=float(self.marker_size.get()),
                         ecolor=self.errbar_color["text"],
                         capsize=float(self.errbar_size.get())
                         )

        plt.xscale(self.x_scale.get())
        plt.yscale(self.y_scale.get())
        plt.show()

    def clear_plot(self):
        plt.clf()

    def run(self):
        self.window.update()
        self.window.mainloop()
        return self.fp

    def quit(self):
        self.fp = FinalPlot()
        plt.close()
        self.window.quit()
        self.window.destroy()
        

    def open(self):
        fname = fd.askopenfilename()
        if 0 == len(fname):
            return
        tab = self.open_func(fname, mode="r")
        self.populate_from_crate(tab)

