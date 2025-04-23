import image_processing as ip
import sys
import cv2 as cv

def main():
    img = cv.imread("../qr_real_world.png", cv.IMREAD_GRAYSCALE)

    if img is None:
        sys.exit("Could not read the image.")

    binary = img.copy()
    _, binary = cv.threshold(img, 127, 255, cv.THRESH_BINARY)

    finders = ip.getFinders(binary)

if __name__ == "__main__":
    main()
