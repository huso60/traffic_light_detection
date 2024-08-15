import cv2
import numpy as np
import tkinter
import time

index=1
img=cv2.imread("2.jpg")
def cut(frame,scale=0.75):
    widht=int(frame.shape[1]*scale)
    height=int(frame.shape[0]*scale)
    dimention=(widht,height)
    return cv2.resize(frame,dimention,interpolation=cv2.INTER_AREA)


img_r=cut(img)
cropped=img_r[0:700,0:700]
cv2.imshow("crroped",cropped)

blank=np.zeros(cropped.shape)

lab=cv2.cvtColor(cropped,cv2.COLOR_BGR2LAB)
cv2.imshow("lab",lab)

blur=cv2.GaussianBlur(lab,(5,5),cv2.BORDER_DEFAULT)
cv2.imshow("blur",blur)

cany=cv2.Canny(blur,100,150)
cv2.imshow("canny",cany)

contours,hierarchives=cv2.findContours(cany,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
print(f'{len(contours)} contours(s),found')
contours=sorted(contours,key=lambda x:cv2.contourArea(x),reverse=True)
cv2.drawContours(blank,contours,-1,(0,255,0),1)

cv2.imshow("contours",blank)
blank=np.zeros(cropped.shape)

contv=0
diff=0
hdiff=10

for cont in contours:
    contv=contv+1
    (x,y,w,h)=cv2.boundingRect(cont)
    diff=w-h

    if diff<0:
        diff=diff*-1

    if diff<hdiff:
        hdiff=diff
        index=contv-1
    if contv==5:
        break


(x,y,w,h)=cv2.boundingRect(contours[index])
xt=x-5
yt=y-5
cv2.rectangle(cropped,(xt,yt),(xt + w+10, yt+h+10),(0,255,0),2)
cv2.imshow("output",cropped)

cx=x+(w/2)
cy=y+(h/2)

cx=int(cx)
cy=int(cy)

r=int(img_r[cx][cy][2])
g=int(img_r[cx][cy][1])
b=int(img_r[cx][cy][0])
cv2.imshow("OUTPUT",img_r)



cv2.waitKey(0)
