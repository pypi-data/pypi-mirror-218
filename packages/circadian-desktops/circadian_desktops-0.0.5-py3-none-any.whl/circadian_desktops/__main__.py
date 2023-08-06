"""
To run circadian_desktops library module as a script:
pythonw -m circadian_desktops
Alternatively, run:
pythonw C:\\path\\to\\folder\\circadian_desktops
"""

import os

import circadian_desktops.app

os.chdir(os.path.dirname(os.path.abspath(__file__)))
circadian_desktops.app.main()
