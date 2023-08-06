"""
To run circadian_desktops library module as a script:
python -m circadian_desktops
Alternatively, run:
python C:\\path\\to\\folder\\circadian_desktops
"""

import os
import subprocess
import sys

exe_dir, exe_name = os.path.split(sys.executable)
if not exe_name.startswith("pythonw"):
    exe_name = exe_name.replace("python", "pythonw", 1)
    exe_path = os.path.join(exe_dir, exe_name)
os.chdir(os.path.dirname(os.path.abspath(__file__)))
if "/noshow" in sys.argv:
    subprocess.Popen([exe_path, "app.py", "/noshow"])
else:
    subprocess.Popen([exe_path, "app.py"])
sys.exit(0)
