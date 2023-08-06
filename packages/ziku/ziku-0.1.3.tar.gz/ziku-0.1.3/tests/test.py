import ziku
import cv2
ziku.size(0.4)
img=cv2.imread("测试图片.png")
img=ziku.write(img,"!@#$%^&",x=100,y=100)

ziku.size(0.6)
img=ziku.write(img,"123450asdkfjowvlASFKA:LKSJF",x=100,y=200)
cv2.imwrite("ziku.png",img)

ziku.size(0.8)
img=ziku.write(img,"老师明明可以靠颜值",x=100,y=300)
cv2.imwrite("ziku.png",img)

ziku.size(1)
img=ziku.write(img,"@@@@@@@",x=100,y=400)
cv2.imwrite("ziku.png",img)
