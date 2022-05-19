import sys
from Pythordle import Game

if len(sys.argv) > 1 and sys.argv[1] == '-debug':
    Game.Debug = True


Game.Run()
