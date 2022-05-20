import os
import sys
import ctypes

ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0) # Hide pip/raylib consoles

os.system('pip install -r requirements.txt')
sys.argv.pop(0)
launchCommand = 'py src/main.py '
for arg in sys.argv:
    launchCommand += arg + ' '
os.system(launchCommand)
