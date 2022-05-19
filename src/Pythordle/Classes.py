from enum import Enum

class EMenuType(Enum):
    MENU = 1
    GAME = 2
    
class EGameStatus(Enum):
    NONE = 1
    WIN = 2
    LOSE = 3
    
    @staticmethod
    def ProperCase(Enum) -> str:
        match Enum:
            case EGameStatus.WIN:
                return "Win"
            case EGameStatus.LOSE:
                return "Lose"
            case _:
                return None

class LetterData:
    
    def __init__(self, letter: str, color=None):
        self.Letter = letter
        self.Color = color