#字库
import cv2,os,numpy as np

class ZIKU:
    """ 这个类读出字库中的汉字的图片，然后写在图片上"""
    def __init__(self):
        """初始化函数，默认写汉字大小为0.5,颜色为红色255,0,0,两字符之间的间隔为2"""
        self.name="ziku"
        current_dir=os.path.dirname(__file__)#当前文件所在目录
        self.zikudir=os.path.join(current_dir,"ZIKU")
        self.zi={}
        self._size=0.6
        self.color=np.array([255,0,0])
        self.zifujiange=2
    def set_size(self, size):
        """
            message 属性设置器
        """
        self._size = size

    def get(self,zihao="明"):
        """ 读取zihao所对应的文字的图片"""
        zis=[]
        for zihao_ in zihao:
            if zihao_==".":
                zihao_="dot"
            elif zihao_=="/":
                zihao_="youxie"
            elif zihao_.isupper():
                zihao_=zihao_+"_"
            elif zihao_==" ":
                zihao_="space"
            if zihao_=="space":
                zi=np.array([-1])
            else:    	
                zi=cv2.imread(os.path.join(self.zikudir,'%s.png'%(zihao_)))
            #print(zihao_)
            #print(zi.shape)
            zis.append(zi)
        return zis
    def write(self,img,zihao="明",x=0,y=0):
        """ 把明字写在图片的(x,y)位置处"""
        return self.write2Img(img,zihao,pos=np.array([y,x]))
    def write2Img(self,img,zihao="明",pos=np.array([0,0])):
        zis=self.get(zihao)
        size=int(self._size*50)
        i=0
        last_pos_x=pos[1]
        move=0
        for zi in zis:
            if zi.shape[0]==1 and zi[0]==-1:
                last_pos_x=size+last_pos_x
                continue	
            zi=cv2.resize(zi,(size,size))
            hzi,wzi=zi.shape[0:2]
            select_index=(zi.sum(2)>128)
            move=int((select_index.sum(0)>0).sum())+self.zifujiange
            zi[select_index]=np.flipud(self.color)
            #select_index=select_index[:,select_index.sum(0)>0]
            #wzi=select_index.shape[1]
            if pos[0]+hzi<img.shape[0] and last_pos_x+wzi<img.shape[1]:
                img[pos[0]:(pos[0]+hzi),(last_pos_x):(wzi+last_pos_x)][select_index]=zi.copy()[select_index]
            else:
                break
            i=i+1
            last_pos_x=move+last_pos_x
        return img
    def test(self):
        """ 测试用的函数，运行后，把一些汉字写入例子图片上，然后保存到当前目录下的Ziku.png中"""
        current_dir=os.path.dirname(__file__)#当前文件所在目录
        print(current_dir)
        self.size=0.5
        img = np.zeros((300,300,3))
        img = cv2.imread(os.path.join(current_dir,"earthmap.png"))
        
        #img[0:hzi,0:wzi][select_index]=zi.copy()[select_index]
        self.write2Img(img,'老师明明可以靠颜值-汉字字库',pos=np.array([50,50]))
        self.write2Img(img,'字库的使用办法:',pos=np.array([110,50]))
        self.write2Img(img,'import-ZIKU',pos=np.array([170,50]))
        self.write2Img(img,'ziku=ZIKU("./ZIKU")',pos=np.array([230,50]))
        self.write2Img(img,'ziku.write2Image(img,"你要写的字")',pos=np.array([300,50]))
        self.write2Img(img,'试着打印一组符号:  @@@@`-=[]\;\',./`\\',pos=np.array([370,50]))
        cv2.imwrite("ZiKu.png",img)
        print("save to ./ZiKu.png")


if __name__=="__main__":
    current_dir=os.path.dirname(__file__)#当前文件所在目录
    print(current_dir)
    ziku=ZIKU()
    ziku._size=0.5
    
    img = np.zeros((300,300,3))
    img = cv2.imread(os.path.join(current_dir,"earthmap.png"))
	
    #img[0:hzi,0:wzi][select_index]=zi.copy()[select_index]
    ziku.write2Img(img,'老师明明可以靠颜值-汉字字库',pos=np.array([50,50]))
    ziku.write2Img(img,'字库的使用办法:',pos=np.array([110,50]))
    ziku.write2Img(img,'import-ZIKU',pos=np.array([170,50]))
    ziku.write2Img(img,'ziku=ZIKU("./ZIKU")',pos=np.array([230,50]))
    ziku.write2Img(img,'ziku.write2Image(img,"你要写的字")',pos=np.array([300,50]))
    ziku.write2Img(img,'试着打印一组符号:  @@@@`-=[]\;\',./`\\',pos=np.array([370,50]))
    cv2.imwrite("ZiKu.png",img)








