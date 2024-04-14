# randomness configuration
SEED = 0
RESET_RNG_ON_GAME_RESTART = False

# pygame constants
WINDOW_SIZE = 600
FPS_CAP = 60
GAP_SIZE = 5

# game configuration
GRID_SIZE = 4
STARTING_TILES = 2
COLORS = {
    0:       (    200,    200,    200    ),
    2:       (    144,    238,    144    ),
    4:       (    150,    236,    135    ),
    8:       (    157,    235,    126    ),
    16:      (    164,    233,    117    ),
    32:      (    171,    232,    108    ),
    64:      (    178,    230,    99     ), 
    128:     (    185,    229,    89     ), 
    256:     (    192,    227,    81     ), 
    512:     (    199,    226,    72     ), 
    1024:    (    206,    225,    63     ), 
    2048:    (    213,    223,    54     ), 
    4096:    (    220,    222,    44     ), 
    8192:    (    227,    220,    36     ), 
    16384:   (    234,    219,    27     ), 
    32768:   (    241,    217,    17     ), 
    65536:   (    248,    216,    8      ),  
    131072:  (    255,    215,    0      ),
}

# global helper functions based on constants
def GET_TILE_COLOR(value):
    if value in COLORS:
        return COLORS[value]
    else:
        return (255, 70, 70)

