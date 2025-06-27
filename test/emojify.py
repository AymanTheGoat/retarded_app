## this is a script to take an image and covert it to emoji art.
import math
import cv2 as cv
import numpy as np
from typing import List, Tuple

SECTIONS = 6

emojiDict = {
    (232,18,36): "🟥",
    (247,99,12): "🟧",
    (255,241,0): "🟨",
    (22,198,12): "🟩",
    (0,120,215): "🟦",
    (136,108,228): "🟪",
    (142,86,46): "🟫",
    (56,56,56,): "⬛",
    (242,242,242): "⬜"
}


def getImage(emoji_name, colorspaceRGB = True) -> cv.typing.MatLike:   
    image_path = f"assets/{emoji_name}"
    img = cv.GaussianBlur(cv.imread(image_path), (9, 9), 0)
    if colorspaceRGB:
        img = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    return img


def validateImage(img):
    if img is None:
        raise ValueError("Image not found or unable to load.")
    if img.shape[0] == 0 or img.shape[1] == 0:
        raise ValueError("Image has no content.")
    if not img.shape[0] / img.shape[1] == 1:
        raise ValueError("Image is not square.")


def splitImage(img):
    sections = SECTIONS
    rows, cols, _ = img.shape

    x = int(rows / sections)
    y = int(cols / sections)

    tileSize = math.ceil(rows / sections)

    tiles = []
    for y in range(0, cols, tileSize):
        tileRows = []
        for x in range(0, rows, tileSize):
            tile = img[y:y+tileSize, x:x+tileSize]
            tileRows.append(tile)
        tiles.append(tileRows)

    return tiles


def getAverages(tiles:list[list[cv.typing.MatLike]]) -> list[list[tuple[int]]]:
    averages = []
    for row in tiles:
        rowAverages = []
        for tile in row:
            avg = tile.mean(axis=(0, 1)).astype(int)
            rowAverages.append(avg)
        averages.append(rowAverages)
    return averages


def getDominants(tiles: List[List[cv.typing.MatLike]]):
    dominants = []

    for row in tiles:
        row_dominants: List[Tuple[int, int, int]] = []
        for tile in row:
            data = tile.reshape((-1, 3)).astype(np.float32)

            dummy_labels = np.zeros((data.shape[0], 1), dtype=np.int32)

            criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
            flags = cv.KMEANS_RANDOM_CENTERS
            _, _, centers = cv.kmeans(data, 1, dummy_labels, criteria, 10, flags)

            dominant_color:tuple = tuple(map(int, centers[0]))
            row_dominants.append(dominant_color)

        dominants.append(row_dominants)

    return dominants


def getDistanceEuclydian(color1:tuple[int], color2:tuple[int]):
    r1, g1, b1 = color1 # type: ignore
    r2, g2, b2 = color2 # type: ignore

    distance = math.sqrt((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2)

    return distance


def getDistanceManhattan(color1, color2):
    r_diff = abs(color1[0] - color2[0])
    g_diff = abs(color1[1] - color2[1])
    b_diff = abs(color1[2] - color2[2])

    return r_diff + g_diff + b_diff


def getClosestEmoji(color:tuple[int], algorithm) -> str:
    closest_emoji = None
    min_distance = float('inf')

    for emoji_color, emoji in emojiDict.items():
        distance = algorithm(color, emoji_color) # type: ignore
        if distance < min_distance:
            min_distance = distance
            closest_emoji = emoji

    return closest_emoji # type: ignore


def createEmojiArt(averages:list[list[tuple[int]]], algorithm=getDistanceEuclydian) -> str:
    emoji_art = ""

    for row in averages:
        for color in row:
            emoji = getClosestEmoji(color, algorithm)
            # print(f"Color: {color}, Emoji: {emoji}")
            emoji_art += emoji
        emoji_art += "\n"

    return emoji_art


if __name__ == "__main__":
    imgname = r"swastika.png"
    img = getImage(imgname)
    validateImage(img)
    img = splitImage(img)
    averages = getAverages(img)
    emoji_art = createEmojiArt(averages, getDistanceEuclydian)
    print("Processing complete. Tiles saved, (Kmeans + euclydian distance).\n{}".format(emoji_art))