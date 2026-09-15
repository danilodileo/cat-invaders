"""Tunable constants for Cat Invaders."""

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
CAPTION = "Cat Invaders: Operation Chill Out"

# --- Colors -----------------------------------------------------------
BG_COLOR = (18, 14, 34)
BG_COLOR_2 = (28, 20, 48)
STAR_COLOR = (220, 220, 255)
TEXT_COLOR = (245, 245, 250)
ACCENT_COLOR = (255, 189, 89)
DANGER_COLOR = (255, 90, 90)
SUCCESS_COLOR = (120, 230, 160)

PLAYER_COLOR = (255, 200, 120)
PLAYER_EYE_COLOR = (30, 20, 10)
PROJECTILE_COLOR = (255, 150, 200)
ALIEN_COLORS = [
    (150, 200, 255),  # back row - calmest colour, highest value
    (170, 255, 190),
    (255, 210, 130),
    (255, 140, 140),  # front row - angriest, lowest value
]
ALIEN_CALM_COLOR = (255, 255, 255)
HAIRBALL_COLOR = (200, 170, 140)
MOTHERSHIP_COLOR = (200, 160, 255)

# --- Player -------------------------------------------------------------
PLAYER_PIXEL_SIZE = 5
PLAYER_SPEED = 340  # px/s
PLAYER_LIVES = 3
PLAYER_SHOOT_COOLDOWN = 0.45  # seconds between shots
PLAYER_INVULNERABLE_TIME = 1.5  # seconds of grace after being hit

# --- Projectiles ----------------------------------------------------------
PROJECTILE_PIXEL_SIZE = 4
PROJECTILE_SPEED = 480
HAIRBALL_PIXEL_SIZE = 4
HAIRBALL_SPEED = 220

# --- Alien swarm ------------------------------------------------------
ALIEN_PIXEL_SIZE = 4
ALIEN_ROWS = 4
ALIEN_COLS = 8
ALIEN_H_SPACING = 62
ALIEN_V_SPACING = 46
ALIEN_TOP_MARGIN = 70
ALIEN_SIDE_MARGIN = 60
ALIEN_STEP_DOWN = 18
ALIEN_BASE_INTERVAL = 0.85  # seconds between swarm steps at full strength
ALIEN_MIN_INTERVAL = 0.09
ALIEN_ROW_POINTS = [40, 30, 20, 10]  # back row worth the most
ALIEN_CALM_DURATION = 0.6  # seconds of "aww" animation before leaving

ENEMY_FIRE_BASE_CHANCE = 0.10  # chance per swarm step that a column fires
ENEMY_FIRE_LEVEL_SCALING = 0.01

# --- Mothership bonus ---------------------------------------------------
MOTHERSHIP_MIN_DELAY = 12.0
MOTHERSHIP_MAX_DELAY = 22.0
MOTHERSHIP_SPEED = 160
MOTHERSHIP_POINTS = 150

# --- Progression --------------------------------------------------------
DANGER_LINE_Y = SCREEN_HEIGHT - 110  # aliens reaching this line end the game

HIGH_SCORE_FILE = "cat_invaders_highscore.json"
