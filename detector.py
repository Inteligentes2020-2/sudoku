import cv2
import numpy as np
import pytesseract as pytesseract


def get(file_path):
    grid = np.zeros((9, 9), dtype=int)
    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    img = cv2.imread(file_path)
    starty = 385
    endy = 1170
    startx = 365
    endx = 1155
    stepy = round((endy - starty) / 9)
    stepx = round((endx - startx) / 9)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Applying Gaussian Blur to smooth out the noise
    gray = cv2.GaussianBlur(gray, (11, 11), 0)
    #cv2.imwrite("StagesImages/1.jpg", gray)

    # Applying thresholding using adaptive Gaussian|Mean thresholding
    gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C | cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                 cv2.THRESH_BINARY, 5, 2)
    #cv2.imwrite("StagesImages/2.jpg", gray)

    # Dilating the image to fill up the "cracks" in lines
    kernel = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], np.uint8)
    gray = cv2.dilate(gray, kernel)
    img = gray
    #cv2.imwrite("StagesImages/3.jpg", gray)

    for i in range(0, 9):
        for j in range(0, 9):
            x1 = startx + (stepx * j)
            x2 = startx + stepx * (j + 1)
            y1 = starty + (stepy * i)
            y2 = starty + stepy * (i + 1)
            casilla = img[y1 + 10:y2 - 10, x1 + 10:x2 - 17]

            # Apply OCR on the cropped image
            text = pytesseract.image_to_string(casilla, config='--psm 6')

            try:
                grid[i, j] = int(float(text))
            except:
                pass

            #cv2.imwrite('Casillas/casilla(' + str(i) + ',' + str(j) + ').png', casilla)
    return grid
