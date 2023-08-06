# 这是一个字库软件包
# 使用方法：
```
import ziku
import cv2
ziku.size(0.4)
img=cv2.imread("src/ziku/earthmap.png")
img=ziku.write(img,"太阳当空照",x=100,y=100)

ziku.size(0.6)
img=ziku.write(img,"花儿对我笑",x=100,y=200)
cv2.imwrite("ziku.png",img)

ziku.size(0.8)
img=ziku.write(img,"小鸟说 早早早",x=100,y=300)
cv2.imwrite("ziku.png",img)

ziku.size(1)
img=ziku.write(img,"你为什么背上大书包",x=100,y=400)
cv2.imwrite("ziku.png",img)
```


## 版本0.1.3增加了如下字符：

1. 中文字符:“～！@#\%……&*（）——）+「」「｜：“《》？”
2. 英文字符:~!|{}
