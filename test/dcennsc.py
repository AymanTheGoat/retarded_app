import cv2 as cv
import numpy as np
from collections import Counter
from typing import List, Tuple


def extractDominantColors(
    imgPath:str,
    maxWidth:int = 600,
    n:int = 5,
    q:int = 20,
    orientation:int = 0, # 0 for horizontal, 1 for vertical, -1 for auto
) -> tuple[bool, np.ndarray]:
    img = cv.imread(imgPath)
    h, w = img.shape[:2]

    if w > maxWidth:
        scale = maxWidth / w
        newWidth = int(w * scale)
        newHeight = int(h * scale)

        resized = cv.resize(img, (newWidth, newHeight), interpolation=cv.INTER_AREA)
        img = resized

    data = img.reshape((-1, 3))
    colorTuples = [tuple(color) for color in data]

    uniqueColors = set(colorTuples)
    print("Unique Colors:", len(uniqueColors))

    if len(uniqueColors) <= 300:
        print("Using Most Frequent Colors")
        colorCounter = Counter(colorTuples)
        mostFrquents = colorCounter.most_common(n)
        dominantsUnquantized = [color for color, _ in mostFrquents]
        dominants = [tuple((channel // q) * q for channel in color) for color in dominantsUnquantized]
        dominants = list(set(dominants))
        print("Dominants:", len(dominants))

    else:
        print("Using KMeans")
        data = np.float32(data)
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        k = min(n, len(uniqueColors))

        _, labels, centers = cv.kmeans(data, k, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)  # type: ignore

        dominants = [tuple(map(int, center)) for center in centers]

    def luminance(color):
        # print(color)
        # r, g, b = color[0], color[1], color[2]
        r, g, b = color
        perceivedLuminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
        return perceivedLuminance

    sorted_dominants = sorted(dominants, key=luminance)

    width, height = img.shape[0], img.shape[1]
    c = len(dominants)
    margin = min(width, height) // 20
    # barMargin = int(width/(3*c - 1))
    barMargin = margin

    barH = int(height * 0.2)
    barW = (width - barMargin * (c - 1)) / c
    blankWidth = int(width + margin * 2)
    blankHeight = int(height + barH + barMargin + margin * 2)

    offsetX, offsetY = margin, margin
    endX, endY = offsetX + width, offsetY + height

    if orientation:
        blank = np.zeros((blankHeight, blankWidth, 3), dtype=np.uint8)
    else:
        blank = np.zeros((blankWidth, blankHeight, 3), dtype=np.uint8)

    # background = tuple(255 - channel for channel in sorted_dominants[0])

    # blank[:] = background
    blank[:] = (255, 255, 255)
    blank[offsetX:endX, offsetY:endY] = img
    for i, color in enumerate(dominants):
        # barStartX = int(margin + i * (barMargin + barW))
        # barStartY = int(height + barMargin + margin)
        barStartX = int(margin + i *(barW + margin))
        barStartY = int(2* margin + height)

        endX = int(barStartX + barW)
        endY = int(barStartY + barH)
        if orientation:
            blank[barStartY:endY, barStartX:endX] = color
        else :
            blank[barStartX:endX, barStartY:endY] = color
    finalImage =  blank  # technically its not blank anymore

    cv.imwrite("output.jpg", finalImage)
    cv.imshow("Dominant Colors", finalImage)
    cv.waitKey(0)
    cv.destroyAllWindows()
    jpg = cv.imencode(".jpg", finalImage)
    return jpg


def main():
    analyzed = extractDominantColors("assets/image.png", orientation=1)


if __name__ == "__main__":
    main()
