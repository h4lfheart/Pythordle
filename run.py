import os
import sys
import ctypes

ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0) # Hide pip/raylib consoles

os.system('pip install -r requirements.txt')
os.system('py src/main.py' + (" -debug" if len(sys.argv) > 1 and sys.argv[1] == '-debug' else ""))
