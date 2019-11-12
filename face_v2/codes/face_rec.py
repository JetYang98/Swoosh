import glob
import numpy as np
import tensorflow as tf
from skimage import io, transform
from tensorflow import keras
import os 

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

net = keras.models.load_model('models/face_v2.h5')
labels = {
    0: '陈逢',
    1: '李凯'
}


def read_img(path):
    """
    定义函数read_img，用于读取图像数据，并且对图像进行resize格式统一处理
	"""
    w, h = 100, 100
    imgs = []
    for im in glob.glob(path + '/*.jpg'):
        print('reading the images:%s' % im)
        img = io.imread(im)
        img = transform.resize(img, (w, h))
        imgs.append(img)
    return np.asarray(imgs, np.float32)


x = read_img('temp/')
pre = tf.argmax(net.predict(x), axis=1).numpy()

for i in pre:
    print(labels.get(i))
