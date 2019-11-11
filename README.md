# Swoosh

## face_v2文件夹

人脸识别，使用tensorflow2.0

> 在此文件夹下运行，否则会出现地址错误

### codes文件夹

*make_model.py*制作人脸识别模型，*face_rec.py*进行人脸识别

### res文件夹

将要训练的图片放到*res/photos*文件夹下，不同类别的图片放到不同的文件夹下，如李明图片放到*res/photos/liming/*文件夹下



## face_recgnization文件夹

简单的人脸识别，使用tensorflow1.x

> 在此文件夹下运行，否则会出现地址错误

### codes文件夹

*Face_recognition.py*人脸识别启动程序，*make_model.py*制作人脸识别模型

### res文件夹

将要训练的图片放到*res/photos*文件夹下，不同类别的图片放到不同的文件夹下，如李明图片放到*res/photos/liming/*文件夹下



## Swoosh_flask文件夹

使用flask重新设计了网页版的客户关系管理系统，使用到了数据库、Python、HTML、js等。

> 在此文件夹下运行，否则会出现地址错误

> 最主要使用到了flask中的动态生成页面，取消了Swoosh文件夹（下面）修改\*.html文件显示不同数据的弊端。其他文件请参考*Swoosh文件夹*的说明
>
> 增加了网站的保密性，直接输入URL会返回到登录页面。

**注意：**

- *add_license.py*使用了*MySQL*数据库，请**修改**里面的数据库**用户名**和**密码**（在前几行）
- *modules/db.py*使用了*MySQL*数据库，请**修改**里面的数据库**用户名**和**密码**（在前几行）



## Swoosh_Django文件夹

利用Django设计网页版的客户关系管理系统，使用到了数据库、Python、HTML等。

> 在此文件夹下运行，否则会出现地址错误

*add_license.py*是网站中申请用户名的20位LICENSE

*data.xlsx*是网站中的订单导入页面的示例文件，其他订单按照本格式上传。

**注意：**

- *add_license.py*使用了*MySQL*数据库，请**修改**里面的数据库**用户名**和**密码**（在前几行）
- *myWebsite/db.py*使用了*MySQL*数据库，请**修改**里面的数据库**用户名**和**密码**（在前几行）
