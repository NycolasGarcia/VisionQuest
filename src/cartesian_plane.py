import cv2

from .config import FONT, BLACK, RED, PLANE_STEP


def draw_cartesian_plane(img, center, width, height, step=PLANE_STEP):
    cx, cy = center
    half_w, half_h = width // 2, height // 2

    # Grid lines
    for x in range(cx - half_w, cx + half_w + 1, step):
        cv2.line(img, (x, cy - half_h), (x, cy + half_h), BLACK, 1)
        if x != cx:
            label = (x - cx) // step
            cv2.putText(img, str(label), (x - 10, cy + 20), FONT, 0.5, BLACK, 1)

    for y in range(cy - half_h, cy + half_h + 1, step):
        cv2.line(img, (cx - half_w, y), (cx + half_w, y), BLACK, 1)
        if y != cy:
            label = (cy - y) // step
            cv2.putText(img, str(label), (cx - 30, y + 5), FONT, 0.5, BLACK, 1)

    # Axes
    cv2.line(img, (cx - half_w, cy), (cx + half_w, cy), RED, 2)
    cv2.line(img, (cx, cy - half_h), (cx, cy + half_h), RED, 2)
