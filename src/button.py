import time
import cv2
import webbrowser

from .config import (
    FONT, BLACK, WHITE, ACCENT, GRAY, DARK_GRAY, GREEN,
    DWELL_TIME,
)


class Button:
    """Interactive button with hover highlight and dwell-click confirmation."""

    def __init__(self, x, y, width, height, text="", image=None, link=None,
                 color=WHITE, hover_color=ACCENT, text_color=BLACK,
                 border_color=BLACK, font_scale=1.0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.image = image
        self.link = link
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.border_color = border_color
        self.font_scale = font_scale

        # Dwell state
        self._hover_start = 0
        self._hovering = False
        self._dwell_progress = 0.0  # 0.0 to 1.0

    def draw(self, img):
        if self.image is not None:
            self._draw_image(img)
        else:
            self._draw_button(img)

    def _draw_image(self, img):
        resized = cv2.resize(self.image, (self.width, self.height))
        y1, y2 = self.y, self.y + self.height
        x1, x2 = self.x, self.x + self.width
        if resized.shape[2] == 4:
            alpha = resized[:, :, 3] / 255.0
            inv = 1.0 - alpha
            for c in range(3):
                img[y1:y2, x1:x2, c] = (
                    alpha * resized[:, :, c] + inv * img[y1:y2, x1:x2, c]
                )
        else:
            img[y1:y2, x1:x2] = resized

    def _draw_button(self, img):
        x1, y1 = self.x, self.y
        x2, y2 = self.x + self.width, self.y + self.height

        # Background color (changes on hover)
        bg = self.hover_color if self._hovering else self.color
        cv2.rectangle(img, (x1, y1), (x2, y2), bg, cv2.FILLED)
        cv2.rectangle(img, (x1, y1), (x2, y2), self.border_color, 2)

        # Dwell progress bar at bottom of button
        if self._hovering and self._dwell_progress > 0:
            bar_w = int(self.width * self._dwell_progress)
            cv2.rectangle(img, (x1, y2 - 6), (x1 + bar_w, y2), GREEN, cv2.FILLED)

        # Text
        if self.text:
            ts = cv2.getTextSize(self.text, FONT, self.font_scale, 2)[0]
            tx = x1 + (self.width - ts[0]) // 2
            ty = y1 + (self.height + ts[1]) // 2
            cv2.putText(img, self.text, (tx, ty), FONT, self.font_scale,
                        self.text_color, 2)

    def contains(self, px, py):
        return (self.x <= px <= self.x + self.width
                and self.y <= py <= self.y + self.height)

    def update_hover(self, cursors):
        """Update hover/dwell state based on cursor positions. Call every frame."""
        hovering_now = any(self.contains(cx, cy) for cx, cy in cursors)

        if hovering_now and not self._hovering:
            # Just started hovering
            self._hover_start = time.time()
            self._hovering = True
        elif not hovering_now:
            self._hovering = False
            self._hover_start = 0
            self._dwell_progress = 0.0

        if self._hovering:
            elapsed = time.time() - self._hover_start
            self._dwell_progress = min(elapsed / DWELL_TIME, 1.0)

    def check_dwell_click(self):
        """Returns True if dwell time completed (user held over button long enough)."""
        if self._hovering and self._dwell_progress >= 1.0:
            self._dwell_progress = 0.0
            self._hover_start = time.time() + 0.5  # cooldown
            if self.link:
                webbrowser.open(self.link)
            return True
        return False

    def check_click(self, pinches):
        """Legacy instant click check (for pinch gesture)."""
        for px, py in pinches:
            if self.contains(px, py):
                if self.link:
                    webbrowser.open(self.link)
                return True
        return False
