from skimage import io, transform    # skimage包主要用于图像数据的处理，在该实验当中，
# io模块主要图像数据的读取（imread）和输出（imshow）操作，transform模块主要用于改变图像的大小（resize函数）
import tensorflow as tf
import numpy as np
import cv2
import sys, tkinter
from collections import Counter


def catch_pic_from_video(window_name, camera_idx, catch_pic_num, path_name):
    cv2.namedWindow(window_name)

    # 视频来源，可以来自一段已存好的视频，也可以直接来自USB摄像头
    cap = cv2.VideoCapture(camera_idx)

    # 告诉OpenCV使用人脸识别分类器
    classifier = cv2.CascadeClassifier("./haarcascade_frontalface_alt2.xml")

    # 识别出人脸后要画的边框的颜色，RGB格式
    color = (0, 255, 0)

    num = 0
    while cap.isOpened():
        ok, frame = cap.read()  # 读取一帧数据
        if not ok:
            break
        grey = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # 将当前桢图像转换成灰度图像
        # 人脸检测，1.2和2分别为图片缩放比例和需要检测的有效点数
        face_rects = classifier.detectMultiScale(grey, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))
        if len(face_rects) > 0:  # 大于0则检测到人脸
            for faceRect in face_rects:  # 单独框出每一张人脸
                x, y, w, h = faceRect

                # 将当前帧保存为图片
                img_name = '%s/%d.jpg ' %(path_name, num)
                image = frame[y - 10: y + h + 10, x - 10: x + w + 10]
                cv2.imwrite(img_name, image)

                num += 1
                if num > catch_pic_num:  # 如果超过指定最大保存数量退出循环
                    break

                # 画出矩形框
                cv2.rectangle(frame, (x - 10, y - 10), (x + w + 10, y + h + 10), color, 2)

                # 显示当前捕捉到了多少人脸图片了，这样站在那里被拍摄时心里有个数，不用两眼一抹黑傻等着
                font = cv2.FONT_HERSHEY_SIMPLEX
                cv2.putText(frame, 'num:%d' % num, (x + 30, y + 30), font, 1, (255, 0, 255), 4)

                # 超过指定最大保存数量结束程序
        if num > catch_pic_num: break

        # 显示图像
        cv2.imshow(window_name, frame)
        c = cv2.waitKey(10)
        if c & 0xFF == ord('q'):
            break

            # 释放摄像头并销毁所有窗口
    cap.release()
    cv2.destroyAllWindows()


def rec():
    if len(sys.argv) != 1:
            print("Usage:%s camera_id face_num_max path_name\r\n" % (sys.argv[0]))
    else:
        catch_pic_from_video("Face_Recognition", 0, 20, './res/photos/temp/')
        # model_path='res/Models/model.ckpt'  # 模型保存路径
        # 从原始数据集的每个类别中各自随机抽取一张图像进行模型验证
        base_path = './res/photos/temp/'

        # 定义花类字典，对每种花都赋值一个数值类别
        flower_dict = {0: '陈逢', 1: '李凯', 2: '衷佩玮'}

        # 定义转换之后测试花类图像的大小（长宽高分别是100,100,3）
        w = 100
        h = 100
        c = 3

        # 定义read_one_image函数，用于将验证图像转换成统一大小的格式（100*100*3）
        def read_one_image(path):               # 定义函数read_one_image
            img = io.imread(path)               # 利用io.imread函数读取图像 
            img = transform.resize(img, (w, h))   # 利用transform.resize函数对读取的图像数据进行格式统一化处理
            return np.asarray(img)              # 对img图像数据进行转化 

        with tf.Session() as sess:              # 创建会话，用于执行已经定义的运算
            data = []                           # 定义空白列表，用于保存处理后的验证数据 
            for i in range(20):
                path = base_path + '%s.jpg' % (i+1)
                data1 = read_one_image(path)   # 利用自定义函数read_one_image依次对5张验证图像进行格式标准化处理
                data.append(data1)                  # 将处理过后的验证图像数据保存在前面创建的空白data列表当中

            saver = tf.train.import_meta_graph('res/Models/model.ckpt.meta')     # 利用import_meta_graph函数直接加载之前已经持久化了的模型内容
            saver.restore(sess, tf.train.latest_checkpoint('res/Models'))         # 利用restore函数加载已经训练好的模型，并利用tf.train.latest_checkpoint函数提取最近一次保存的模型

            graph = tf.get_default_graph()              # 获取当前的默认计算图
            x = graph.get_tensor_by_name("x:0")         # 返回给定名称的tensor
            feed_dict = {x: data}                        # 利用feed_dict，给占位符传输数据
            logits = graph.get_tensor_by_name("logits_eval:0")      # 返回logits_eval对应的tensor
            classification_result = sess.run(logits, feed_dict)      # 利用feed_dict把数据传输到logits进行验证图像预测
            output = tf.argmax(classification_result, 1).eval()      # 选择出预测矩阵每一行最大值的下标，并将字符串str当成有效的表达式来求值并返回计算结果，将其赋值给output
            temp = []
            for i in range(len(output)):                            # 遍历len(output)=5的花的类型
                temp.append(flower_dict[output[i]])
        a = Counter(temp).most_common(1)
        global lat
        lat.config(text='识别出的人为：' + a[0][0])


if __name__ == '__main__':
    root = tkinter.Tk()
    root.title('Swoosh人脸识别系统')
    root['width']=900
    root['height']=600
    root.geometry('+495+230')
    # root.resizable(width=False,height=False)
    logo = tkinter.PhotoImage(file='./res/swoosh.png')
    frm1 = tkinter.Frame(root, width=900, height=200)
    frm1.pack(side='top')
    l = tkinter.Label(frm1, image=logo).grid(row=0)
    frm2 = tkinter.Frame(root, width=900, height=400)
    frm2.pack()
    tkinter.Label(frm2).grid(row=0)
    tkinter.Label(frm2).grid(row=1)
    tkinter.Label(frm2).grid(row=2)
    bt1 = tkinter.Button(frm2, text='识别', width=7, height=2, command=rec)
    bt1.grid(row=3, column=0)
    lat = tkinter.Label(frm2, text='识别出的人为: ')
    lat.grid(row=3, column=2)
    tkinter.Label(frm2).grid(row=4)
    root.mainloop()
