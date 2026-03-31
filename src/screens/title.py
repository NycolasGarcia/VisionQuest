import os
import time
import cv2

from ..config import (
    IMAGES_DIR, COLLABORATORS, FONT_TITLE, FONT,
    BLACK, GOLD, WHITE, ACCENT, DARK_GRAY, GRAY,
    COLLAB_COOLDOWN, CLICK_COOLDOWN, WINDOW_WIDTH,
)
from ..button import Button
from ..hand_tracker import get_cursors, get_pinches


class TitleScreen:
    def __init__(self):
        self._load_collaborators()
        self.last_collab_time = 0

        cx = WINDOW_WIDTH // 2
        self.play_btn = Button(cx - 160, 280, 320, 90, "JOGAR",
                               color=DARK_GRAY, hover_color=ACCENT,
                               text_color=WHITE, border_color=ACCENT,
                               font_scale=1.3)
        self.exit_btn = Button(cx - 120, 400, 240, 70, "Sair",
                               color=DARK_GRAY, hover_color=(0, 0, 180),
                               text_color=GRAY, border_color=GRAY,
                               font_scale=0.9)

    def _load_collaborators(self):
        self.collabs = []
        for data in COLLABORATORS:
            img_path = os.path.join(IMAGES_DIR, data["image"])
            img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
            if img is not None:
                img = cv2.resize(img, (80, 80))
            self.collabs.append({
                "name": data["name"],
                "image": img,
                "link": data["link"],
                "button": None,
            })

    def update(self, img, hands):
        """Draw title screen and process input. Returns 'play', 'exit', or None."""
        h, w = img.shape[:2]

        # Dark overlay on camera feed
        overlay = img.copy()
        cv2.rectangle(overlay, (0, 0), (w, h), (30, 25, 20), -1)
        cv2.addWeighted(overlay, 0.6, img, 0.4, 0, img)

        self._draw_title(img)
        self._draw_instructions(img)

        cursors = get_cursors(hands)
        pinches = get_pinches(hands)

        # Update hover states
        self.play_btn.update_hover(cursors)
        self.exit_btn.update_hover(cursors)

        self.play_btn.draw(img)
        self.exit_btn.draw(img)
        self._draw_collaborators(img)

        # Check collaborator clicks
        now = time.time()
        if now - self.last_collab_time >= COLLAB_COOLDOWN:
            for collab in self.collabs:
                if collab["button"] and collab["button"].check_click(pinches):
                    self.last_collab_time = now
                    break

        # Check main buttons
        if self.play_btn.check_click(pinches):
            return "play"
        if self.exit_btn.check_click(pinches):
            return "exit"

        return None

    def _draw_title(self, img):
        text = "VisionQuest"
        scale = 2.8
        ts = cv2.getTextSize(text, FONT_TITLE, scale, 4)[0]
        x = (img.shape[1] - ts[0]) // 2
        y = 160

        # Shadow
        cv2.putText(img, text, (x + 3, y + 3), FONT_TITLE, scale, (0, 0, 0), 5)
        # Main text
        cv2.putText(img, text, (x, y), FONT_TITLE, scale, GOLD, 4)

        # Subtitle
        sub = "Aprenda Matematica com as Maos"
        sts = cv2.getTextSize(sub, FONT, 0.7, 2)[0]
        sx = (img.shape[1] - sts[0]) // 2
        cv2.putText(img, sub, (sx, y + 45), FONT, 0.7, GRAY, 2)

    def _draw_instructions(self, img):
        text = "Junte o indicador e o polegar para selecionar"
        ts = cv2.getTextSize(text, FONT, 0.55, 1)[0]
        x = (img.shape[1] - ts[0]) // 2
        cv2.putText(img, text, (x, 510), FONT, 0.55, ACCENT, 1)

    def _draw_collaborators(self, img):
        count = len(self.collabs)
        img_size = 80
        spacing = 120
        total_w = count * spacing - (spacing - img_size)
        start_x = (img.shape[1] - total_w) // 2
        y_pos = 570

        for i, collab in enumerate(self.collabs):
            x = start_x + i * spacing

            # Photo
            photo = collab["image"]
            if photo is not None:
                if photo.shape[2] == 4:
                    alpha = photo[:, :, 3] / 255.0
                    inv = 1.0 - alpha
                    for c in range(3):
                        img[y_pos:y_pos + img_size, x:x + img_size, c] = (
                            alpha * photo[:, :, c]
                            + inv * img[y_pos:y_pos + img_size, x:x + img_size, c]
                        )
                else:
                    img[y_pos:y_pos + img_size, x:x + img_size] = photo

                # Border
                cv2.rectangle(img, (x - 2, y_pos - 2),
                              (x + img_size + 2, y_pos + img_size + 2), ACCENT, 1)

            collab["button"] = Button(x, y_pos, img_size, img_size, link=collab["link"])

            # Name
            name = collab["name"]
            ts = cv2.getTextSize(name, FONT, 0.4, 1)[0]
            tx = x + (img_size - ts[0]) // 2
            cv2.putText(img, name, (tx, y_pos + img_size + 18), FONT, 0.4, WHITE, 1)
