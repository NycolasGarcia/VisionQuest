import time
import cv2

from ..config import (
    FONT, FONT_TITLE, BLACK, WHITE, ACCENT, DARK_GRAY, GRAY, GREEN, GOLD, RED,
    DIFFICULTY_DELAY, WINDOW_WIDTH,
)
from ..button import Button
from ..hand_tracker import get_cursors, get_pinches


DIFFICULTIES = [
    {
        "name": "Facil",
        "desc": "Soma e subtracao (1-20)",
        "color": GREEN,
    },
    {
        "name": "Medio",
        "desc": "Multiplicacao, divisao, potencias",
        "color": GOLD,
    },
    {
        "name": "Dificil",
        "desc": "Equacoes, logaritmos, raizes",
        "color": RED,
    },
]

BUTTON_WIDTH = 240
BUTTON_HEIGHT = 90
BUTTON_SPACING = 50


class DifficultyScreen:
    def __init__(self):
        self.activation_time = 0
        self.buttons = []
        self._build_buttons()

    def _build_buttons(self):
        total = len(DIFFICULTIES) * BUTTON_WIDTH + (len(DIFFICULTIES) - 1) * BUTTON_SPACING
        start_x = (WINDOW_WIDTH - total) // 2
        self.buttons = []
        for i, diff in enumerate(DIFFICULTIES):
            x = start_x + i * (BUTTON_WIDTH + BUTTON_SPACING)
            btn = Button(x, 320, BUTTON_WIDTH, BUTTON_HEIGHT, diff["name"],
                         color=DARK_GRAY, hover_color=diff["color"],
                         text_color=WHITE, border_color=diff["color"],
                         font_scale=1.1)
            self.buttons.append((btn, diff))

    def reset(self, timestamp=None):
        self.activation_time = timestamp or time.time()

    def update(self, img, hands):
        """Draw and process. Returns 'difficulty:<name>' or None."""
        h, w = img.shape[:2]

        # Dark overlay
        overlay = img.copy()
        cv2.rectangle(overlay, (0, 0), (w, h), (30, 25, 20), -1)
        cv2.addWeighted(overlay, 0.6, img, 0.4, 0, img)

        self._draw_header(img)

        cursors = get_cursors(hands)
        pinches = get_pinches(hands)

        for btn, diff in self.buttons:
            btn.update_hover(cursors)
            btn.draw(img)
            # Description below each button
            desc = diff["desc"]
            ts = cv2.getTextSize(desc, FONT, 0.5, 1)[0]
            dx = btn.x + (btn.width - ts[0]) // 2
            cv2.putText(img, desc, (dx, btn.y + btn.height + 25),
                        FONT, 0.5, GRAY, 1)

        # Instructions
        inst = "Junte indicador e polegar sobre o nivel desejado"
        ts = cv2.getTextSize(inst, FONT, 0.55, 1)[0]
        ix = (w - ts[0]) // 2
        cv2.putText(img, inst, (ix, 520), FONT, 0.55, ACCENT, 1)

        active = time.time() - self.activation_time >= DIFFICULTY_DELAY
        if not active:
            remaining = DIFFICULTY_DELAY - (time.time() - self.activation_time)
            cv2.putText(img, f"Aguarde {remaining:.0f}s...",
                        (w // 2 - 60, 570), FONT, 0.6, GRAY, 1)
            return None

        if not pinches:
            return None

        for btn, diff in self.buttons:
            if btn.check_click(pinches):
                return f"difficulty:{diff['name']}"

        return None

    def _draw_header(self, img):
        text = "Selecione a Dificuldade"
        scale = 1.8
        ts = cv2.getTextSize(text, FONT_TITLE, scale, 3)[0]
        x = (img.shape[1] - ts[0]) // 2
        y = 200

        cv2.putText(img, text, (x + 2, y + 2), FONT_TITLE, scale, BLACK, 4)
        cv2.putText(img, text, (x, y), FONT_TITLE, scale, ACCENT, 3)
