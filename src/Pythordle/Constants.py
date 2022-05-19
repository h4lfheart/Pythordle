import raylib as rl

def Init():
    global WinSound
    WinSound = rl.LoadSound(b"src/resources/win.ogg")
    
    global LoseSound
    LoseSound = rl.LoadSound(b"src/resources/lose.ogg")
    
    global EnterSound
    EnterSound = rl.LoadSound(b"src/resources/enter.wav")
    
    global DeleteSound
    DeleteSound = rl.LoadSound(b"src/resources/delete.wav")
    
    global InvalidSound
    InvalidSound = rl.LoadSound(b"src/resources/invalid.wav")
    
    global AddSound
    AddSound = rl.LoadSound(b"src/resources/add.wav")
    
    global Icon
    Icon = rl.LoadImage(b"src/resources/icon.png")
    
WinSound = None
LoseSound = None
EnterSound = None
DeleteSound = None
InvalidSound = None
AddSound = None

Icon = None

ValidLetters = [rl.KEY_A, rl.KEY_B, rl.KEY_C, rl.KEY_D, rl.KEY_E, rl.KEY_F, rl.KEY_G, rl.KEY_H, rl.KEY_I, 
                rl.KEY_J, rl.KEY_K, rl.KEY_L, rl.KEY_M, rl.KEY_N, rl.KEY_O, rl.KEY_P, rl.KEY_Q, rl.KEY_R, 
                rl.KEY_S, rl.KEY_T, rl.KEY_U, rl.KEY_V, rl.KEY_W, rl.KEY_X, rl.KEY_Y, rl.KEY_Z]

BackgroundColor = rl.ColorFromHSV(0, 0, 0.88)
GreenColor = rl.ColorFromHSV(125, 0.51, 0.7)
YellowColor = rl.ColorFromHSV(47, 0.59, 1.0)
TransparentGray = rl.ColorAlpha(rl.ColorFromHSV(0, 0, 0), 0.5)

KeyboardTop = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P']
KeyboardMiddle = ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L']
KeyboardBottom = ['Z', 'X', 'C', 'V', 'B', 'N', 'M']