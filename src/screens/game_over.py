import time
import cv2

from ..config import (
    FONT, FONT_TITLE, BLACK, WHITE, GRAY, DARK_GRAY, ACCENT,
    GREEN, RED, GOLD, GAME_OVER_DELAY,
)
from ..button import Button
from ..hand_tracker import get_cursors, get_pinches


class GameOverScreen:
    def __init__(self):
        self.start_time = 0
        self.score_data = None
        self.play_btn = None
        self.exit_btn = None

    def reset(self, score_system=None):
        self.start_time = time.time()
        self.play_btn = None
        self.exit_btn = None
        if score_system:
            self.score_data = {
                "score": score_system.score,
                "correct": score_system.correct_count,
                "wrong": score_system.wrong_count,
                "streak": score_system.streak,
                "lives": score_system.lives,
                "is_win": score_system.is_win,
            }

    def update(self, img, hands):
        """Draw and process. Returns 'play_again', 'exit', or None."""
        h, w = img.shape[:2]

        # Dark overlay
        overlay = img.copy()
        cv2.rectangle(overlay, (0, 0), (w, h), (20, 20, 20), -1)
        cv2.addWeighted(overlay, 0.7, img, 0.3, 0, img)

        # Frame
        fx, fy = 180, 100
        fw, fh = w - 360, h - 200
        cv2.rectangle(img, (fx, fy), (fx + fw, fy + fh), DARK_GRAY, cv2.FILLED)
        cv2.rectangle(img, (fx, fy), (fx + fw, fy + fh), ACCENT, 2)

        # Title
        is_win = self.score_data and self.score_data["is_win"]
        if is_win:
            title = "PARABENS!"
            title_color = GOLD
        else:
            title = "FIM DE JOGO"
            title_color = RED

        ts = cv2.getTextSize(title, FONT_TITLE, 2.0, 3)[0]
        tx = fx + (fw - ts[0]) // 2
        cv2.putText(img, title, (tx, fy + 80), FONT_TITLE, 2.0, title_color, 3)

        # Stats
        if self.score_data:
            stats_x = fx + 80
            stats_y = fy + 150
            line_h = 45

            if is_win:
                msg = "Voce atingiu a pontuacao maxima!"
            else:
                msg = "Suas vidas acabaram!"
            cv2.putText(img, msg, (stats_x, stats_y), FONT, 0.8, WHITE, 2)
            stats_y += line_h + 10

            stats = [
                (f"Pontuacao: {self.score_data['score']}", ACCENT),
                (f"Acertos: {self.score_data['correct']}", GREEN),
                (f"Erros: {self.score_data['wrong']}", RED),
                (f"Questoes: {self.score_data['correct'] + self.score_data['wrong']}", WHITE),
            ]
            for text, color in stats:
                cv2.putText(img, text, (stats_x, stats_y), FONT, 0.9, color, 2)
                stats_y += line_h

        # Buttons
        bw, bh, spacing = 280, 80, 40
        total = 2 * bw + spacing
        bx = fx + (fw - total) // 2
        by = fy + fh - bh - 40

        if self.play_btn is None:
            self.play_btn = Button(bx, by, bw, bh, "Jogar Novamente",
                                   color=DARK_GRAY, hover_color=GREEN,
                                   text_color=WHITE, border_color=ACCENT,
                                   font_scale=0.8)
            self.exit_btn = Button(bx + bw + spacing, by, bw, bh, "Sair",
                                   color=DARK_GRAY, hover_color=RED,
                                   text_color=WHITE, border_color=ACCENT,
                                   font_scale=0.8)

        cursors = get_cursors(hands)
        self.play_btn.update_hover(cursors)
        self.exit_btn.update_hover(cursors)
        self.play_btn.draw(img)
        self.exit_btn.draw(img)

        # Delay before allowing clicks
        active = time.time() - self.start_time >= GAME_OVER_DELAY
        if not active:
            remaining = GAME_OVER_DELAY - (time.time() - self.start_time)
            cv2.putText(img, f"Aguarde {remaining:.0f}s...",
                        (fx + fw // 2 - 80, by - 15), FONT, 0.6, GRAY, 1)
            return None

        pinches = get_pinches(hands)
        if not pinches:
            return None

        if self.play_btn.check_click(pinches):
            return "play_again"
        if self.exit_btn.check_click(pinches):
            return "exit"
        return None
