"""
To run circadian_desktops library module as a script:
pythonw -m circadian_desktops
Alternatively, run:
pythonw C:\\path\\to\\folder\\circadian_desktops
"""

import os
import subprocess
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
if "/noshow" in sys.argv:
    subprocess.Popen([sys.executable, "app.py", "/noshow"])
else:
    subprocess.Popen([sys.executable, "app.py"])
sys.exit(0)
