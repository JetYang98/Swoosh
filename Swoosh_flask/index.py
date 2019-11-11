from modules import verify
import time, os.path, openpyxl, os
from flask import Flask, render_template, send_from_directory, request, redirect, url_for

app = Flask(__name__)
v = verify.Verify()    # 对数据库操作的类 对象化

@app.route("/", methods=["GET", "POST"])
def login():
    """
    商家登陆界面，判断用户名和密码是否正确
    """
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if v.vendor_login(username, password):
            return render_template('system.html', username=username)
        else:
            error_msg = "用户名或密码不正确"
            return render_template('login.html', error_msg=error_msg)

@app.route("/system/", methods=["GET", "POST"])
def system():
    """
    系统主页
    """
    p1 = request.form.get("p1", None)
    if p1 is None:
        return redirect("")
    return render_template('system.html')

@app.route("/identify/", methods=["GET", "POST"])
def identify():
    """
    商家认证界面，根据licence进行认证
    """
    if request.method == 'GET':
            return render_template('identify.html')

    if request.method == 'POST':
        license = request.form['license']
        username = request.form['username']
        password = request.form['password']
        if v.vendor_verify(username,password,license) == True:
            return redirect('system')
        elif v.vendor_verify(username, password, license) == 'nolicense':
            error_msg = "商家证书不存在或已被使用"
        elif v.vendor_verify(username, password, license) == 'license':
            error_msg = "商家证书或者用户名错误"
        elif v.vendor_verify(username,password,license) == 'username':
            error_msg = "用户名不能为空或者大于二十位，只能包含'_'"
        elif v.vendor_verify(username, password, license) == 'pw':
            error_msg = "密码不能为空或者大于二十位"
        return render_template('identify.html', error_msg=error_msg)

@app.route("/cuslist/", methods=["GET", "POST"])
def cuslist():
    """
    列出顾客信息
    """
    if request.method == 'GET':

        p1 = request.args.get("p1", None)
        if p1 is None:
            return redirect('')

        datas = []
        datas_temp = v.query_customer_info('')

        for data in datas_temp:
            temp = []
            try:
                name = data[1]
            except:
                name = '-'
            try:
                gender = data[3]
            except:
                gender = '-'
            try:
                phone = data[4]
            except:
                phone = '-'
            try:
                s = str(data[2])
                s = s.replace('-', '')
                s = int(s[:4])
                a = time.localtime()
                dy = a[0] - s
                birth = dy
                if birth > 200:
                    birth = '-'
            except:
                birth = '-'

            if os.path.exists(r'.\static\customers_pic\%s.png' % data[0]):
                temp.append(data[0])
            else:
                temp.append("face")
            temp.append(data[0])
            temp.append(name)
            temp.append(gender)
            temp.append(birth)
            temp.append(phone)
            temp.append(data[5])
            datas.append(temp)

        return render_template('cuslist.html', datas=datas, username=p1)
    if request.method == 'POST':
        datas = []
        id_or_name = request.form.get("id_or_name", "")
        datas_temp = v.query_customer_info(str(id_or_name))
        
        for data in datas_temp:
            temp = []
            try:
                name = data[1]
            except:
                name = '-'
            try:
                gender = data[3]
            except:
                gender = '-'
            try:
                phone = data[4]
            except:
                phone = '-'
            try:
                s = str(data[2])
                s = s.replace('-', '')
                s = int(s[:4])
                a = time.localtime()
                dy = a[0] - s
                birth = dy
                if birth > 200:
                    birth = '-'
            except:
                birth = '-'

            if os.path.exists(r'.\static\customers_pic\%s.png' % data[0]):
                temp.append(data[0])
            else:
                temp.append("face")
            temp.append(data[0])
            temp.append(name)
            temp.append(gender)
            temp.append(birth)
            temp.append(phone)
            temp.append(data[5])
            datas.append(temp)

        return render_template('cuslist.html', datas=datas)

@app.route("/cussta/")
def cussta():
    """
    利用echarts显示会员注册的按时间注册的图表，年龄分布，性别比例
    """
    p1 = request.args.get("p1", None)
    if p1 is not None:
        make_cussta(v.query_customer_info(''))
        return render_template('cussta.html', usernmae=p1)
    else:
        return redirect('')

@app.route("/recom/", methods=["GET", "POST"])
def recom():
    """
    用户喜好，根据顾客id返回顾客买东西的前六中商品
    """
    if request.method == 'GET':
        p1 = request.args.get("p1", None)
        if p1 is not None:
            return render_template('recom.html', username=p1)
        else:
            return redirect('')
    if request.method == 'POST':
        datas = []
        id = str(request.form.get('id', ""))
        datas_temp = sort_interest(id)

        for data in datas_temp:
            temp = []
            x = v.query_item_info(data[1])
            temp.append(data[0])
            temp.append(data[1])
            temp.append(x[0][1])
            temp.append(data[2])
            datas.append(temp)

        return render_template('recom.html', datas=datas)

@app.route("/tralist/", methods=["GET", "POST"])
def tralist():
    """
    列出订单信息，可根据顾客id或者订单id进行查询
    """
    if request.method == 'GET':

        p1 = request.args.get("p1", None)
        if p1 is None:
            return redirect('')

        datas = []
        datas_temp = v.query_order_by_id('')

        for data in datas_temp:
            temp = []
            try:
                name = v.query_customer_info(data[1])
                name = name[0][1]
            except:
                name = '-'
            temp.append(data[0])
            temp.append(data[1])
            temp.append(name)
            temp.append(data[5])
            temp.append(data[6])
            temp.append(data[7])
            datas.append(temp)

        return render_template('tralist.html', datas=datas, username=p1)

    if request.method == 'POST':
        datas = []
        id = request.form.get("id", "")
        datas_temp = v.query_order_by_id(id)
        
        for data in datas_temp:
            temp = []
            try:
                name = v.query_customer_info(data[1])
                name = name[0][1]
            except:
                name = '-'
            temp.append(data[0])
            temp.append(data[1])
            temp.append(name)
            temp.append(data[5])
            temp.append(data[6])
            temp.append(data[7])
            datas.append(temp)

        return render_template('tralist.html', datas=datas)

@app.route("/uptrade/", methods=["GET", "POST"])
def uptrade():
    """
    上传订单界面
    """
    if request.method == 'GET':
        p1 = request.args.get("p1", None)
        if p1 is not None:
            return render_template('uptrade.html', username=p1)
        else:
            return redirect('')
    if request.method == 'POST':
        content = request.files.get("upload", None)
        if content is not None:
            if not os.path.exists("temp"):
                os.mkdir("temp")
            position = os.path.join(r'.\static\temp', content.name)
            content.save(position)
            inwb = openpyxl.load_workbook(position)
            sheetnames = inwb.get_sheet_names()
            ws = inwb.get_sheet_by_name(sheetnames[0])
            rows = ws.max_row
            os.remove(position)
            orders = []
            for i in range(rows):
                orders.append([ws.cell(i+1, 1).value, ws.cell(i+1, 2).value, ws.cell(i+1, 3).value,
                               ws.cell(i+1, 4).value, ws.cell(i+1, 5).value, ws.cell(i+1, 6).value])
            for order in orders:
                a = str(order[1])
                b = str(order[3])
                a = a.replace('，', ',')
                b = b.replace('，', ',')
                print(order)
                v.add_order(str(order[0]), a, str(order[2]), b, str(order[4]), str(order[5]))
                i_id = []
                i_num = []
                i_id.extend(a.split(','))
                i_num.extend(b.split(','))
                for i in range(len(i_id)):
                    v.update_kucun(i_id[i],i_num[i])
                temp = str(order[1]).replace('，', ',')
                temp = temp.split(',')
                if isinstance(temp, int):
                    temp = [temp]
                update_interest(str(order[0]), temp)
            error_msg = "添加商品成功"
            return render_template('uptrade.html', error_msg=error_msg)
        else:
            error_msg = "添加商品失败"
            return render_template('uptrade.html', error_msg=error_msg)

@app.route("/goodlist/", methods=["GET", "POST"])
def goodlist():
    """
    列出商品优惠信息，可根据id删除商品优惠信息，查询商品优惠信息
    """
    if request.method == 'GET':

        p1 = request.args.get("p1", None)
        if p1 is None:
            return redirect('')

        datas = []
        datas_temp = v.query_item_discount()

        for data in datas_temp:
            temp = []
            start_time = data[5]
            end_time = data[6]
            if start_time is None:
                start_time = ''
            if end_time is None:
                end_time = ''
            discount_time = str(start_time) + '~' + str(end_time)
            discount = data[4]
            if discount is None:
                discount = '-'

            if os.path.exists(r'.\static\items_pic\%s.png'%data[0]):
                temp.append(data[0])
            else:
                temp.append("milk")
            temp.append(data[0])
            temp.append(data[1])
            temp.append(data[2])
            temp.append(discount)
            temp.append(discount_time)
            datas.append(temp)

        return render_template('goodlist.html', datas=datas, username=p1)
    if request.method == 'POST':
        datas = []
        if request.form.get('search', None) is not None:
            id_or_name = request.form.get("id_or_name", "")
            datas_temp = v.query_item_info(str(id_or_name))

            for data in datas_temp:
                temp = []
                start_time = data[5]
                end_time = data[6]
                if start_time is None:
                    start_time = ''
                if end_time is None:
                    end_time = ''
                discount_time = str(start_time) + '~' + str(end_time)
                discount = data[4]
                if discount is None:
                    discount = '-'

                if os.path.exists(r'.\static\items_pic\%s.png'%data[0]):
                    temp.append(data[0])
                else:
                    temp.append("milk")
                temp.append(data[0])
                temp.append(data[1])
                temp.append(data[2])
                temp.append(discount)
                temp.append(discount_time)
                datas.append(temp)

            return render_template('goodlist.html', datas=datas)

        if request.form.get('delete', None) is not None:
            id = request.form.get("id", "")
            v.delete_item_discount_by_item_id(str(id))
            datas_temp = v.query_item_info("")

            for data in datas_temp:
                temp = []
                start_time = data[5]
                end_time = data[6]
                if start_time is None:
                    start_time = ''
                if end_time is None:
                    end_time = ''
                discount_time = str(start_time) + '~' + str(end_time)
                discount = data[4]
                if discount is None:
                    discount = '-'

                if os.path.exists(r'.\static\items_pic\%s.png'%data[0]):
                    temp.append(data[0])
                else:
                    temp.append("milk")
                temp.append(data[0])
                temp.append(data[1])
                temp.append(data[2])
                temp.append(discount)
                temp.append(discount_time)
                datas.append(temp)

            return render_template('goodlist.html', datas=datas)

@app.route("/comgoods/", methods=["GET", "POST"])
def comgoods():
    """
    商品信息上传界面
    """
    if request.method == 'GET':
        p1 = request.args.get("p1", None)
        if p1 is not None:
            return render_template('comgoods.html', username=p1)
        else:
            return redirect('')
    if request.method == 'POST':
        id = str(request.form["id"])
        name = str(request.form["name"])
        price = str(request.form["price"])
        type = str(request.form['type'])
        discount = str(request.form["discount"])
        discount_start = str(request.form["discount_start"])
        discount_end = str(request.form["discount_end"])
        kucun = str(request.form['kucun'])
        if kucun != "":
            kucun = int(kucun)
        qudao = str(request.form['qudao'])
        content = request.files.get("upload", None)
        if id != '' and price != '':
            if content is not None:
                if not os.path.exists("items_pic"):
                    os.mkdir("items_pic")
                position = os.path.join(r'.\static\items_pic', id+'.png')
                content.save(position)
            if v.query_item_info(id) != ():
                v.add_item_discount_by_item_id(id, price, discount, discount_start, discount_end, kucun, qudao)
                error_msg = "修改成功"
                return render_template('comgoods.html', error_msg=error_msg)
            else:
                v.add_item_info(name, price, type, discount, discount_start, discount_end, id, kucun, qudao)
                error_msg = "添加商品成功"
                return render_template('comgoods.html', error_msg=error_msg)
        else:
            error_msg = "添加失败"
            return render_template('comgoods.html', error_msg=error_msg)

@app.route("/classgoods/", methods=["GET", "POST"])
def classgoods():
    """
    根据商品种类显示不同商品
    """
    if request.method == 'GET':

        if request.method == 'GET':
            p1 = request.args.get("p1", None)
        if p1 is None:
            return redirect('')

        datas = v.query_item_info_by_type('当季水果',2)
        datas = tuple_to_list(datas)
        for i in range(len(datas)):
            if not os.path.exists(r'.\static\items_pic\%s.png'%datas[i][0]):
                datas[i][0] = "milk"
        return render_template('classgoods.html', datas=datas, username=p1)
    if request.method == 'POST':
        if request.form.get('dangji', None) is not None:
            datas = v.query_item_info_by_type('当季水果',2)
            datas = tuple_to_list(datas)
            for i in range(len(datas)):
                if not os.path.exists(r'.\static\items_pic\%s.png'%datas[i][0]):
                    datas[i][0] = "milk"
            return render_template('classgoods.html', datas=datas)
        elif request.form.get('jiangguo', None) is not None:
            datas = v.query_item_info_by_type('浆果类', 2)
            datas = tuple_to_list(datas)
            for i in range(len(datas)):
                if not os.path.exists(r'.\static\items_pic\%s.png'%datas[i][0]):
                    datas[i][0] = "milk"
            return render_template('classgoods.html', datas=datas)
        elif request.form.get('guaguo', None) is not None:
            datas = v.query_item_info_by_type('瓜果类', 2)
            datas = tuple_to_list(datas)
            for i in range(len(datas)):
                if not os.path.exists(r'.\static\items_pic\%s.png'%datas[i][0]):
                    datas[i][0] = "milk"
            return render_template('classgoods.html', datas=datas)
        elif request.form.get('juguo', None) is not None:
            datas = v.query_item_info_by_type('橘果类', 2)
            datas = tuple_to_list(datas)
            for i in range(len(datas)):
                if not os.path.exists(r'.\static\items_pic\%s.png'%datas[i][0]):
                    datas[i][0] = "milk"
            return render_template('classgoods.html', datas=datas)
        elif request.form.get('heguo', None) is not None:
            datas = v.query_item_info_by_type('核果类', 2)
            datas = tuple_to_list(datas)
            for i in range(len(datas)):
                if not os.path.exists(r'.\static\items_pic\%s.png'%datas[i][0]):
                    datas[i][0] = "milk"
            return render_template('classgoods.html', datas=datas)
        elif request.form.get('renguo', None) is not None:
            datas = v.query_item_info_by_type('仁果类', 2)
            datas = tuple_to_list(datas)
            for i in range(len(datas)):
                if not os.path.exists(r'.\static\items_pic\%s.png'%datas[i][0]):
                    datas[i][0] = "milk"
            return render_template('classgoods.html', datas=datas)
        else:
            datas = v.query_item_info_by_type('当季水果',2)
            datas = tuple_to_list(datas)
            for i in range(len(datas)):
                if not os.path.exists(r'.\static\items_pic\%s.png'%datas[i][0]):
                    datas[i][0] = "milk"
            return render_template('classgoods.html', datas=datas)

@app.route("/predict/", methods=["GET", "POST"])
def predict():
    """
    商品销量预测，按照商品名或商品id显示本季度的销量和拟合曲线
    """
    if request.method == 'GET':
        p1 = request.args.get("p1", None)
        if p1 is not None:
            return render_template('predict.html', img_name="车厘子", username=p1)
        else:
            return redirect('')
    if request.method == 'POST':
        id_or_name = str(request.form['id_or_name'])
        if id_or_name not in ["车厘子", "葡萄柚", "杨桃"]:
            id_or_name = "车厘子"
        return render_template('predict.html', img_name=id_or_name)

@app.route("/userreg/", methods=["GET", "POST"])
def userreg():
    """
    用户注册界面，接收用户的信息
    """
    if request.method == 'GET':
        return render_template('userreg.html')
    if request.method == 'POST':
        username = request.form['username']
        pw = request.form['pw']
        repw = request.form['repw']
        name = request.form['name']
        gender = request.form['gender']
        birth = request.form['birth']
        phone = request.form['phone']
        content = request.files.get("test", None)
        if birth is None or birth == '':
            birth = '0000-00-00'
        if username != '' and pw != '' and repw != '':
            if pw != repw:
                error_msg = '两次密码不一致'
                return render_template('userreg.html', error_msg=error_msg)
            temp = v.member_sign_up(str(username), str(pw), str(name), str(birth), str(gender), str(phone))
            if temp == '会员用户名已存在' or (not temp):
                error_msg = "会员用户名已存在或格式不正确"
                return render_template('userreg.html', error_msg=error_msg)
            elif temp == '顾客信息添加失败':
                error_msg = "顾客信息添加失败"
                return render_template('userreg.html', error_msg=error_msg)
            else:
                if content is not None:
                    if not os.path.exists("customers_pic"):
                        os.mkdir("customers_pic")
                    position = os.path.join(r'.\static\customers_pic', temp + '.png')
                    content.save(position)
                error_msg = "注册成功"
                return render_template('userreg.html', error_msg=error_msg)
        else:
            error_msg = "格式不正确"
            return render_template('userreg.html', error_msg=error_msg)

def tuple_to_list(t):
    t = list(t)
    for i in range(len(t)):
        t[i] = list(t[i])
    return t

def make_cussta(datas):
    """
    动态更新会员的按时间注册的图标、性别比例、年龄分布界面
    """
    begin = '''
    $(function() {
	setOption("echarts-1", {
		//标题
		title: {
			text: '年龄分布'
		},
		//工具栏
		tooltip: {},
		//图表图注
		legend: {
			data: ['人数']
		},
		//x轴
		xAxis: {
			data: ["18岁以下", "19-25岁", "26-35岁", "36-45岁", "46-55岁", "56岁以上", "未知"]
		},
		//y轴
		yAxis: {},
		//系列
		series: [{
			name: '人数',
			//图表类型设置
			type: 'bar',
    '''
    begin2 = '''
    }]
	});
	setOption("echarts-2", {
		title: {
			text: '性别比例'
		},
		backgroundColor: '#3388cb',
		visualMap: {
			show: true,
			min: 0,
			max: 500000,
			inRange: {
				colorLightness: [2, 5.5]
			}
		},
		series: [{
			name: '性别比例',
			type: 'pie',
			radius: '60%',
			data: [{
    '''
    begin3 = '''
    }],
			roseType: 'angle',
			label: {
				normal: {
					textStyle: {
						color: 'rgba(255, 255, 255, 0.8)'
					}
				}
			},
			labelLine: {
				normal: {
					lineStyle: {
						color: 'rgba(255, 255, 255, 0.8)'
					}
				}
			},
			itemStyle: {
				normal: {
					color: '#c23531',
					// shadowBlur: 200,
					shadowColor: 'rgba(0, 0, 0, 0.8)'
				}
			}
		}]
	});
	setOption("echarts-3",{
	   title: {
    '''
    begin4 = '''
    },
    tooltip: {
        trigger: 'axis'
    },
    // legend: {
    //     data:['上网','QQ','游戏','音乐','看电影']
    // },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    toolbox: {
        feature: {
            saveAsImage: {}
        }
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
    },
    yAxis: {
        type: 'value'
    },
    series: [
        {
            name:'人数',
            type:'line',
            stack: '花费',
    '''
    begin5 = '''
    },
        // {
        //     name:'QQ',
        //     type:'line',
        //     stack: '花费',
        //     data:[220, 182, 191, 234, 290, 330, 310]
        // },
        // {
        //     name:'游戏',
        //     type:'line',
        //     stack: '花费',
        //     data:[150, 232, 201, 154, 190, 330, 410]
        // },
        // {
        //     name:'音乐',
        //     type:'line',
        //     stack: '花费',
        //     data:[320, 332, 301, 334, 390, 330, 320]
        // },
        // {
        //     name:'看电影',
        //     type:'line',
        //     stack: '花费',
        //     data:[820, 932, 901, 934, 1290, 1330, 1320]
        // }
    ]
	});
});
/*
 **功能:柱状、折线图
 **参数1：元素ID
 **参数2：配置项设置
 */
function setOption(ident, opt) {
	//基于准备好的dom,初始化echarts实例
	let myChart = echarts.init($('#' + ident)[0]);
	// 使用刚指定的配置项和数据显示图表。
	myChart.setOption(opt);
}
/*
 **功能:南丁格尔图
 **参数1：元素ID
 **参数2：配置项设置
 */
function setOption(ident, opt) {
	//基于准备好的dom,初始化echarts实例
	let myChart = echarts.init($('#' + ident)[0]);
	// 使用刚指定的配置项和数据显示图表。
	myChart.setOption(opt);
}
    '''
    x = [0,0,0,0,0,0,0]
    y = [0,0,0]
    z = [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    print(datas, '---\n')
    for data in datas:
        print(data)
        if data is None:
            continue
        a = time.localtime()
        if data[2] is not None:
            s = str(data[2])
        else:
            s = '0000-00-00'
        s = s.replace('-', '')
        s = s[:4]
        print('----\n',s,type(s))
        if s is None or s == '' or s == ' None':
            print('这里走了吗')
            s = 0
        s = int(s)
        dy = a[0] - s
        birth = int(dy)
        if birth <= 18:
            x[0] += 1
        elif 18 < birth <= 25:
            x[1] += 1
        elif 25 < birth <= 35:
            x[2] += 1
        elif 35 < birth <= 45:
            x[3] += 1
        elif 45 < birth <= 55:
            x[4] += 1
        elif 55 < birth <= 150:
            x[5] += 1
        else:
            x[6] += 1
        if data[3] == '女':
            y[1] += 1
        elif data[3] == '男':
            y[0] += 1
        else:
            y[2] += 1
        day = str(data[5])
        day = day.replace('-','')
        day = int(day[6:8])
        cu_month = str(data[5])
        cu_month = cu_month.replace('-','')
        if a[1] == int(cu_month[4:6]):
            z[day-1] += 1
    a = time.localtime()
    f = open('./static/js/common.js', 'w', encoding='utf8')
    f.write(begin)
    f.write('data: [%s, %s, %s, %s, %s, %s, %s]				//年龄数据传入' % (x[0], x[1], x[2], x[3], x[4], x[5], x[6]))
    f.write(begin2)
    f.write("value: %s,	//性别数据传入\nname: '男性',\n}, {\nvalue: %s,\nname: '女性',\n},{\nvalue: %s,\nname: '未知'," % (y[0],y[1],y[2]))
    f.write(begin3)
    f.write("text: '%s月会员注册人数统计'"%(a[1]))
    f.write(begin4)
    f.write("data:[%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s]       //总人数数据传入"%(z[0],z[1],z[2],z[3],z[4],z[5],z[6],z[7],z[8],z[9],z[10],z[11],z[12],z[13],z[14],z[15],z[16],z[17],z[18],z[19],z[20],z[21],z[22],z[23],z[24],z[25],z[26],z[27],z[28],z[29],z[30]))
    f.write(begin5)
    f.close()


def update_interest(customer_id, items_id):
    """
    更新储存的顾客的喜好到硬盘
    :param customer_id:
    :param items_id:
    :return:
    """
    file_path = r'.\static\interest\interest.txt'
    data = ''
    judg = 0
    n=1
    for item_id in items_id:
        n = n+1
        with open(file_path, 'r+') as f:
            for line in f.readlines():
                temp = line.split(' ')
                temp[2] = temp[2].replace('\n', '')
                if temp[0] == customer_id and temp[1] == item_id:
                    temp_int = int(temp[2])
                    temp_int += 1
                    temp[2] = str(temp_int)
                    temp = ' '.join(temp)
                    data = data + temp + '\n'
                    judg += 1
                else:
                    data = data + line
            f.seek(0)
            if judg != 0:
                f.write(data)
                judg = 0
            else:
                f.write(data+' '.join([customer_id, item_id, '1'])+'\n')
            data = ''


def sort_interest(customer_id):
    """
    排序顾客喜好，返回最喜欢的6种商品
    :param customer_id:
    :return:
    """
    file_path = r'.\static\interest\interest.txt'
    data = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            temp = line.split(' ')
            temp[2] = temp[2].replace('\n', '')
            if customer_id == temp[0]:
                data.append(temp)
    x = sorted(data, key=lambda s: s[2])
    x = x[::-1]
    return x[:7]


if __name__=='__main__':
    app.run(port=80, debug=True, host="0.0.0.0")
