import cv2
import numpy as np
frameWidth = 640
frameHeight = 480
url = "http://192.168.0.101:8080/video"
cap=cv2.VideoCapture(url)
cap.set(3, frameWidth)
cap.set(4, frameHeight)
cap.set(10,150)

myColors = [[85,100,120,128,255,255], #blue
            [10,90,210,20,250,255], #orange
            [150,80,80,179,150,255], #pink
            [22,100,150,50,255,255]] #yellow
myColorValues = [[255,51,51],[51,153,255],[255,51,255],[51,255,255]] #bgr

myPoints = []   #[x, y, colorId]

#blue = [85,128,100,255,120,255]
#orange = [10,20,90,250,210,255]
#pink = [150,179,80,150,80,255]
#yellow = [22,50,100,255,150,255]
def findColor(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count=0
    newPoints=[]
    for color in myColors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV, lower, upper)
        x,y=getContours(mask)
        cv2.circle(imgResult,(x,y),10,myColorValues[count],cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x,y,count])
        count += 1
        #cv2.imshow(str(color[0]),mask)
    return newPoints

def getContours(img):
    contours,hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h=0,0,0,0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        #cv2.drawContours(imgcontour,cnt,-1,(255,0,0),3)
        if area>500:
            #cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt,True)
            approx = cv2.approxPolyDP(cnt,0.02*peri,True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2,y

def drawOnCanvas(myPoints,myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)

while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findColor(img, myColors,myColorValues)
    if len(newPoints)!=0:
        for newP in newPoints:
            myPoints.append(newP)
    if len(myPoints)!=0:
        drawOnCanvas(myPoints,myColorValues)
    cv2.imshow("result", imgResult)
    if cv2.waitKey(1) & 0xFF ==ord('q'):
        break