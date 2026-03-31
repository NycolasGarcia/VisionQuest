import sys
import cv2

from .config import WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE
from .hand_tracker import HandTracker
from .screens.title import TitleScreen
from .screens.difficulty import DifficultyScreen
from .screens.gameplay import GameplayScreen
from .screens.game_over import GameOverScreen


STATE_TITLE = "title"
STATE_DIFFICULTY = "difficulty"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game_over"


class Game:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, WINDOW_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, WINDOW_HEIGHT)

        self.tracker = HandTracker()
        self.state = STATE_TITLE

        self.title_screen = TitleScreen()
        self.difficulty_screen = DifficultyScreen()
        self.gameplay_screen = None
        self.game_over_screen = GameOverScreen()

    def run(self):
        while True:
            success, img = self.cap.read()
            if not success:
                break

            img = cv2.flip(img, 1)

            # 1. Detect hands (NO drawing yet)
            hands = self.tracker.detect(img)

            # 2. Update current screen (draws UI elements)
            action = self._update_current_screen(img, hands)

            # 3. Draw hands ON TOP of everything (cursor always visible)
            self.tracker.draw(img, hands)

            # 4. Handle state transitions
            self._handle_action(action)

            cv2.imshow(WINDOW_TITLE, img)
            if cv2.waitKey(1) == ord("q"):
                break

        self._cleanup()

    def _update_current_screen(self, img, hands):
        if self.state == STATE_TITLE:
            return self.title_screen.update(img, hands)
        elif self.state == STATE_DIFFICULTY:
            return self.difficulty_screen.update(img, hands)
        elif self.state == STATE_PLAYING:
            return self.gameplay_screen.update(img, hands)
        elif self.state == STATE_GAME_OVER:
            return self.game_over_screen.update(img, hands)
        return None

    def _handle_action(self, action):
        if action is None:
            return

        if action == "play":
            self.state = STATE_DIFFICULTY
            self.difficulty_screen.reset()

        elif action == "exit":
            self._cleanup()
            sys.exit()

        elif action.startswith("difficulty:"):
            difficulty = action.split(":", 1)[1]
            self.gameplay_screen = GameplayScreen(difficulty)
            self.state = STATE_PLAYING

        elif action == "game_over":
            self.state = STATE_GAME_OVER
            self.game_over_screen.reset(self.gameplay_screen.score)

        elif action == "play_again":
            self.state = STATE_DIFFICULTY
            self.difficulty_screen.reset()

    def _cleanup(self):
        self.tracker.release()
        self.cap.release()
        cv2.destroyAllWindows()
