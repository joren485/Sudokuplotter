import time
st=time.time()
import cv2
import numpy as np
import sys
debug=False

###Image PreProcessing###
###Works
print("Image preprocessing")
img = cv2.imread(sys.argv[1])
img = cv2.GaussianBlur(img,(5,5),0)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
mask = np.zeros((gray.shape),np.uint8)
kernel1 = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(11,11))

close = cv2.morphologyEx(gray,cv2.MORPH_CLOSE,kernel1)
div = np.float32(gray)/(close)
res = np.uint8(cv2.normalize(div,div,0,255,cv2.NORM_MINMAX))
res2 = cv2.cvtColor(res,cv2.COLOR_GRAY2BGR)

###Finding Sudoku Square and Creating Mask Image###
###Works
print("Finding Square")
thresh = cv2.adaptiveThreshold(res,255,0,1,19,2)

if debug:
	cv2.imwrite("thresh.jpg",thresh)

contour,hier = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

max_area = 0
best_cnt = None
for cnt in contour:
    area = cv2.contourArea(cnt)
    if area > 1000:
        if area > max_area:
            max_area = area
            best_cnt = cnt

cv2.drawContours(mask,[best_cnt],0,255,-1)
cv2.drawContours(mask,[best_cnt],0,0,2)

res = cv2.bitwise_and(res,mask)
if debug:
	cv2.imwrite("puzzle.jpg",res)


###Finding Vertical lines###
###Works
print("Finding V lines")
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
if debug:
	cv2.imwrite("vlines.jpg",closex)

###Finding Horizontal Lines ###
###Works
print("Finding H Lines")
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
if debug:
	cv2.imwrite("hlines.jpg",closey)

###Finding Grid Points###
###Works
print("Finding points")
res = cv2.bitwise_and(closex,closey)
if debug:
	cv2.imwrite("points.jpg",res)

###Correcting the defects###
###Works
print("Correcting defects")

contour, hier = cv2.findContours(res,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
centroids = []
for cnt in contour:
    mom = cv2.moments(cnt)
    (x,y) = int(mom['m10']/mom['m00']), int(mom['m01']/mom['m00'])
    cv2.circle(img,(x,y),4,(0,255,0),-1)
    centroids.append((x,y))

centroids = np.array(centroids,dtype = np.float32)
c = centroids.reshape((100,2))
c2 = c[np.argsort(c[:,1])]

b = np.vstack([c2[i*10:(i+1)*10][np.argsort(c2[i*10:(i+1)*10,0])] for i in xrange(10)])
bm = b.reshape((10,10,2))

###Final Stage###
###
result=""
size=630
size=(size,)*2
number=size[0]/9
print("OCR Stage")
import cv2.cv as cv
import OCR
for i,j in enumerate(b):	    
    ri = i/10
    ci = i%10
    if ci != 9 and ri!=9:
        src = bm[ri:ri+2, ci:ci+2 , :].reshape((4,2))
	dst = np.array( [ [ci*number,ri*number],[(ci+1)*number-1,ri*number],[ci*number,(ri+1)*number-1],[(ci+1)*number-1,(ri+1)*number-1] ], np.float32)
	retval = cv2.getPerspectiveTransform(src,dst)
	warp = cv2.warpPerspective(res2,retval,(size))
	whole_digit= warp[ri*number:(ri+1)*number-1 , ci*number:(ci+1)*number-1].copy()
	noborder_digit= whole_digit[5:64,5:64]
	gray_digit = cv2.cvtColor(noborder_digit,cv2.COLOR_BGR2GRAY)
	thresh_digit = cv2.adaptiveThreshold(gray_digit,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,0,151,80)
	image = cv.CreateImageHeader((thresh_digit.shape[1],thresh_digit.shape[0]), cv.IPL_DEPTH_8U, 1)
	cv.SetData(image, thresh_digit.tostring(), thresh_digit.dtype.itemsize*thresh_digit.shape[1])
	result+=OCR.ocr_singledigit(image)

rows = OCR.split_len(result,9)
for row in rows:
	print row
print time.time()-st
