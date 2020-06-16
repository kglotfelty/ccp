#!/usr/bin/env python

'A Simple plot GUI'

import sys

def tool():
    from pycrates import TABLECrate
    from click_click_plot import ClickClickPlotGui

    if len(sys.argv) == 2:
        infile = sys.argv[1]
        tab = TABLECrate(infile, mode="r")
    else:
        tab = None

    app = ClickClickPlotGui(tab, open_func=TABLECrate)
    app.run()


if __name__ == "__main__":
    tool()
