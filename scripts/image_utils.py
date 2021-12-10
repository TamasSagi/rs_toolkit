import cv2

import numpy as np

from dataclasses import dataclass
from PIL import Image


@dataclass
class ImageWithRegion:

    img: np.array
    region: list


def template_match(img, template, precision=0.97):
    res = cv2.matchTemplate(img, template, cv2.TM_CCORR_NORMED)
    return np.where(res >= precision)


def draw_template_match_results(img, template, match_locations):
    print(len(match_locations))
    h, w, c = template.shape
    drawn_image = cv2.UMat(img).get()  # TODO: draw on screen
    for (x, y) in zip(match_locations[1], match_locations[0]):
        cv2.rectangle(drawn_image, (int(x), int(y)), (int(x + w), int(y + h)), (0, 255, 0), 1)


def get_mouse_action_region(full_screen_img):
    pass


def get_img_region(img, region: list, offset: list = [0, 23], debug: bool = True) -> ImageWithRegion:
    # Calculate x, y coordinates and index from top left corner
    # +1 is to exclude the border drawn by the mouse.
    x = sorted([region[0] + 1, region[0] + region[2]])
    y = sorted([region[1] - offset[1] + 1, region[1] - offset[1] + region[3]])

    cropped_img = img[y[0] : y[1], x[0] : x[1]]

    if debug:
        Image.fromarray(cropped_img).save("get_img_region_result.png")

    return ImageWithRegion(cropped_img, region)
