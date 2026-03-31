import cv2

from ..config import FONT, BLACK, WHITE, GRAY, DARK_GRAY, ACCENT
from ..button import Button
from ..hand_tracker import get_cursors, get_pinches


class HintOverlay:
    def __init__(self):
        self.close_btn = None

    def draw(self, img, hint_text, hands):
        """Draw hint overlay with 50% opacity so hand stays visible.
        Returns True if user clicked close."""
        h, w = img.shape[:2]

        # Semi-transparent background (50% instead of 80%)
        overlay = img.copy()
        cv2.rectangle(overlay, (0, 0), (w, h), (30, 30, 30), -1)
        cv2.addWeighted(overlay, 0.5, img, 0.5, 0, img)

        # Frame
        fx, fy = 150, 120
        fw, fh = w - 300, h - 240
        cv2.rectangle(img, (fx, fy), (fx + fw, fy + fh), DARK_GRAY, cv2.FILLED)
        cv2.rectangle(img, (fx, fy), (fx + fw, fy + fh), ACCENT, 2)

        # Title
        cv2.putText(img, "DICA", (fx + fw // 2 - 50, fy + 50),
                    FONT, 1.5, ACCENT, 3)

        # Hint text (auto-scale)
        scale = 1.0
        max_w = fw - 60
        ts = cv2.getTextSize(hint_text, FONT, scale, 2)[0]
        while ts[0] > max_w and scale > 0.4:
            scale -= 0.1
            ts = cv2.getTextSize(hint_text, FONT, scale, 2)[0]
        tx = fx + (fw - ts[0]) // 2
        ty = fy + fh // 2
        cv2.putText(img, hint_text, (tx, ty), FONT, scale, WHITE, 2)

        # Close button
        bw, bh = 200, 70
        bx = fx + (fw - bw) // 2
        by = fy + fh - bh - 30
        if self.close_btn is None:
            self.close_btn = Button(bx, by, bw, bh, "Fechar",
                                    color=DARK_GRAY, hover_color=ACCENT,
                                    text_color=WHITE, border_color=ACCENT)
        else:
            self.close_btn.x = bx
            self.close_btn.y = by

        # Update hover and draw
        cursors = get_cursors(hands)
        self.close_btn.update_hover(cursors)
        self.close_btn.draw(img)

        # Check click
        pinches = get_pinches(hands)
        if self.close_btn.check_click(pinches):
            self.close_btn = None
            return True

        return False
