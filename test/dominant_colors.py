import cv2 as cv
import numpy as np
from collections import Counter
from typing import List, Tuple





def extractDominantColors(image_path: str, dominant_count: int = 5) -> cv.typing.MatLike:
    img = _load_and_resize_image(image_path)
    dominants = getDominants(img, dominant_count)
    sorted_dominants = sortDominants(dominants)
    final_image = composeFinalImage(img, sorted_dominants)
    _display(final_image)
    cv.imwrite("output.jpg", final_image)
    return final_image
    

def _load_and_resize_image(image_path: str, max_width: int = 800) -> cv.typing.MatLike:
    img = cv.imread(image_path)
    return resize(img, max_width)


def _display(image):
    cv.imshow("Dominant Colors", image)
    cv.waitKey(0)
    cv.destroyAllWindows()


# keeps color quantized to steps
def quantizeColor(color, step=10):
    return tuple((channel // step) * step for channel in color)


# invert the color for better background contrast
def invertColor(color):
    return tuple(255 - channel for channel in color)


# ensures image is resized to a max width
def resize(image, max_width):
    h, w = image.shape[:2]

    if w <= max_width:
        return image

    scale = max_width / w
    new_width = int(w * scale)
    new_height = int(h * scale)

    resized = cv.resize(image, (new_width, new_height), interpolation=cv.INTER_AREA)
    return resized


# calculates dominant colors using frequency or k-means
def getDominants(img: cv.typing.MatLike, n: int = 3, q: int = 30):
    data = img.reshape((-1, 3))
    data_tuples = [tuple(color) for color in data]

    unique_colors = set(data_tuples)
    print("Unique Colors:", len(unique_colors))

    if len(unique_colors) <= 300:
        print("Using Most Frequent Colors")
        color_counts = Counter(data_tuples)
        most_common = color_counts.most_common(n)
        dominants_unquantized = [color for color, _ in most_common]
        dominants = [quantizeColor(color, q) for color in dominants_unquantized]
        dominants = list(set(dominants))
        print("Dominants:", len(dominants))

    else:
        print("Using KMeans")
        data = np.float32(data)
        criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
        k = min(n, len(unique_colors))

        _, labels, centers = cv.kmeans(data, k, None, criteria, 10, cv.KMEANS_RANDOM_CENTERS)  # type: ignore

        dominants = [tuple(map(int, center)) for center in centers]

    return dominants


# sorts colors based on luminance
def sortDominants(dominantsArr):
    def luminance(color):
        # print(color)
        # r, g, b = color[0], color[1], color[2]
        r, g, b = color
        perceivedLuminance = 0.2126 * r + 0.7152 * g + 0.0722 * b
        return perceivedLuminance

    return sorted(dominantsArr, key=luminance)


# creates final image with original image and dominant color bars
def composeFinalImage(img, dominants, vertical=False):
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

    if vertical:
        blank = np.zeros((blankHeight, blankWidth, 3), dtype=np.uint8)
    else:
        blank = np.zeros((blankWidth, blankHeight, 3), dtype=np.uint8)

    background = invertColor(dominants[0])

    blank[:] = background
    blank[offsetX:endX, offsetY:endY] = img
    for i, color in enumerate(dominants):
        # barStartX = int(margin + i * (barMargin + barW))
        # barStartY = int(height + barMargin + margin)
        barStartX = int(margin + i *(barW + margin))
        barStartY = int(2* margin + height)

        endX = int(barStartX + barW)
        endY = int(barStartY + barH)
        if vertical:
            blank[barStartY:endY, barStartX:endX] = color
        else :
            blank[barStartX:endX, barStartY:endY] = color
    return blank  # technically its not blank anymore


def main():
    analyzer = extractDominantColors("assets/image.png", 3)
    cv.imshow("Dominant Colors", analyzer)

if __name__ == "__main__":
    main()
