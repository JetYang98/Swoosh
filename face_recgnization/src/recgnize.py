from skimage import io,transform    # skimage包主要用于图像数据的处理，在该实验当中，
                                    # io模块主要图像数据的读取（imread）和输出（imshow）操作，transform模块主要用于改变图像的大小（resize函数）
import tensorflow as tf # tensorflow是目前业界最流行的深度学习框架，在图像，语音，文本，目标检测等领域都有深入的应用。是该实验的核心，主要用于定义占位符，定义变量，创建卷积神经网络模型

import numpy as np  # numpy是一个基于python的科学计算包，在该实验中主要用来处理数值运算，包括创建爱你等差数组，生成随机数组，聚合运算等。

# path='res/photos/'  # 数据存放路径 
model_path='models/model.ckpt'  # 模型保存路径 
base_path = 'temp/'

# 定义花类字典，对每种花都赋值一个数值类别
flower_dict = {0:'李凯',1:'杨宗瑾',2:'胡英强',3:'衷佩玮',4:'陈逢'} 

# 定义转换之后测试花类图像的大小（长宽高分别是100,100,3）
w=100
h=100
c=3

# 定义read_one_image函数，用于将验证图像转换成统一大小的格式（100*100*3）
def read_one_image(path):               # 定义函数read_one_image
    img = io.imread(path)               # 利用io.imread函数读取图像 
    img = transform.resize(img,(w,h))   # 利用transform.resize函数对读取的图像数据进行格式统一化处理 
    return np.asarray(img)              # 对img图像数据进行转化 

with tf.Session() as sess:              # 创建会话，用于执行已经定义的运算
    data = []                           # 定义空白列表，用于保存处理后的验证数据 
    for i in range(20):
        path = base_path + '%s.jpg'%(i+1)
        data1 = read_one_image(path)   # 利用自定义函数read_one_image依次对5张验证图像进行格式标准化处理
        data.append(data1)                  # 将处理过后的验证图像数据保存在前面创建的空白data列表当中

    saver = tf.train.import_meta_graph('models/model.ckpt.meta')     # 利用import_meta_graph函数直接加载之前已经持久化了的模型内容
    saver.restore(sess,tf.train.latest_checkpoint('models/'))         # 利用restore函数加载已经训练好的模型，并利用tf.train.latest_checkpoint函数提取最近一次保存的模型

    graph = tf.get_default_graph()              # 获取当前的默认计算图 

    x = graph.get_tensor_by_name("x:0")         # 返回给定名称的tensor
    print(x)                                  # 返回加载的模型的参数 

    feed_dict = {x:data}                        # 利用feed_dict，给占位符传输数据 

    logits = graph.get_tensor_by_name("logits_eval:0")      # 返回logits_eval对应的tensor
    print(logits)

    classification_result = sess.run(logits,feed_dict)      # 利用feed_dict把数据传输到logits进行验证图像预测

    output = tf.argmax(classification_result,1).eval()      # 选择出预测矩阵每一行最大值的下标，并将字符串str当成有效的表达式来求值并返回计算结果，将其赋值给output
    print(output)
    print(output.shape)

    for i in range(len(output)):                            # 遍历len(output)=5的花的类型
        print("people",i+1,"prediction:"+flower_dict[output[i]])    # 输出每种花预测值最高的选项 
