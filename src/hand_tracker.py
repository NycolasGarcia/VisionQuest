import os
import math
import cv2
import mediapipe as mp
from mediapipe.tasks.python.vision import HandLandmarker, HandLandmarkerOptions, RunningMode
from mediapipe.tasks.python import BaseOptions

from .config import (
    ASSETS_DIR, MAX_HANDS, DETECTION_CONFIDENCE, TRACKING_CONFIDENCE,
    PINCH_THRESHOLD, FINGER_RADIUS, CURSOR_RADIUS,
    YELLOW, CURSOR_COLOR, CURSOR_PINCH_COLOR,
)

MODEL_PATH = os.path.join(ASSETS_DIR, "hand_landmarker.task")

INDEX_TIP = 8
THUMB_TIP = 4

HAND_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),
    (0, 5), (5, 6), (6, 7), (7, 8),
    (0, 9), (9, 10), (10, 11), (11, 12),
    (0, 13), (13, 14), (14, 15), (15, 16),
    (0, 17), (17, 18), (18, 19), (19, 20),
    (5, 9), (9, 13), (13, 17),
]


class HandData:
    """Holds per-hand detection results for one frame."""
    __slots__ = ("index_pos", "thumb_pos", "is_pinching", "landmarks_px")

    def __init__(self, index_pos, thumb_pos, is_pinching, landmarks_px):
        self.index_pos = index_pos      # (x, y) of index fingertip
        self.thumb_pos = thumb_pos      # (x, y) of thumb tip
        self.is_pinching = is_pinching  # bool
        self.landmarks_px = landmarks_px  # list of (x, y) for all 21 landmarks


class HandTracker:
    """Detects hands and returns structured data. Drawing is separate."""

    def __init__(self):
        options = HandLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=MODEL_PATH),
            running_mode=RunningMode.IMAGE,
            num_hands=MAX_HANDS,
            min_hand_detection_confidence=DETECTION_CONFIDENCE,
            min_hand_presence_confidence=DETECTION_CONFIDENCE,
            min_tracking_confidence=TRACKING_CONFIDENCE,
        )
        self.landmarker = HandLandmarker.create_from_options(options)

    def detect(self, img):
        """Detect hands. Returns list of HandData (does NOT draw anything)."""
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
        result = self.landmarker.detect(mp_image)
        hands = []

        if not result.hand_landmarks:
            return hands

        h, w = img.shape[:2]
        for hand_landmarks in result.hand_landmarks:
            landmarks_px = [(int(lm.x * w), int(lm.y * h)) for lm in hand_landmarks]
            ix, iy = landmarks_px[INDEX_TIP]
            tx, ty = landmarks_px[THUMB_TIP]
            pinching = math.hypot(ix - tx, iy - ty) < PINCH_THRESHOLD

            hands.append(HandData(
                index_pos=(ix, iy),
                thumb_pos=(tx, ty),
                is_pinching=pinching,
                landmarks_px=landmarks_px,
            ))

        return hands

    def draw(self, img, hands):
        """Draw hand skeletons and cursors on the image. Call AFTER screen rendering."""
        for hand in hands:
            # Draw skeleton
            for start, end in HAND_CONNECTIONS:
                cv2.line(img, hand.landmarks_px[start], hand.landmarks_px[end], YELLOW, 2)
            for pt in hand.landmarks_px:
                cv2.circle(img, pt, 3, YELLOW, cv2.FILLED)

            # Draw cursor at index fingertip
            color = CURSOR_PINCH_COLOR if hand.is_pinching else CURSOR_COLOR
            cv2.circle(img, hand.index_pos, CURSOR_RADIUS, color, 3)
            cv2.circle(img, hand.index_pos, 4, color, cv2.FILLED)

            # Draw thumb highlight
            cv2.circle(img, hand.thumb_pos, FINGER_RADIUS, YELLOW, cv2.FILLED)

    def release(self):
        self.landmarker.close()


def get_pinches(hands):
    """Extract (x, y) positions from hands that are pinching."""
    return [h.index_pos for h in hands if h.is_pinching]


def get_cursors(hands):
    """Extract all (x, y) cursor positions (index fingertip) regardless of pinch."""
    return [h.index_pos for h in hands]
