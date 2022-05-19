import raylib as rl
from cmath import sin
from Pythordle.Game import W, H

def HCenterText(text: str, Y: int, size: int, col):
    TextLength = rl.MeasureText(text, size)
    rl.DrawText(text, int(W/2)-int(TextLength/2), Y, size, col)
    
def Bounce(speed=1.0, min=0, max=1) -> float:
    return int(abs(sin(rl.GetTime()*speed))*(max-min))+min

def DrawBox(xy, uv, t, c):
    rl.DrawLineEx(xy, (xy[0]+uv[0], xy[1]), t, c)
    rl.DrawLineEx(xy, (xy[0], xy[1]+uv[1]), t, c)
    rl.DrawLineEx((xy[0], xy[1]+uv[1]), (xy[0]+uv[0], xy[1]+uv[1]), t, c)
    rl.DrawLineEx((xy[0]+uv[0], xy[1]), (xy[0]+uv[0], xy[1]+uv[1]), t, c)
    
def FindOccurance(func, target, default=None):
    if not target:
        return default
    return next(filter(func, target), default)