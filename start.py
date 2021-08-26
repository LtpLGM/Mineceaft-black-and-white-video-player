import time
import mcpi.minecraft as minecraft
from mcpi import block
from mcpi.vec3 import Vec3
from PIL import Image

#常量区
HEIGHT=128#图片横向长
WIDTH=96#图片纵向长
X=0#据出生点x距离
Y=100#高度
Z=0#据出生点z距离
SPEED=2#最大帧数率

mc = minecraft.Minecraft.create()

def set_(x,y,z,color):
    '''用户自定义函数，由game_loop()调用
        x,y,z为显示坐标，color为0 or 1(int)
        heng_h:横像素长，默认64
        zong_h:纵像素长，默认48'''
    if color==0:
        mc.setBlock(x,y,z,block.WOOL.id,16)#黑色
    else:
        mc.setBlock(x,y,z,block.WOOL.id,15)#白色

def flie_name(imp,address='',last_name='.jpg'):
    ''' 用户自定义函数，由input_image()调用
    输入值：address:图像集位置 例：D://ress 空为程序目录
           last_name:后缀名，默认.jpg
           imp:input_image()传入的图像编号，从1开始
        输出值：图像地址及名称，例：D:\\ress\\0001.jpg'''
    if(imp<10):
        imp_='000'+str(imp)
    if(imp>=10 and imp<100):
        imp_='00'+str(imp)
    if(imp>=100 and imp<1000):
        imp_='0'+str(imp)
    if(imp>=1000):
        imp_=str(imp)
    return address+'\\'+imp_+last_name

def input_image(address='',last_name='.jpg',heng_h=0,zong_h=0):
    """导入图像
    输入值：address:图像集位置 例：D://ress 空为程序目录
           last_name:后缀名，默认.jpg
           heng_h:横像素长，默认为第一帧图像长
           zong_h:纵像素长，默认为第一帧图像宽
    输出值：三维元组（帧编号，横坐标，纵坐标，黑白值0为黑1为白）,帧编号自1开始"""
    imp=0#图像指针
    black_waite=[]
    heng_black_waite=[]
    zong_black_waite=[]
    while True:
        try:
            imp=imp+1
            add=flie_name(imp,address=address,last_name=last_name)
            im = Image.open(add)
            #print(address+imp_+last_name)
            #im.show()
            px=im.load()
            if heng_h==0:
                heng_h=im.size[0]
            if heng_h==0:
                heng_h=im.size[1]
            for m in range(0,heng_h):#横向
                for n in range(0,zong_h):#纵向
                    rgb=list(px[m,n])
                    if rgb[0]+rgb[1]+rgb[2]>256*3/2:
                        heng_black_waite.append(0)
                    else:
                        heng_black_waite.append(1)
                zong_black_waite.append(heng_black_waite)
                heng_black_waite=[ ]#清空列表
           

        except:
            print("输入结束，共有"+str(imp-1)+"张图片")
            black_waite.append(zong_black_waite)
            del black_waite[len(black_waite)-1:len(black_waite)]
            zong_black_waite=[ ]#清空列表
            break
        
        black_waite.append(zong_black_waite)
        zong_black_waite=[ ]#清空列表
    
    return black_waite


def game_loop(video,y_int,zhen_speed,heng_h=64,zong_h=48):
    '''视频授时
    video: input_image的返回值
    将会调用户自定义函数set_(x,y,z,color):
        vedio为input_image()返回值
        y_int为高度
        zhen_speed为帧速率
        heng_h:横像素长，默认64
        zong_h:纵像素长，默认48
        '''
    mc = minecraft.Minecraft.create()
    print(mc.player.getTilePos())
    try:
        for zhen in range(0,len(video)-1):
            zhen_time=time.time()
            print(zhen)

            for m in range(1,heng_h):#横向
                for n in range(1,zong_h):#纵向
                    if video[zhen][m][n]==0:
                        set_(m,y_int,n,0)
                    else:
                        set_(m,y_int,n,1)
            p=0.0
            while not time.time()-zhen_time>1/zhen_speed:
                time.sleep(0.00001)
                p+1

    except NameError:
        raise Exception('未找到set_(x,y,z,color)函数')


a=input_image("D:\\HMCL\\.minecraft\\mcpipy\\vehicles\\picture128\\",heng_h=HEIGHT,zong_h=WIDTH)#初始化图像
game_loop(a,Y,SPEED,HEIGHT,WIDTH)#在游戏中加载
