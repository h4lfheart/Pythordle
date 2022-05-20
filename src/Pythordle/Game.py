# Globals
W = 640
H = 960

import raylib as rl
import random
import json
from Pythordle import Constants
from Pythordle.Classes import EGameStatus, EMenuType, LetterData
from Pythordle.Utils import HCenterText, Bounce, DrawBox, FindOccurance, Rainbow

CorrectWord = 'SLING'
Debug = False
Party = False
__LetterCountCorrect = {}

__CurrentMenu = EMenuType.MENU
__GameStatus = EGameStatus.NONE

__InvalidTimer = 0

GuessWordList = []
TargetWordList = []
def Run():
    global __InvalidTimer
    with open('src/words.json') as WordFile:
        global GuessWordList
        GuessWordList = json.loads(WordFile.read())
    with open('src/validwords.json') as WordFile:
        global TargetWordList
        TargetWordList = json.loads(WordFile.read())
    rl.InitWindow(W, H, b"Pythordle")
    rl.InitAudioDevice()
    Constants.Init()
    rl.SetTargetFPS(60)
    rl.HideCursor()
    rl.SetWindowState(rl.FLAG_WINDOW_UNDECORATED)
    rl.SetWindowIcon(Constants.Icon)
    #rl.SetExitKey(0)
    InvokeWord()
    
    while not rl.WindowShouldClose():
        rl.BeginDrawing()
        rl.ClearBackground(Constants.BackgroundColor if not Party else Rainbow())
        if (__InvalidTimer >= 0):
            __InvalidTimer -= rl.GetFrameTime()
        else:
            __InvalidTimer = 0
        match __CurrentMenu:
            case EMenuType.MENU:
                __DrawMenu()
            case EMenuType.GAME:
                __DrawGame()
        
        rl.EndDrawing()
    
def InvokeWord():
    global CorrectWord
    CorrectWord = TargetWordList[random.randint(0, len(TargetWordList)-1)].upper()
    for Letter in CorrectWord:
        if Letter in __LetterCountCorrect:
            __LetterCountCorrect[Letter] += 1
        else:
            __LetterCountCorrect[Letter] = 1
    
  
__PlayColor = list(rl.LIGHTGRAY)  
def __DrawMenu():
    HCenterText(b"Pythordle", 50, 80, rl.DARKGRAY)
    rl.DrawText(b"y", 176, 50, 80, Constants.GreenColor)
    rl.DrawText(b"d", 408, 50, 80, Constants.GreenColor)
    rl.DrawText(b"t", 224, 50, 80, Constants.YellowColor)
    rl.DrawText(b"r", 360, 50, 80, Constants.YellowColor)
    rl.DrawText(b"e", 480, 50, 80, Constants.YellowColor)
    
    __PlayColor[3] = Bounce(speed=1.5, max=255) # Alpha Channel
    HCenterText(b"Press Space to Play", H-80, 40, __PlayColor)
    
    if rl.IsKeyPressed(rl.KEY_SPACE):
        global __CurrentMenu
        __CurrentMenu = EMenuType.GAME

# Position, (Letter, BackgroundColor)
__LetterMatrix = {}

__ColorByLetter = {}
__GlobalGreen = []
__CurrentPosition = [0, 0]
__CurrentBoxColor = list(rl.DARKGRAY)  
def __DrawGame():
    global __GameStatus
    global __InvalidTimer
    global __CurrentPosition 
    global __LetterMatrix
    global __ColorByLetter
    global __GlobalGreen
    global __CurrentMenu
    __CurrentBoxColor[3] = Bounce(speed=2.0, max=255)
    __PlayColor[3] = Bounce(speed=1.5, max=255) # Alpha Channel
    
    
    __DrawKeyboardLayer(30, 740, Constants.KeyboardTop)
    __DrawKeyboardLayer(50, 800, Constants.KeyboardMiddle)
    __DrawKeyboardLayer(110, 860, Constants.KeyboardBottom)
    
    if Debug:
        HCenterText(bytes(f"DEBUG: Word is {CorrectWord}", 'utf-8'), H-30, 20, rl.DARKGRAY)
        
    # Draw Background Box Colors
    for Position, Data in __LetterMatrix.items():
        if not Data.Color:
            continue
        
        ColPos = Position[0]*110 + 50
        RowPos = Position[1]*110 + 50
        rl.DrawRectangle(ColPos, RowPos, 100, 100, Data.Color)
    
    # Draw Boxes
    for Row in range(6):
        RowPos = Row*110 + 50
        for Col in range(5):
            ColPos = Col*110 + 50
            BoxColor =  __CurrentBoxColor if __CurrentPosition == [Col, Row] and __GameStatus == EGameStatus.NONE else rl.LIGHTGRAY
            DrawBox((ColPos, RowPos), (100, 100), 5, BoxColor)
    
    # Draw Letters
    for Position, Data in __LetterMatrix.items():
        ColPos = Position[0]*110 + 80
        RowPos = Position[1]*110 + 70
        rl.DrawText(bytes(Data.Letter, 'utf-8'), ColPos, RowPos, 70, rl.WHITE if Data.Color else rl.GRAY)
        
    if __InvalidTimer > 0:
        HCenterText(b"Not in Word List!", 6, 40, rl.GRAY)
        
    if __GameStatus != EGameStatus.NONE:
        rl.DrawRectangle(0, 0, W, H, Constants.TransparentGray)
        HCenterText(bytes(f"You {EGameStatus.ProperCase(__GameStatus)}!", 'utf-8'), int(H/2)-60, 120, rl.RAYWHITE)
        if __GameStatus == EGameStatus.LOSE:
            HCenterText(bytes(f"The Word was {CorrectWord}", 'utf-8'), int(H/2)+60, 40, rl.RAYWHITE)
        
        HCenterText(b"Press Space to Play Again", H-80, 40, __PlayColor)
        
        if rl.IsKeyPressed(rl.KEY_SPACE):
            ClearGame()
            InvokeWord()
                
    # Handle Key Events
    if not (Key := rl.GetKeyPressed()) or __GameStatus != EGameStatus.NONE:
        return # Everything from here on out requires a valid key press, all drawing is above

    # Set Letter
    if Key in Constants.ValidLetters and __CurrentPosition[0] < 5:
        __LetterMatrix[tuple(__CurrentPosition)] = LetterData(chr(Key))
        __CurrentPosition[0] += 1
        rl.PlaySound(Constants.AddSound)
        
    # Remove Letter
    elif Key == rl.KEY_BACKSPACE:
        TargetItem = __CurrentPosition
        TargetIdx = __CurrentPosition[0]-1
        if TargetIdx >= 0:
            TargetItem[0] = TargetIdx
            __LetterMatrix.pop(tuple(TargetItem))
            rl.PlaySound(Constants.DeleteSound)
        else:
            rl.PlaySound(Constants.InvalidSound)
        
    # Submit word guess
    elif Key == rl.KEY_ENTER and __CurrentPosition[0] == 5:
    
        GuessWord = ''
        CorrectInRow = 0
        CorrectLetters = []
        LetterCountGuess = {}
        LetterCountGuess.clear()
        
        # Check List
        for Position, Data in __LetterMatrix.items():
            if not __CurrentPosition[1] == Position[1]:
                continue
        
            GuessWord += Data.Letter
            
        if GuessWord.lower() not in TargetWordList and GuessWord.lower() not in GuessWordList:
            __InvalidTimer = 1
            rl.PlaySound(Constants.InvalidSound)
            return
        
        # Check for correct position
        for Position, Data in __LetterMatrix.items():
            if not __CurrentPosition[1] == Position[1]: # only check current row
                continue
            
            
            if Data.Letter in LetterCountGuess:
                LetterCountGuess[Data.Letter] += 1
            else:
                LetterCountGuess[Data.Letter] = 1
              
            if CorrectWord[Position[0]] == Data.Letter:
                Data.Color = Constants.GreenColor
                __ColorByLetter[Data.Letter] = Data.Color
                CorrectLetters.append(Data.Letter)
                __GlobalGreen.append(Data.Letter)
                CorrectInRow += 1
            else:
                if Data.Color == Constants.YellowColor:
                    continue
                Data.Color = rl.DARKGRAY
                if Data.Letter not in __GlobalGreen:
                    __ColorByLetter[Data.Letter] = Data.Color
            
        # Then check for correct letters
        for Position, Data in __LetterMatrix.items():
            if not __CurrentPosition[1] == Position[1]: # only check current row
                continue
            

            if Data.Letter in CorrectWord and __LetterCountCorrect[Data.Letter] > 0 and LetterCountGuess[Data.Letter] <= __LetterCountCorrect[Data.Letter] and Data.Color != Constants.GreenColor:
                Data.Color = Constants.YellowColor
                __ColorByLetter[Data.Letter] = Data.Color
        
        
            
        __CurrentPosition[0] = 0
        __CurrentPosition[1] += 1
        
        if CorrectInRow == 5:
            __GameStatus = EGameStatus.WIN
            rl.PlaySound(Constants.WinSound)
            return
        
        if __CurrentPosition[1] >= 6:
            __GameStatus = EGameStatus.LOSE
            rl.PlaySound(Constants.LoseSound)
            return
        
        rl.PlaySound(Constants.EnterSound)
            
def __DrawKeyboardLayer(xoffset, yoffset, layer):
    for Idx, Letter in enumerate(layer):   
        ColPos = Idx*60+xoffset
        RowPos = yoffset
        if LetterColor := __ColorByLetter.get(Letter):
            rl.DrawRectangle(ColPos, RowPos, 50, 50, LetterColor)
            DrawBox((ColPos, RowPos), (50, 50), 3, LetterColor)
        else:
            rl.DrawRectangle(ColPos, RowPos, 50, 50, rl.LIGHTGRAY)
            DrawBox((ColPos, RowPos), (50, 50), 3, rl.LIGHTGRAY)
            
        rl.DrawText(bytes(Letter, 'utf-8'), ColPos+14, RowPos+10, 35, rl.WHITE)
        
def ClearGame():
    global __CurrentMenu
    global __CurrentPosition
    global __GameStatus
    __CurrentMenu = EMenuType.GAME
    __CurrentPosition = [0, 0]
    __LetterMatrix.clear()
    __LetterCountCorrect.clear()
    __ColorByLetter.clear()
    __GlobalGreen.clear()
    __GameStatus = EGameStatus.NONE
