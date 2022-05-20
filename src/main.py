import sys
from Pythordle import Game

if '-debug' in sys.argv:
    Game.Debug = True
if '-party' in sys.argv:
    Game.Party = True


Game.Run()
