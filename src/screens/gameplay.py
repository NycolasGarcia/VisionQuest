import os
import math
import time
import cv2
import pygame

from ..config import (
    SOUNDS_DIR, FONT, FONT_TITLE, BLACK, WHITE, GREEN, RED, GRAY, DARK_GRAY,
    GOLD, ACCENT, ORANGE, IMAGES_DIR,
    PLANE_CENTER, PLANE_WIDTH, PLANE_HEIGHT, PLANE_STEP, POINT_TOLERANCE,
    PROGRESS_BAR_WIDTH, PROGRESS_BAR_HEIGHT,
    FEEDBACK_DURATION, MAX_SCORE, MAX_LIVES, WINDOW_WIDTH,
)
from ..button import Button
from ..cartesian_plane import draw_cartesian_plane
from ..question_generator import generate_question
from ..score_system import ScoreSystem
from ..hand_tracker import get_cursors, get_pinches
from .hint import HintOverlay


class GameplayScreen:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.score = ScoreSystem()
        self.question = generate_question(difficulty)
        self.hint_overlay = HintOverlay()

        # Feedback state
        self.feedback_text = ""
        self.feedback_color = GREEN
        self.feedback_time = 0
        self.need_new_question = False
        self.show_correct_answer = ""
        self.bonus_text = ""
        self.bonus_time = 0

        # Hint button
        hint_img = cv2.imread(os.path.join(IMAGES_DIR, "lampada.png"), cv2.IMREAD_UNCHANGED)
        if hint_img is not None:
            hint_img = cv2.resize(hint_img, (50, 50))
        self.hint_btn = Button(20, 640, 60, 60, image=hint_img)
        self.showing_hint = False

        # Option buttons (persisted across frames)
        self._option_buttons = []
        self._build_option_buttons()

        # Audio
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        self.win_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "win.mp3"))
        self.loss_sound = pygame.mixer.Sound(os.path.join(SOUNDS_DIR, "loss.mp3"))

    def _build_option_buttons(self):
        """Create option buttons for the current question."""
        self._option_buttons = []
        q = self.question
        if q["type"] != "multiple_choice":
            return
        opts = q["options"]
        count = len(opts)
        btn_w, btn_h = 220, 90
        spacing = 40
        total = count * btn_w + (count - 1) * spacing
        start_x = (WINDOW_WIDTH - total) // 2
        for i, opt in enumerate(opts):
            x = start_x + i * (btn_w + spacing)
            self._option_buttons.append(
                Button(x, 420, btn_w, btn_h, opt,
                       color=DARK_GRAY, hover_color=ACCENT,
                       text_color=WHITE, border_color=ACCENT,
                       font_scale=1.2)
            )

    def update(self, img, hands):
        """Draw and process. Returns 'game_over' or None."""
        if self.score.is_game_over:
            return "game_over"

        if self.showing_hint:
            return self._update_hint(img, hands)

        h, w = img.shape[:2]

        # Darken camera feed slightly for readability
        overlay = img.copy()
        cv2.rectangle(overlay, (0, 0), (w, h), (20, 20, 20), -1)
        cv2.addWeighted(overlay, 0.3, img, 0.7, 0, img)

        self._draw_hud(img)
        self._draw_question(img)
        self._draw_hint_button(img)
        self._draw_feedback(img)
        self._tick_feedback()

        cursors = get_cursors(hands)
        pinches = get_pinches(hands)

        # Update hover on all interactive buttons
        for btn in self._option_buttons:
            btn.update_hover(cursors)

        if self.feedback_text or not pinches:
            return None

        # Check hint button
        if self.hint_btn.check_click(pinches):
            self.showing_hint = True
            return None

        # Check answer
        px, py = pinches[0]
        self._check_answer(px, py)
        return None

    def _update_hint(self, img, hands):
        closed = self.hint_overlay.draw(img, self.question["hint"], hands)
        if closed:
            self.showing_hint = False
        return None

    # --- HUD ---

    def _draw_hud(self, img):
        h, w = img.shape[:2]

        # Top bar background
        cv2.rectangle(img, (0, 0), (w, 80), (30, 25, 20), cv2.FILLED)
        cv2.line(img, (0, 80), (w, 80), ACCENT, 2)

        # Score
        score_text = f"Pontos: {self.score.score}/{MAX_SCORE}"
        cv2.putText(img, score_text, (20, 50), FONT, 0.9, ACCENT, 2)

        # Streak
        if self.score.streak > 0:
            streak_text = f"Sequencia: {self.score.streak}"
            cv2.putText(img, streak_text, (280, 50), FONT, 0.7, GOLD, 2)

        # Lives (hearts)
        heart_x = w - 160
        for i in range(MAX_LIVES):
            cx = heart_x + i * 45
            cy = 40
            if i < self.score.lives:
                # Filled heart
                cv2.circle(img, (cx - 7, cy - 3), 10, RED, cv2.FILLED)
                cv2.circle(img, (cx + 7, cy - 3), 10, RED, cv2.FILLED)
                pts = [(cx - 17, cy), (cx, cy + 18), (cx + 17, cy)]
                cv2.fillPoly(img, [self._heart_points(cx, cy)], RED)
            else:
                # Empty heart
                cv2.circle(img, (cx - 7, cy - 3), 10, GRAY, 2)
                cv2.circle(img, (cx + 7, cy - 3), 10, GRAY, 2)

        # Progress bar
        bar_x = w // 2 - PROGRESS_BAR_WIDTH // 2
        bar_y = 25
        bar_w = int(PROGRESS_BAR_WIDTH * self.score.progress)
        cv2.rectangle(img, (bar_x, bar_y),
                      (bar_x + PROGRESS_BAR_WIDTH, bar_y + PROGRESS_BAR_HEIGHT),
                      DARK_GRAY, cv2.FILLED)
        if bar_w > 0:
            cv2.rectangle(img, (bar_x, bar_y),
                          (bar_x + bar_w, bar_y + PROGRESS_BAR_HEIGHT),
                          GREEN, cv2.FILLED)
        cv2.rectangle(img, (bar_x, bar_y),
                      (bar_x + PROGRESS_BAR_WIDTH, bar_y + PROGRESS_BAR_HEIGHT),
                      WHITE, 1)

        # Question counter in progress bar
        q_text = f"{self.score.score}/{MAX_SCORE}"
        ts = cv2.getTextSize(q_text, FONT, 0.6, 2)[0]
        tx = bar_x + (PROGRESS_BAR_WIDTH - ts[0]) // 2
        cv2.putText(img, q_text, (tx, bar_y + 23), FONT, 0.6, WHITE, 2)

        # Difficulty label
        diff_text = f"[{self.difficulty}]"
        cv2.putText(img, diff_text, (bar_x + PROGRESS_BAR_WIDTH + 15, bar_y + 23),
                    FONT, 0.6, GRAY, 1)

    def _heart_points(self, cx, cy):
        """Generate heart polygon points."""
        import numpy as np
        return np.array([
            [cx - 17, cy - 2],
            [cx - 10, cy + 10],
            [cx, cy + 18],
            [cx + 10, cy + 10],
            [cx + 17, cy - 2],
        ], dtype=np.int32)

    # --- Question rendering ---

    def _draw_question(self, img):
        q = self.question
        if q["type"] == "multiple_choice":
            self._draw_mc(img, q)
        elif q["type"] == "cartesian_plane":
            self._draw_cartesian(img, q)

    def _draw_mc(self, img, q):
        h, w = img.shape[:2]

        # Question box
        qbox_y = 120
        qbox_h = 130
        cv2.rectangle(img, (60, qbox_y), (w - 60, qbox_y + qbox_h), DARK_GRAY, cv2.FILLED)
        cv2.rectangle(img, (60, qbox_y), (w - 60, qbox_y + qbox_h), ACCENT, 2)

        # Question text (auto-scale)
        scale = 1.8
        text = q["question"]
        ts = cv2.getTextSize(text, FONT, scale, 2)[0]
        while ts[0] > w - 160 and scale > 0.5:
            scale -= 0.1
            ts = cv2.getTextSize(text, FONT, scale, 2)[0]
        tx = (w - ts[0]) // 2
        ty = qbox_y + qbox_h // 2 + ts[1] // 2
        cv2.putText(img, text, (tx, ty), FONT, scale, WHITE, 2)

        # Option buttons
        for btn in self._option_buttons:
            btn.draw(img)

    def _draw_cartesian(self, img, q):
        draw_cartesian_plane(img, PLANE_CENTER, PLANE_WIDTH, PLANE_HEIGHT)

        # Question in a box at top
        text = q["question"]
        ts = cv2.getTextSize(text, FONT, 1.0, 2)[0]
        tx = (img.shape[1] - ts[0]) // 2
        cv2.rectangle(img, (tx - 15, 85), (tx + ts[0] + 15, 125), DARK_GRAY, cv2.FILLED)
        cv2.rectangle(img, (tx - 15, 85), (tx + ts[0] + 15, 125), ACCENT, 1)
        cv2.putText(img, text, (tx, 115), FONT, 1.0, WHITE, 2)

    # --- Hint button ---

    def _draw_hint_button(self, img):
        # Draw hint button with border
        self.hint_btn.draw(img)
        cv2.rectangle(img, (18, 638), (82, 702), ACCENT, 2)
        cv2.putText(img, "Dica", (25, 720), FONT, 0.5, ACCENT, 1)

    # --- Answer checking ---

    def _check_answer(self, px, py):
        q = self.question
        if q["type"] == "multiple_choice":
            for btn in self._option_buttons:
                if btn.contains(px, py):
                    if btn.text == q["correct_answer"]:
                        self._correct()
                    else:
                        self._incorrect(q["correct_answer"])
                    break
        elif q["type"] == "cartesian_plane":
            tx, ty = q["target_point"]
            sx = PLANE_CENTER[0] + tx * PLANE_STEP
            sy = PLANE_CENTER[1] - ty * PLANE_STEP
            if math.hypot(px - sx, py - sy) < POINT_TOLERANCE:
                self._correct()

    def _correct(self):
        self.feedback_text = "Correto!"
        self.feedback_color = GREEN
        self.feedback_time = time.time()
        self.show_correct_answer = ""
        self.win_sound.play()
        bonus = self.score.correct_answer()
        if bonus:
            self.bonus_text = f"Bonus +1! (sequencia de {self.score.streak})"
            self.bonus_time = time.time()
        self.need_new_question = True

    def _incorrect(self, correct_answer):
        self.feedback_text = "Errado!"
        self.feedback_color = RED
        self.feedback_time = time.time()
        self.show_correct_answer = f"Resposta correta: {correct_answer}"
        self.loss_sound.play()
        self.score.incorrect_answer()
        self.need_new_question = True

    # --- Feedback ---

    def _draw_feedback(self, img):
        h, w = img.shape[:2]

        if self.feedback_text:
            # Centered feedback banner
            ts = cv2.getTextSize(self.feedback_text, FONT, 1.8, 3)[0]
            tx = (w - ts[0]) // 2
            ty = 600

            # Background
            cv2.rectangle(img, (tx - 20, ty - 50), (tx + ts[0] + 20, ty + 15),
                          (0, 0, 0), cv2.FILLED)
            cv2.putText(img, self.feedback_text, (tx, ty), FONT, 1.8,
                        self.feedback_color, 3)

            # Show correct answer below when wrong
            if self.show_correct_answer:
                ats = cv2.getTextSize(self.show_correct_answer, FONT, 0.9, 2)[0]
                atx = (w - ats[0]) // 2
                cv2.rectangle(img, (atx - 10, ty + 10), (atx + ats[0] + 10, ty + 45),
                              (0, 0, 0), cv2.FILLED)
                cv2.putText(img, self.show_correct_answer, (atx, ty + 38),
                            FONT, 0.9, ACCENT, 2)

        if self.bonus_text:
            bts = cv2.getTextSize(self.bonus_text, FONT, 0.9, 2)[0]
            bx = (w - bts[0]) // 2
            cv2.putText(img, self.bonus_text, (bx, 560), FONT, 0.9, GOLD, 2)

    def _tick_feedback(self):
        now = time.time()
        if self.feedback_text and now - self.feedback_time > FEEDBACK_DURATION:
            self.feedback_text = ""
            self.show_correct_answer = ""
            if self.need_new_question:
                self.question = generate_question(self.difficulty)
                self._build_option_buttons()
                self.need_new_question = False
        if self.bonus_text and now - self.bonus_time > FEEDBACK_DURATION:
            self.bonus_text = ""
