

import os
import sys

assert "ASCDS_INSTALL" in os.environ, "Please setup for CIAO before installing"

from distutils.core import setup

setup( name='click_click_plot',
       version='0.1.0',
       description='Simple UI to matplotlib',
       author='Anonymous',
       author_email='WhoDat@cfa.harvard.edu',
       url='https://github.com/kglotfelty/ccp/',
       py_modules=["click_click_plot", ],
       scripts=["ccp", ],                    
    )
