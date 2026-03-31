import os
import cv2

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
IMAGES_DIR = os.path.join(ASSETS_DIR, "images")
SOUNDS_DIR = os.path.join(ASSETS_DIR, "sounds")

# Window
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_TITLE = "VisionQuest"

# Hand tracking
PINCH_THRESHOLD = 50
MAX_HANDS = 2
DETECTION_CONFIDENCE = 0.7
TRACKING_CONFIDENCE = 0.7
FINGER_RADIUS = 12
CURSOR_RADIUS = 18
CURSOR_COLOR = (255, 100, 0)      # Blue-ish circle (BGR)
CURSOR_PINCH_COLOR = (0, 255, 0)  # Green when pinching

# Colors (BGR)
GOLD = (0, 215, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 200, 0)
BRIGHT_GREEN = (0, 255, 0)
RED = (0, 0, 220)
YELLOW = (0, 255, 255)
GRAY = (200, 200, 200)
DARK_GRAY = (80, 80, 80)
LIGHT_BLUE = (230, 200, 150)
DARK_BLUE = (140, 80, 30)
ORANGE = (0, 140, 255)
BG_DARK = (40, 35, 30)
BG_PANEL = (50, 45, 40)
ACCENT = (0, 200, 255)         # Warm yellow-orange accent

# Scoring
MAX_SCORE = 10
BONUS_STREAK = 3
MAX_LIVES = 3

# Timing (seconds)
FEEDBACK_DURATION = 2.0
CLICK_COOLDOWN = 0.5
COLLAB_COOLDOWN = 2.0
GAME_OVER_DELAY = 1.5
DIFFICULTY_DELAY = 1.0
DWELL_TIME = 1.0    # Hold over button for 1s to confirm click

# Cartesian plane (shifted down to avoid HUD overlap)
PLANE_STEP = 35
PLANE_CENTER = (640, 420)
PLANE_WIDTH = PLANE_STEP * 32
PLANE_HEIGHT = PLANE_STEP * 16
POINT_TOLERANCE = 40

# Fonts
FONT = cv2.FONT_HERSHEY_SIMPLEX
FONT_TITLE = cv2.FONT_HERSHEY_TRIPLEX

# Progress bar
PROGRESS_BAR_WIDTH = 300
PROGRESS_BAR_HEIGHT = 30

# Collaborators
COLLABORATORS = [
    {
        "name": "Lucas Silva",
        "image": "lucas_silva.png",
        "link": "https://www.linkedin.com/in/lucaslopesdasilva/",
    },
    {
        "name": "Nycolas Garcia",
        "image": "nycolas_garcia.png",
        "link": "https://www.linkedin.com/in/nycolasagrgarcia/",
    },
    {
        "name": "Danilo Santos",
        "image": "danilo_santos.png",
        "link": "https://www.linkedin.com/in/danilodoes/",
    },
    {
        "name": "Breno Melo",
        "image": "breno_melo.png",
        "link": "https://www.linkedin.com/in/breno-melo-53822a20a/",
    },
]
