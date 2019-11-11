import glob
import os
import datetime
import numpy as np
import tensorflow as tf
from skimage import io, transform
from tensorflow import keras

w, h = 100, 100


def read_img(path, number):
    """
    定义函数read_img，用于读取图像数据，并且对图像进行resize格式统一处理
	"""
    cate = [path + x for x in os.listdir(path) if os.path.isdir(path + x)]
    train_imgs = []
    train_labels = []
    vali_imgs = []
    vali_labels = []
    for idx, folder in enumerate(cate):
        count = 0
        for im in glob.glob(folder + '/*.jpg'):
            print('reading the images: %s' % im)
            img = io.imread(im)
            img = transform.resize(img, (w, h))
            if count < int(number * 0.8):
                train_imgs.append(img)
                train_labels.append(idx)
            else:
                vali_imgs.append(img)
                vali_labels.append(idx)
            count += 1
    return ((np.asarray(train_imgs, np.float32), np.asarray(train_labels, np.int32)),
            (np.asarray(vali_imgs, np.float32), np.asarray(vali_labels, np.int32)))


# 网络模型
model = [
    # layer1: 100, 100, 3 => 50, 50, 32
    keras.layers.Conv2D(32, (5, 5), padding="same", activation=tf.nn.relu),
    keras.layers.Dropout(0.5),
    keras.layers.MaxPool2D(strides=(2, 2)),
    # layer2: => 25, 25, 64
    keras.layers.Conv2D(64, (5, 5), padding="same", activation=tf.nn.relu),
    keras.layers.Dropout(0.5),
    keras.layers.MaxPool2D(strides=(2, 2)),
    # layer3: => 12, 12, 128
    keras.layers.Conv2D(128, (3, 3), padding="same", activation=tf.nn.relu),
    keras.layers.Dropout(0.5),
    keras.layers.MaxPool2D(strides=(2, 2)),
    # layer4: => 6, 6, 128
    keras.layers.Conv2D(128, (3, 3), padding="same", activation=tf.nn.relu),
    keras.layers.Dropout(0.5),
    keras.layers.MaxPool2D(strides=(2, 2)),

    keras.layers.Flatten(),

    # layer1: 6*6*128=4608 => 1024
    keras.layers.Dense(1024, activation=tf.nn.relu),
    keras.layers.Dropout(0.5),
    # layer2: => 512
    keras.layers.Dense(512, activation=tf.nn.relu),
    keras.layers.Dropout(0.5),
    # layer3: => 128
    keras.layers.Dense(128, activation=tf.nn.relu),
    keras.layers.Dropout(0.5),
    # layer4: => 5
    keras.layers.Dense(2, activation=tf.nn.softmax),
    # keras.layers.Dropout(0.5)

    # keras.layers.Softmax()
]

# 建立模型
net = tf.keras.Sequential(model)
net.build(input_shape=(None, 100, 100, 3))

# 读取数据
(train_x, train_y), (vali_x, vali_y) = read_img('res/photos/', 100)

# 数据处理
train_y = tf.one_hot(train_y, depth=2, axis=1)
vali_y = tf.one_hot(vali_y, depth=2, axis=1)
train_x = tf.convert_to_tensor(train_x, dtype=tf.float32)
vali_x = tf.convert_to_tensor(vali_x, dtype=tf.float32)

# print(train_x.shape)
# print(train_y.shape)
# print(vali_x.shape)
# print(vali_y.shape)

net.compile(
    optimizer='adam',
    # loss='categorical_crossentropy',
    # loss=keras.losses.categorical_crossentropy,
    loss=keras.losses.CategoricalCrossentropy(),
    metrics=['accuracy']
)

# net.summary()

# Windows下运行会出错
# log_dir="logs/fit/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
# 下面正确
log_dir="logs\\fit\\" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)

net.fit(
    train_x, train_y,
    batch_size=64,
    epochs=5,
    validation_data=(vali_x, vali_y),
    callbacks=[tensorboard_callback]  # tensorboard
)

net.save('models/face_v2.h5')
print('model is saved.')
