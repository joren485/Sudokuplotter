import time
import cv2
import numpy as np
import sys
import OCR

#debug info 
debug_mode = True
if debug_mode:
    import os
    debug_folder = "debug/"
    if not os.path.exists(debug_folder):
	    os.mkdir(debug_folder)

timer_start = time.time()

image_file = sys.argv[1]
print("Using file: " + image_file)

###Image PreProcessing
print "1) Image preprocessing"
img = cv2.imread(image_file)
img = cv2.GaussianBlur(img,(5,5),0)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
mask = np.zeros((gray.shape),np.uint8)
kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11))

close = cv2.morphologyEx(gray,cv2.MORPH_CLOSE,kernel1)
div = np.float32(gray)/(close)
res = np.uint8(cv2.normalize(div,div,0,255,cv2.NORM_MINMAX))
res2 = cv2.adaptiveThreshold(res,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,0,151,80)


###Finding Sudoku Square and Creating Mask Image
print "2) Finding Square"
thresh = cv2.adaptiveThreshold(res,255,0,1,19,2)

if debug_mode:
    cv2.imwrite(debug_folder+"thresh.jpg",thresh)

contour,hier = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

max_area = 0
for cnt in contour:
    area = cv2.contourArea(cnt)
    if area > 1000 and area > max_area:
        max_area = area
        best_cnt = cnt

cv2.drawContours(mask,[best_cnt],0,255,-1)
cv2.drawContours(mask,[best_cnt],0,0,2)

res = cv2.bitwise_and(res,mask)
if debug_mode:
	cv2.imwrite(debug_folder+"puzzle.jpg",res)

###Finding Vertical lines
print "3) Finding V lines" 
kernelx = cv2.getStructuringElement(cv2.MORPH_RECT,(2,10))

dx = cv2.Sobel(res,cv2.CV_64F,1,0)
dx = cv2.convertScaleAbs(dx)
cv2.normalize(dx,dx,0,255,cv2.NORM_MINMAX)
ret,close = cv2.threshold(dx,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

close = cv2.morphologyEx(close,cv2.MORPH_DILATE,kernelx,iterations = 1)

contour, hier = cv2.findContours(close,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
for cnt in contour:
    x,y,w,h = cv2.boundingRect(cnt)
    if h/w > 5:
        cv2.drawContours(close,[cnt],0,255,-1)
    else:
        cv2.drawContours(close,[cnt],0,0,-1)

close = cv2.morphologyEx(close,cv2.MORPH_CLOSE,None,iterations = 2)
closex = close.copy()
if debug_mode:
	cv2.imwrite(debug_folder+"vlines.jpg",closex)

###Finding Horizontal Lines
print "4) Finding H Lines" 
kernely = cv2.getStructuringElement(cv2.MORPH_RECT,(10,2))

dy = cv2.Sobel(res,cv2.CV_64F,0,1)
dy = cv2.convertScaleAbs(dy)
cv2.normalize(dy,dy,0,255,cv2.NORM_MINMAX)
ret,close = cv2.threshold(dy,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

close = cv2.morphologyEx(close,cv2.MORPH_DILATE,kernely)

contour, hier = cv2.findContours(close,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
for cnt in contour:
    x,y,w,h = cv2.boundingRect(cnt)
    if w/h > 5 and w > 100 :
        cv2.drawContours(close,[cnt],0,255,-1)
    else:
        cv2.drawContours(close,[cnt],0,0,-1)

close = cv2.morphologyEx(close,cv2.MORPH_DILATE,None,iterations = 2)
closey = close.copy()
if debug_mode:
	cv2.imwrite(debug_folder+"hlines.jpg",closey)

###Finding Grid Points
print "5) Finding points" 
res = cv2.bitwise_and(closex,closey)

if debug_mode:
    cv2.imwrite(debug_folder+"points.jpg",res)

###Correcting the defects
print "6) Correcting defects"

##finding all the coordinates points
contour, hier = cv2.findContours(res,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

##create a list with the coordinates sorted 
centroids = []
for cnt in contour:
    
    mom = cv2.moments(cnt)
    (x,y) = int(mom['m10']/mom['m00']), int(mom['m01']/mom['m00'])
    centroids.append((x,y))

if len(centroids) != 100:
    print "Centroids: " + str(len(centroids))
    exit()


c_points = [sorted(i, key = lambda x: x[1]) for i in OCR.split_len(sorted(centroids),10)]

r_points = [ list(i) for i in zip(*c_points)]
r_points = [x for sublist in r_points for x in sublist]


###OCR Stage
print "7) OCR Stage: "
result = [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]]


for row in range(9):
    print "\tRow: " + str(row+1)
    for column in range(9):

        ## top left corner = x1:y1 | down right corner = x2:y2
        x1,x2,y1,y2 = OCR.getcorners((row,column),r_points)
        
        crop = res2[y1+5 : y2-5 , x1+5 : x2-5]

        if crop.size == 0:
            result[row][column] = "E"
            continue

        cv2.imwrite("debug/digits"+str(row)+str(column)+".jpg",crop)
        digit = cv2.cv.CreateImageHeader((crop.shape[1],crop.shape[0]), cv2.cv.IPL_DEPTH_8U, 1)
        cv2.cv.SetData(digit, crop.tostring(), crop.dtype.itemsize*crop.shape[1])
        
        ##recognize the digit
        result[column][row] = OCR.ocr_singledigit(digit)

        
##print out the sudoku puzzle
for row in result:
	string = ""
	for digit in row:
		string+= str(digit) + " "
	print string

print 
print "Total time: " + str(time.time()-timer_start)
