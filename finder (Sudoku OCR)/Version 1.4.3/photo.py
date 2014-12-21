import os
import time 

st = time.time()
print "Taking picture"
photo_com="sudo raspistill -w 600 -h 600 -cfx 128:128 -q 100 -e jpg -sh 100 -ex night -co 100 -o image.jpg" 
os.system(photo_com)
print "Improving quality"
quality="sudo convert image.jpg -quality 100 -sharpen 10 -sigmoidal-contrast 5 -contrast image.jpg"
os.system(quality)

print "Time: " + round(st - time.time(), 2)