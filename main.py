import cv2 as cv
import sys
import numpy as np

img = cv.imread("qr_code.png")

if img is None:
    sys.exit("Could not read the image.")

gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
_, thresholded = cv.threshold(gray, 127, 255, 0)

def getFinders(img):
    contours, _ = cv.findContours(thresholded, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    finders = []

    for contour in contours:
        approx = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)

        if len(approx) == 4:
            x, y, w, h = cv.boundingRect(approx)
            aspect_ratio = float(w) / h

            if 0.95 < aspect_ratio < 1.05:
                finders.append((x, y, w, h))
    finders.pop(0) #first contour is an outline of the image

    return finders

finders = getFinders(img)
for (x, y, w, h) in finders:
    print(f"Finder detected at x: {x}, y: {y}, width: {w}, height: {h}")

