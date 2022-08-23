OFF = const(0)
ON = const(1)

class State:
    def __init__(self):
        self.rpm = 0
        self.lock = False
        self.shifting = False##?
        self.shiftStage = 0
        self.selectGear = None
        self.paddleGear = None
        self.gear = None
        self.nextGear = None
        self.solenoid = None
        self.adjPS = 0
        self.adjTCC = 0
        self.ps1 = 0
        self.ps2 = 0
        self.tft = 0

class Data:
    #/n88, n89, n90, n92, n282, n283/
    PARK = (OFF, OFF, ON, OFF, OFF, ON)
    REVERSE = (OFF, OFF, OFF, ON, ON, ON)
    NUETRAL = (OFF, OFF, ON, ON, ON, ON)
    FIRST = (ON, ON, ON, OFF, ON, ON)
    SECOND = (OFF, OFF, ON, OFF, ON, OFF)
    THIRD = (ON, ON, OFF, OFF, ON, ON)
    FOURTH = (ON, ON, ON, OFF, OFF, ON)
    FIFTH = (ON, ON, OFF, ON, OFF, ON)
    SIXTH = (ON, ON, ON, ON, OFF, OFF)

    SELECT_PARK = 0
    SELECT_REVERSE = 1
    SELECT_NUETRAL = 2
    SELECT_DRIVE = 3

    PADDLE_1 = 0
    PADDLE_2 = 1
    PADDLE_3 = 2
    PADDLE_4 = 3
    PADDLE_5 = 4
    PADDLE_6 = 5

    RED = (25, 0, 0)
    L_RED = (9, 0, 0)
    YELLOW = (25, 25, 0)
    ORANGE = (25, 13, 0)
    BLUE = (0, 0, 25)
    GREEN = (0, 25, 0)
    BG = (0, 0, 0)

    """
        RED = (2, 0, 0)
        L_RED = (1, 0, 0)
        YELLOW = (4, 4, 0)
        BLUE = (0, 0, 2)
        GREEN = (0, 2, 0)
        BG = (0, 0, 0)
    """
    PIN = {
        'X1': (5, 1),
        'X2': (5, 2),
        'X3': (5, 3),
        'X4': (5, 4),
        'Y9': (2, 3),
        'Y10': (2, 4)
    }
    
    #led strip order
    COLOR = (BG, GREEN, GREEN, GREEN, GREEN, GREEN, GREEN, YELLOW, ORANGE, RED, BLUE)
    
    RPM = {
        0: (COLOR[0], COLOR[0], COLOR[0], COLOR[0], COLOR[0], COLOR[0], COLOR[0], COLOR[0], COLOR[0], COLOR[0]),
        500: (COLOR[1], COLOR[0], COLOR[0], COLOR[0], COLOR[0], COLOR[0], COLOR[0], COLOR[0], COLOR[0], COLOR[0]),
        1000: (COLOR[1], COLOR[2], COLOR[0], COLOR[0], COLOR[0], COLOR[0], COLOR[0], COLOR[0], COLOR[0], COLOR[0]),
        1500: (COLOR[1], COLOR[2], COLOR[3], COLOR[0], COLOR[0], COLOR[0], COLOR[0], COLOR[0], COLOR[0], COLOR[0]),
        2000: (COLOR[1], COLOR[2], COLOR[3], COLOR[4], COLOR[0], COLOR[0], COLOR[0], COLOR[0], COLOR[0], COLOR[0]),
        2500: (COLOR[1], COLOR[2], COLOR[3], COLOR[4], COLOR[5], COLOR[0], COLOR[0], COLOR[0], COLOR[0], COLOR[0]),
        3000: (COLOR[1], COLOR[2], COLOR[3], COLOR[4], COLOR[5], COLOR[6], COLOR[0], COLOR[0], COLOR[0], COLOR[0]),
        3500: (COLOR[1], COLOR[2], COLOR[3], COLOR[4], COLOR[5], COLOR[6], COLOR[7], COLOR[0], COLOR[0], COLOR[0]),
        4000: (COLOR[1], COLOR[2], COLOR[3], COLOR[4], COLOR[5], COLOR[6], COLOR[7], COLOR[8], COLOR[0], COLOR[0]),
        4500: (COLOR[1], COLOR[2], COLOR[3], COLOR[4], COLOR[5], COLOR[6], COLOR[7], COLOR[8], COLOR[9], COLOR[0]),
        5000: (COLOR[1], COLOR[2], COLOR[3], COLOR[4], COLOR[5], COLOR[6], COLOR[7], COLOR[8], COLOR[9], COLOR[10])
    }
    #lol
    KITT = {
        0: (RED, L_RED, BG, BG, BG, BG, BG, BG, BG, BG),
        1: (L_RED, RED, BG, BG, BG, BG, BG, BG, BG, BG),
        2: (BG, L_RED, RED, BG, BG, BG, BG, BG, BG, BG),
        3: (BG, BG, L_RED, RED, BG, BG, BG, BG, BG, BG),
        4: (BG, BG, BG, L_RED, RED, BG, BG, BG, BG, BG),
        5: (BG, BG, BG, BG, L_RED, RED, BG, BG, BG, BG),
        6: (BG, BG, BG, BG, BG, L_RED, RED, BG, BG, BG),
        7: (BG, BG, BG, BG, BG, BG, L_RED, RED, BG, BG),
        8: (BG, BG, BG, BG, BG, BG, BG, L_RED, RED, BG),
        9: (BG, BG, BG, BG, BG, BG, BG, BG, L_RED, RED),
        10: (BG, BG, BG, BG, BG, BG, BG, BG, RED, L_RED),
        11: (BG, BG, BG, BG, BG, BG, BG, RED, L_RED, BG),
        12: (BG, BG, BG, BG, BG, BG, RED, L_RED, BG, BG),
        13: (BG, BG, BG, BG, BG, RED, L_RED, BG, BG, BG),
        14: (BG, BG, BG, BG, RED, L_RED, BG, BG, BG, BG),
        15: (BG, BG, BG, RED, L_RED, BG, BG, BG, BG, BG),
        16: (BG, BG, RED, L_RED, BG, BG, BG, BG, BG, BG),
        17: (BG, RED, L_RED, BG, BG, BG, BG, BG, BG, BG),
    }

    #left to right & bottom to top    
    SPACE = (BG, BG, BG, BG, BG, BG, BG, BG)
    
    N10 = (BG, BG, BG, BG, BG, BG, BG, BLUE)
    N20 = (BG, BG, BG, BG, BG, BG, BLUE, BLUE)
    N30 = (BG, BG, BG, BG, BG, BLUE, BLUE, BLUE)
    
    R = (RED, RED, RED, RED, RED, RED, RED, RED,
        RED, BG, BG, BG, RED, BG, BG, BG,
        RED, BG, BG, BG, RED, BG, BG, BG,
        RED, BG, BG, BG, RED, RED, BG, BG,
        BG, RED, RED, RED, BG, BG, RED, RED)

    P = (RED, RED, RED, RED, RED, RED, RED, RED,
        RED, BG, BG, BG, RED, BG, BG, BG,
        RED, BG, BG, BG, RED, BG, BG, BG,
        RED, BG, BG, BG, RED, BG, BG, BG,
        BG, RED, RED, RED, BG, BG, BG, BG)

    N = (RED, RED, RED, RED, RED, RED, RED, RED,
        BG, RED, BG, BG, BG, BG, BG, BG,
        BG, BG, RED, RED, BG, BG, BG, BG,
        BG, BG, BG, BG, RED, BG, BG, BG,
        RED, RED, RED, RED, RED, RED, RED, RED)
    
    G1 = (BG, BG, RED, BG, BG, BG, BG, RED,
         BG, RED, BG, BG, BG, BG, BG, RED,
         RED, RED, RED, RED, RED, RED, RED, RED,
         BG, BG, BG, BG, BG, BG, BG, RED,
         BG, BG, BG, BG, BG, BG, BG, RED)
    
    G2 = (BG, RED, RED, BG, BG, BG, RED, RED,
         RED, BG, BG, BG, BG, RED, BG, RED,
         RED, BG, BG, BG, RED, BG, BG, RED,
         RED, BG, BG, RED, BG, BG, BG, RED,
         BG, RED, RED, BG, BG, BG, BG, RED)

    G3 = (BG, RED, BG, BG, BG, RED, RED, BG,
         RED, BG, BG, BG, BG, BG, BG, RED,
         RED, BG, BG, BG, BG, BG, BG, RED,
         RED, BG, BG, RED, BG, BG, BG, RED,
         BG, RED, RED, BG, RED, RED, RED, BG)