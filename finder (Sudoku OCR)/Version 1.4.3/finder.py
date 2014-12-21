"""Finds sudoku puzzles in images."""
import time
import cv2
import numpy as np
import sys
import OCR

#debug info 
DEBUG_MODE = False
if DEBUG_MODE:
    import os
    DEBUG_FOLDER = "debug/"
    if not os.path.exists(DEBUG_FOLDER):
        os.mkdir(DEBUG_FOLDER)

TIMER_START = time.time()

IMAGE_FILE = sys.argv[1]
print "[+]Using file: " + IMAGE_FILE

###Image PreProcessing
print "[1]Image preprocessing"
IMG = cv2.imread(IMAGE_FILE)
IMG = cv2.GaussianBlur(IMG, (5, 5), 0)
GRAY = cv2.cvtColor(IMG, cv2.COLOR_BGR2GRAY)
MASK = np.zeros((GRAY.shape), np.uint8)

MASK_HOR = np.zeros((GRAY.shape), np.uint8)
MASK_VER = np.zeros((GRAY.shape), np.uint8)

KERNEL1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))

CLOSE = cv2.morphologyEx(GRAY, cv2.MORPH_CLOSE, KERNEL1)
DIV = np.float32(GRAY)/(CLOSE)
RES = np.uint8(cv2.normalize(DIV, DIV, 0, 255, cv2.NORM_MINMAX))
RES2 = cv2.adaptiveThreshold(RES, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 0, 151, 70)

###Finding Sudoku Square and Creating MASK Image
print "[2]Finding Square"
THRESH = cv2.adaptiveThreshold(RES, 255, 0, 1, 19, 2)

if DEBUG_MODE:
    cv2.imwrite(DEBUG_FOLDER + "THRESH.jpg", THRESH)

CONTOUR, HIER = cv2.findContours(THRESH, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

MAX_AREA = 0
for CNT in CONTOUR:
    AREA = cv2.contourArea(CNT)
    if AREA > 1000 and AREA > MAX_AREA:
        MAX_AREA = AREA
        BEST_CNT = CNT

cv2.drawContours(MASK, [BEST_CNT], 0, 255, -1)
cv2.drawContours(MASK, [BEST_CNT], 0, 0, 2)

RES = cv2.bitwise_and(RES, MASK)
if DEBUG_MODE:
    cv2.imwrite(DEBUG_FOLDER+"puzzle.jpg", RES)

###Finding Vertical lines
print "[3]Finding V lines"
KERNELX = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 10))

DX = cv2.Sobel(RES, cv2.CV_64F, 1, 0)

DX = cv2.convertScaleAbs(DX)

cv2.normalize(DX, DX, 0, 255, cv2.NORM_MINMAX)

RET, CLOSEX = cv2.threshold(DX, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

CLOSEX = cv2.morphologyEx(CLOSEX, cv2.MORPH_DILATE, KERNELX)

CONTOUR, HIER = cv2.findContours(CLOSEX, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for CNT in CONTOUR:
    x, y, w, h = cv2.boundingRect(CNT)
    if h/w > 5:
        cv2.drawContours(CLOSEX, [CNT], 0, 255, -1)
    else:
        cv2.drawContours(CLOSEX, [CNT], 0, 0, -1)

CLOSEX = cv2.morphologyEx(CLOSEX, cv2.MORPH_DILATE, None, iterations = 2)

if DEBUG_MODE:
    cv2.imwrite(DEBUG_FOLDER + "vlines.jpg", CLOSEX)

###Finding Horizontal Lines
print("[4]Finding H Lines")
KERNELY = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 2))

DY = cv2.Sobel(RES, cv2.CV_64F, 0, 1)
DY = cv2.convertScaleAbs(DY)
cv2.normalize(DY, DY, 0, 255, cv2.NORM_MINMAX)
RET, CLOSEY = cv2.threshold(DY, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

CLOSEY = cv2.morphologyEx(CLOSEY, cv2.MORPH_DILATE, KERNELY)

CONTOUR, HIER = cv2.findContours(CLOSEY, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
for CNT in CONTOUR:
    x, y, w, h = cv2.boundingRect(CNT)
    if w/h > 5:
        cv2.drawContours(CLOSEY, [CNT], 0, 255, -1)
    else:
        cv2.drawContours(CLOSEY, [CNT], 0, 0, -1)

CLOSEY = cv2.morphologyEx(CLOSEY, cv2.MORPH_DILATE, None, iterations = 2)

if DEBUG_MODE:
    cv2.imwrite(DEBUG_FOLDER + "hlines.jpg", CLOSEY)

###Finding Grid POINTS
print("[5]Finding POINTS")
RES = cv2.bitwise_and(CLOSEX, CLOSEY)

if DEBUG_MODE:
    cv2.imwrite(DEBUG_FOLDER + "POINTS.jpg", RES)

###Correcting the defects
print("[6]Correcting defects")
CONTOUR, HIER = cv2.findContours(RES, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

POINTS = []
for CNT in CONTOUR:
    mom = cv2.moments(CNT)
    (x, y) = int(mom['m10']/mom['m00']), int(mom['m01']/mom['m00'])
    cv2.circle(IMG, (x, y), 4, (0, 255, 0), -1)
    POINTS.append((x, y))

if len(POINTS) != 100:
    print "[!]Centroids: " + str(len(POINTS))
    print "[!]Exiting"
    sys.exit()
    
C_POINTS = [sorted(i, key = lambda x: x[1]) for i in OCR.split_len(sorted(POINTS), 10)]

R_POINTS = [ list(i) for i in zip(*C_POINTS)]
R_POINTS = [x for sublist in R_POINTS for x in sublist]

###OCR Stage
print "[7]OCR Stage: "
RESULT = [[0]*9 for i in range(9)]


for row in range(9):
    print "\t[+]Row: " + str(row + 1)
    for column in range(9):

    ## top left corner = x1:y1 | down right corner = x2:y2
        x1, x2, y1, y2 = OCR.getcorners((row, column), R_POINTS)
        
        crop = RES2[y1 + 7 : y2 - 7 , x1 + 7: x2 - 7]
        
        digit = cv2.cv.CreateImageHeader((crop.shape[1], crop.shape[0]), cv2.cv.IPL_DEPTH_8U, 1)
        cv2.cv.SetData(digit, crop.tostring(), crop.dtype.itemsize*crop.shape[1])
        
        if DEBUG_MODE:
            print row, column
            cv2.imwrite(DEBUG_FOLDER + str(row) + str(column)+".jpg", crop)
    
        ##recognize the digit
        RESULT[column][row] = OCR.ocr_singledigit(digit)

        
##print out the sudoku puzzle
print
print "[+]Solution:"
for row in RESULT:
    string = ""
    for digit in row:
        string += str(digit) + " "
    print string

print 
print "Total time: " + str(round(time.time() - TIMER_START, 2)) + " seconds"
