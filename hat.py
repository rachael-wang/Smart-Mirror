#-*- coding: utf-8 -*-
import time
import cv2
import sys
from PIL import Image
import multiprocessing as mp
def CatchUsbVideo(window_name, camera_idx, hatno):
    cv2.namedWindow(window_name)
    
    #视频来源，可以来自一段已存好的视频，也可以直接来自USB摄像头
    cap = cv2.VideoCapture(camera_idx)
    #cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH,1024)  
    #cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT,768) 
    #告诉OpenCV使用人脸识别分类器
    classfier = cv2.CascadeClassifier(r'./lbpcascade_frontalface.xml')
    if hatno==1:
        pic='h1.png'
    if hatno==2:
        pic='h2.jpg'
    if hatno==3:
        pic='h3.png'
    if hatno==4:
        pic='h4.jpg'
    #识别出人脸后要画的边框的颜色，RGB格式
    color = (0, 255, 0)
    time0=time.time()
    while cap.isOpened():
        ok, frame = cap.read() #读取一帧数据
        if not ok:            
            break  
        #将当前帧转换成灰度图
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)                 
        
        #人脸检测，1.2和2分别为图片缩放比例和需要检测的有效点数
        faceRects = classfier.detectMultiScale(grey, scaleFactor = 1.6, minNeighbors = 3, minSize = (16, 16))
        if len(faceRects) > 0:            #大于0则检测到人脸                                   
            flag=1
            for faceRect in faceRects:  #单独框出每一张人脸
                x, y, w, h = faceRect        
                cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, 2)
            if y>92*w/100:
                img2=cv2.imread(pic)
                rows,cols,channels=img2.shape
                w=6*w/5
                rows=3*w/4
                cols=w
                img2=cv2.resize(img2,(w,w),interpolation=cv2.INTER_CUBIC)
                roi = frame[(y-rows):(y+w-rows),x:(x+cols)]
                img2gray = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)#将logo图像灰度化
                ret,mask =cv2.threshold(img2gray,200,255,cv2.THRESH_BINARY)#将logo灰度图二值化，将得到的图像赋值给mask，logo部分的值为255，白色
                mask_inv = cv2.bitwise_not(mask)  #将mask按位取反，即白变黑，黑变白

                image_bg = cv2.bitwise_and(roi,roi,mask = mask)#将原始图像中截取的部分做处理，mask中黑色部分按位与运算，即保留黑色部分，保留除logo位置外的部分
                img2_fg = cv2.bitwise_and(img2,img2,mask = mask_inv)#将logo图像中，mask_inv部分按位与运算，即保留黑色部分，保留logo
                dst = cv2.add(image_bg,img2_fg) #图像相加
                frame[(y-rows):(y+w-rows),x:(x+cols)] = dst       #图像替换
        #显示图像       
        cv2.moveWindow(window_name,200,300)
        #cv2.resizeWindow(window_name,1024,768)
        cv2.imshow(window_name, frame)        
        c = cv2.waitKey(10)
        time1=time.time()
        if time1-time0 > 30:
            break        
    
    #释放摄像头并销毁所有窗口
    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == '__main__':
       CatchUsbVideo("识别人脸区域", 0, int(sys.argv[1]))
