from django.shortcuts import render
from django.http import HttpResponseRedirect
from myWebsite import verify
import time, os.path, openpyxl, os

v = verify.Verify()    # 对数据库操作的类 对象化
# Create your views here.


def login(request):
    """
    商家登陆界面，判断用户名和密码是否正确
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # password = make_password(password)
        if v.vendor_login(username,password):
            return HttpResponseRedirect('/system/')
        else:
            error_msg = "用户名或密码不正确"
            return render(request, 'login.html', {'error_msg': error_msg})


def predict(request):
    """
    商品销量预测，按照商品名或商品id显示本季度的销量和拟合曲线
    :param request:
    :return:
    """
    # predict_make_pic()
    if request.method == 'GET':
        return render(request, 'predict.html')
    if request.method == 'POST':
        id_or_name = str(request.POST.get('id_or_name'))
        make_predict(id_or_name)
        return render(request, 'predict.html')


def recom(request):
    """
    用户喜好，根据顾客id返回顾客买东西的前六中商品
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'recom.html')
    if request.method == 'POST':
        id = str(request.POST.get('id'))
        x = sort_interest(id)
        print(x)
        make_recom(x)
        return render(request, 'recom.html')


def classgoods(request):
    """
    根据商品种类显示不同商品
    :param request:
    :return:
    """
    if request.method == 'GET':
        datas = v.query_item_info_by_type('当季水果', 2)
        make_classgoods(datas)
        return render(request, 'classgoods.html')
    if request.method == 'POST':
        if 'dangji' in request.POST:
            datas = v.query_item_info_by_type('当季水果',2)
            make_classgoods(datas)
            return render(request, 'classgoods.html')
        elif 'jiangguo' in request.POST:
            datas = v.query_item_info_by_type('浆果类', 2)
            make_classgoods(datas)
            return render(request, 'classgoods.html')
        elif 'guaguo' in request.POST:
            datas = v.query_item_info_by_type('瓜果类', 2)
            make_classgoods(datas)
            return render(request, 'classgoods.html')
        elif 'juguo' in request.POST:
            datas = v.query_item_info_by_type('橘果类', 2)
            make_classgoods(datas)
            return render(request, 'classgoods.html')
        elif 'heguo' in request.POST:
            datas = v.query_item_info_by_type('核果类', 2)
            make_classgoods(datas)
            return render(request, 'classgoods.html')
        elif 'renguo' in request.POST:
            datas = v.query_item_info_by_type('仁果类', 2)
            make_classgoods(datas)
            return render(request, 'classgoods.html')
        else:
            return render(request, 'classgoods.html')


def userreg(request):
    """
    用户注册界面，接收用户的信息
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'userreg.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        pw = request.POST.get('pw')
        repw = request.POST.get('repw')
        name = request.POST.get('name')
        gender = request.POST.get('gender')
        birth = request.POST.get('birth')
        phone = request.POST.get('phone')
        content = request.FILES.get("test", None)
        if birth is None or birth == '':
            birth = '0000-00-00'
        if username != '' and pw != '' and repw != '':
            if pw != repw:
                error_msg = '两次密码不一致'
                return render(request, 'userreg.html', {'error_msg': error_msg})
            temp = v.member_sign_up(str(username), str(pw), str(name), str(birth), str(gender), str(phone))
            if temp == '会员用户名已存在' or (not temp):
                error_msg = "会员用户名已存在或格式不正确"
                return render(request, 'userreg.html', {'error_msg': error_msg})
            elif temp == '顾客信息添加失败':
                error_msg = "顾客信息添加失败"
                return render(request, 'userreg.html', {'error_msg': error_msg})
            else:
                if content is not None:
                    position = os.path.join(r'.\static\customers_pic', temp + '.png')
                    storage = open(position, 'wb')
                    for chunk in content.chunks():
                        storage.write(chunk)
                    storage.close()
                error_msg = "注册成功"
                return render(request, 'userreg.html', {'error_msg': error_msg})
        else:
            error_msg = "格式不正确"
            return render(request, 'userreg.html', {'error_msg': error_msg})


def identify(request):
    """
    商家认证界面，根据licence进行认证
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'identify.html')
    if request.method == 'POST':
        license = request.POST.get('license')
        username = request.POST.get('username')
        password = request.POST.get('password')
        # password = make_password(password)
        if v.vendor_verify(username,password,license) == True:
            return HttpResponseRedirect('/system/')
        elif v.vendor_verify(username, password, license) == 'nolicense':
            error_msg = "商家证书不存在或已被使用"
        elif v.vendor_verify(username, password, license) == 'license':
            error_msg = "商家证书或者用户名错误"
        elif v.vendor_verify(username,password,license) == 'username':
            error_msg = "用户名不能为空或者大于二十位，只能包含'_'"
        elif v.vendor_verify(username, password, license) == 'pw':
            error_msg = "密码不能为空或者大于二十位"
        return render(request, 'identify.html', {'error_msg': error_msg})


def system(request):
    """
    系统主页
    :param request:
    :return:
    """
    return render(request, 'system.html')


def comgoods(request):
    """
    商品信息上传界面
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'comgoods.html')
    if request.method == 'POST':
        id = str(request.POST.get("id"))
        name = str(request.POST.get("name"))
        price = str(request.POST.get("price"))
        type = str(request.POST.get('type'))
        discount = str(request.POST.get("discount"))
        discount_start = str(request.POST.get("discount_start"))
        discount_end = str(request.POST.get("discount_end"))
        kucun = str(request.POST.get('kucun'))
        if kucun != "":
            kucun = int(kucun)
        qudao = str(request.POST.get('qudao'))
        content = request.FILES.get("upload", None)
        if id != '' and price != '':
            if content is not  None:
                position = os.path.join(r'.\static\items_pic', id+'.png')
                storage = open(position, 'wb')
                for chunk in content.chunks():
                    storage.write(chunk)
                storage.close()
            if v.query_item_info(id) != ():
                v.add_item_discount_by_item_id(id, price, discount, discount_start, discount_end, kucun, qudao)
                error_msg = "修改成功"
                return render(request, 'comgoods.html', {'error_msg': error_msg})
            else:
                v.add_item_info(name, price, type, discount, discount_start, discount_end, id, kucun, qudao)
                error_msg = "添加商品成功"
                return render(request, 'comgoods.html', {'error_msg': error_msg})
        else:
            error_msg = "添加失败"
            return render(request, 'comgoods.html', {'error_msg': error_msg})


def cuslist(request):
    """
    列出顾客信息
    :param request:
    :return:
    """
    if request.method == 'GET':
        make_cuslist(v.query_customer_info(''))
        return render(request, 'cuslist.html')
    if request.method == 'POST':
        id_or_name = request.POST.get("id_or_name")
        make_cuslist(v.query_customer_info(str(id_or_name)))
        return render(request, 'cuslist.html')


def cussta(request):
    """
    利用echarts显示会员注册的按时间注册的图表，年龄分布，性别比例
    :param request:
    :return:
    """
    make_cussta(v.query_customer_info(''))
    return render(request, 'cussta.html')


def goodlist(request):
    """
    列出商品优惠信息，可根据id删除商品优惠信息，查询商品优惠信息
    :param request:
    :return:
    """
    if request.method == 'GET':
        make_goodlist(v.query_item_discount())
        return render(request, 'goodlist.html')
    if request.method == 'POST':
        if 'search' in request.POST:
            id_or_name = request.POST.get("id_or_name")
            make_goodlist(v.query_item_info(str(id_or_name)))
            return render(request, 'goodlist.html')
        if 'delete' in request.POST:
            id = request.POST.get("id")
            v.delete_item_discount_by_item_id(str(id))
            make_goodlist(v.query_item_info(""))
            return render(request, 'goodlist.html')


def tralist(request):
    """
    列出订单信息，可根据顾客id或者订单id进行查询
    :param request:
    :return:
    """
    if request.method == 'GET':
        make_tralist(v.query_order_by_id(''))
        return render(request, 'tralist.html')
    if request.method == 'POST':
        id = request.POST.get("id")
        make_tralist(v.query_order_by_id(id))
        return render(request, 'tralist.html')


def uptrade(request):
    """
    上传订单界面
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'uptrade.html')
    if request.method == 'POST':
        content = request.FILES.get("upload", None)
        if content is not None:
            position = os.path.join(r'.\static\temp', content.name)
            storage = open(position, 'wb')
            for chunk in content.chunks():
                storage.write(chunk)
            storage.close()
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
            return render(request, 'uptrade.html', {'error_msg': error_msg})
        else:
            error_msg = "添加商品失败"
            return render(request, 'uptrade.html', {'error_msg': error_msg})


def make_cussta(datas):
    """
    动态更新会员的按时间注册的图标、性别比例、年龄分布界面
    :param datas:
    :return:
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
        # try:
        if data[2] is not None:
            s = str(data[2])
        else:
            s = '0000-00-00'
        s = s.replace('-', '')
        # print(s)
        s = s[:4]
        print('----\n',s,type(s))
        if s is None or s == '' or s == ' None':
            print('这里走了吗')
            s = 0
        s = int(s)
        # print(s)
        dy = a[0] - s
        birth = int(dy)
        # t = str(data[5])
        # t = t.replace('-','')
        # t = int(t[4:6])
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
        # except:
        #     pass
        # try:
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


def make_goodlist(datas):
    """
    动态更新商品列表
    :param datas:
    :return:
    """
    begin = '''
    <!DOCTYPE html>
<html lang="ch">
<head>
	<link rel="stylesheet" type="text/css" href="/static/css/common.css"/>
	
	<meta charset="UTF-8">
	<title>优惠商品信息</title>

</head>
<body>
<form action=" " method="POST">	
<div id="top">
			<div class="top">
				<div class="logo">
					<a href="/system/"><img src="/static/img/logo.png"/></a>
				</div>
				
			</div>
		</div>

	<div>
	<div class="delete1">
			<input type="text" class="text" name="id"  placeholder="请输入商品ID进行删除" />
			<input type="submit" class="delete_l" value="删除" name="delete">
			
			<!-- <input type="text" class="text" name="" id="" value="搜索" onfocus="if (value =='搜索'){value =''}" onblur="if (value ==''){value='搜索'}" /> -->
			<!-- <input type="button" class="button" name="" id="" value="" /> -->
		</div>
		<div class="search">
			<input type="text" class="text" name="id_or_name"  placeholder="请输入商品ID或商品名" />
			<input type="submit" class="search_l" value="搜索" name="search">
			
			<!-- <input type="text" class="text" name="" id="" value="搜索" onfocus="if (value =='搜索'){value =''}" onblur="if (value ==''){value='搜索'}" /> -->
			<!-- <input type="button" class="button" name="" id="" value="" /> -->
		</div>
		<div class="list_cha">
		<table width="720px" border="0" class="stripe" cellpadding="0" cellspacing="0"> 
						<tr> 
							<td width="140px" style="text-align: center;">商品照片</td> 
							<td width="160px" style="text-align: center;">商品ID</td> 
							<td width="140px" style="text-align: center;">商品名称</td> 
							<td width="100px" style="text-align: center;">现价</td>	
							<td width="120px" style="text-align: center;">优惠信息</td>
							<td width="200px" style="text-align: center;">优惠区间</td> 						
						</tr>
    '''
    end = '''
    </table> 
					</table> 
					</div>
	</div>
	</form>
</body>
</html>
    '''
    f = open('./templates/goodlist.html', 'w', encoding='utf8')
    f.write(begin)
    for data in datas:
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
        f.write("<tr>\n")
        if os.path.exists(r'.\static\items_pic\%s.png'%data[0]):
            f.write('<td width="140px">\n<img src="/static/items_pic/%s.png" width="100px" height="100px">\n</td> \n'%data[0])
        else:
            f.write('<td width="140px">\n<img src="/static/img/milk.png" width="100px" height="100px">\n</td> \n')
        f.write('<td width="160px" style="text-align: center;">%s</td> \n' % data[0])
        f.write('<td width="140px" style="text-align: center;">%s</td>\n' % data[1])
        f.write('<td width="100px" style="text-align: center;">%s</td>\n' % data[2])
        f.write('<td width="120px" style="text-align: center;">%s</td>\n' % discount)
        f.write('<td width="200px" style="text-align: center;">%s</td>\n' % discount_time)
        # f.write('<td width="110px" >\n<input type="submit" value="%s" name="del">\n</td> '%data[0])
        # f.write('<td width="170px" style="text-align: center;">%s</td>\n' % data[6])
        # f.write('<td width="140px" style="text-align: center;">%s</td>\n' % data[7])
        f.write("</tr>\n")
    f.write(end)
    f.close()


def make_tralist(datas):
    """
    动态更新订单列表
    :param datas:
    :return:
    """
    begin = '''
    <!DOCTYPE html>
<html lang="ch">
<head>
	<link rel="stylesheet" type="text/css" href="/static/css/common.css"/>
	
	<meta charset="UTF-8">
	<title>订单列表信息</title>

</head>
<body>
<div id="top">
			<div class="top">
				<div class="logo">
					<a href="/system/"><img src="/static/img/logo.png"/></a>
				</div>
				
			</div>
		</div>

	<div>
		<div class="search">
			<form action=" " method="post">	
			<input type="text" class="text"  placeholder="请输入订单ID或会员ID" name="id" />
			<input type="submit" class="search_l" value="搜索">
			</form>
			<!-- <input type="text" class="text" name="" id="" value="搜索" onfocus="if (value =='搜索'){value =''}" onblur="if (value ==''){value='搜索'}" /> -->
			<!-- <input type="button" class="button" name="" id="" value="" /> -->
		</div>
		<div class="list_cha">
		<table width="830px" border="0" class="stripe" cellpadding="0" cellspacing="0"> 
						<tr> 
							<td width="150px" style="text-align: center;">订单号</td> 
							<td width="140px" style="text-align: center;">顾客ID</td> 	
							<td width="120px" style="text-align: center;">顾客姓名</td>
							<td width="110px" style="text-align: center;">订单总价</td>
							<td width="170px" style="text-align: center;">订单时间</td> 						
							<td width="140px" style="text-align: center;">提交人</td>
						</tr>
    '''
    end = '''
    </table> 
					</div>
	</div>
</body>
</html>
    '''
    f = open('./templates/tralist.html', 'w', encoding='utf8')
    f.write(begin)
    for data in datas:
        try:
            name = v.query_customer_info(data[1])
            name = name[0][1]
        except:
            name = '-'
        f.write("<tr>\n")
        f.write('<td width="150px" style="text-align: center;">%s</td>\n' % data[0])
        f.write('<td width="140px" style="text-align: center;">%s</td>\n' % data[1])
        f.write('<td width="120px" style="text-align: center;">%s</td>\n' % name)
        f.write('<td width="110px" style="text-align: center;">%s</td>\n' % data[5])
        f.write('<td width="170px" style="text-align: center;">%s</td>\n' % data[6])
        f.write('<td width="140px" style="text-align: center;">%s</td>\n' % data[7])
        f.write("</tr>\n")
    f.write(end)
    f.close()


def make_cuslist(datas):
    """
    动态更新顾客列表
    :param datas:
    :return:
    """
    begin = '''
     <!DOCTYPE html>
<html lang="ch">
<head>
	<link rel="stylesheet" type="text/css" href="/static/css/common.css"/>
	
	<meta charset="UTF-8">
	<title>会员列表信息</title>

</head>
<body>
<div id="top">
			<div class="top">
				<div class="logo">
					<a href="/system/"><img src="/static/img/logo.png"/></a>
				</div>
				
			</div>
		</div>

	<div>
		<div class="search">
			<form action=" " method="POST">	
			<input type="text" class="text"  placeholder="请输入ID或会员名" name="id_or_name" />
			<input type="submit" class="search_l" value="搜索">
			</form>
			<!-- <input type="text" class="text" name="" id="" value="搜索" onfocus="if (value =='搜索'){value =''}" onblur="if (value ==''){value='搜索'}" /> -->
			<!-- <input type="button" class="button" name="" id="" value="" /> -->
		</div>
		<div class="list_cha">
		<table width="915px" border="0" class="stripe" cellpadding="0" cellspacing="0"> 
						<tr> 
							<td width="100px" style="text-align: center;">头像</td> 
							<td width="140px" style="text-align: center;">会员ID</td> 
							<td width="140px" style="text-align: center;">会员姓名</td> 	
							<td width="120px" style="text-align: center;">会员性别</td>
							<td width="110px" style="text-align: center;">年龄</td>
							<td width="170px" style="text-align: center;">联系方式</td> 						
							<td width="140px" style="text-align: center;">注册时间</td>
						</tr>
    '''
    end = '''
    </table> 
					</div>
	</div>
</body>
</html>
    '''
    f = open('./templates/cuslist.html', 'w', encoding='utf8')
    f.write(begin)
    for data in datas:
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

        f.write("<tr>\n")
        if os.path.exists(r'.\static\customers_pic\%s.png' % data[0]):
            f.write('<td width="100px">\n<img src="/static/customers_pic/%s.png" width="100px" height="100px">\n</td> \n'%data[0])
        else:
            f.write('<td width="100px">\n<img src="/static/img/face.png" width="100px" height="100px">\n</td> \n')
        # f.write('<td width="100px">\n<img src="/static/img/face.png" width="100px" height="100px">\n</td> \n' )
        f.write('<td width="140px" style="text-align: center;">%s</td>\n' % data[0])
        f.write('<td width="140px" style="text-align: center;">%s</td>\n' % name)
        f.write('<td width="120px" style="text-align: center;">%s</td>\n' % gender)
        f.write('<td width="110px" style="text-align: center;">%s</td>\n' % birth)
        f.write('<td width="170px" style="text-align: center;">%s</td>\n' % phone)
        f.write('<td width="140px" style="text-align: center;">%s</td>\n' % data[5])
        f.write("</tr>\n")
    f.write(end)
    f.close()


def make_classgoods(datas):
    """
    按类别动态更新商品信息
    :param datas:
    :return:
    """
    begin = '''
    <!DOCTYPE html>
<html lang="ch">
<head>
	<meta charset="UTF-8">
	<title>商品分类</title>
	<link rel="stylesheet" type="text/css" href="/static/css/classgoods.css"/>
	<link rel="stylesheet" type="text/css" href="/static/css/common.css"/>
</head>
<body>
    <div id="top">
		<div class="top">
			<div class="logo">
				<a href="/system/"><img src="/static/img/logo.png"/></a>
			</div>
			
		</div>

	</div>
	<div class="dropdown" >
	  <button class="dropbtn">水果分类</button>
	  <div class="dropdown-content" style="left:0;">
	  <form action=" " method="POST">	
	    <!-- <a href="food1.html">生鲜水果</a> -->
	    <input type="submit" name='dangji' class="input1" value='当季水果'><br>
	    <!-- <a href="classgoods.html">酒水乳饮 </a> -->
	    <input type="submit" name='jiangguo' class="input1" value='浆果类'><br>
	    <!-- <a href="food2.html">零食副食</a> -->
	    <input type="submit" name='guaguo' class="input1" value='瓜果类'><br>
	    <input type="submit" name='juguo' class="input1" value='橘果类'><br>
	    <input type="submit" name='heguo' class="input1" value='核果类'><br>
	    <input type="submit" name='renguo' class="input1" value='仁果类'><br>
	    </form>
	  </div>
    </div>

    <div class="list_cha">
		<table width="780px" border="0" class="stripe" cellpadding="0" cellspacing="0">
						<tr> 
							<td width="100px" style="text-align: center;">商品照片</td> 
							<td width="200px" style="text-align: center;">商品类别</td> 
							<td width="140px" style="text-align: center;">商品名称</td> 	
							<td width="120px" style="text-align: center;">商品单价</td>
							<!-- <td width="140px" style="text-align: center;">商品销量</td> 	 -->					
							<td width="110px" style="text-align: center;">商品库存</td>
							<td width="110px" style="text-align: center;">进货渠道</td>
						</tr>    
    '''
    end = '''
   </div>
	</div>
</body>
</html>
    '''
    f = open('./templates/classgoods.html', 'w', encoding='utf8')
    f.write(begin)
    for data in datas:

        f.write("<tr>\n")
        if os.path.exists(r'.\static\items_pic\%s.png'%data[0]):
            f.write('<td width="140px">\n<img src="/static/items_pic/%s.png" width="100px" height="100px">\n</td> \n'%data[0])
        else:
            f.write('<td width="140px">\n<img src="/static/img/milk.png" width="100px" height="100px">\n</td> \n')
        f.write('<td width="200px" style="text-align: center;">%s</td> \n' % data[3])
        f.write('<td width="140px" style="text-align: center;">%s</td> \n' % data[1])
        f.write('<td width="120px" style="text-align: center;">%s</td>\n' % data[2])
        f.write('<td width="110px" style="text-align: center;">%s</td> \n' % data[7])
        f.write('<td width="110px" >%s</td> \n' % data[8])
        f.write("</tr>\n")
    f.write(end)
    f.close()


def make_recom(datas):
    """
    动态更新顾客喜好
    :param datas:
    :return:
    """
    begin = '''
    <!DOCTYPE html>
<html lang="ch">
<head>
	<meta charset="UTF-8">
	<link rel="stylesheet" type="text/css" href="/static/css/common.css"/>
	<title>用户喜好</title>
</head>
<body>
	<div id="top">
			<div class="top">
				<div class="logo">
					<a href="/system/"><img src="/static/img/logo.png"/></a>
				</div>
			</div>
		</div>
		<div class="search">
		<form action=" " method="post">	
			<input type="text" class="text" name="id" id="" placeholder="请输入顾客ID" />
			<input type="submit" class="search_l" value="搜索">
		</form>
		</div>
	<div class="list_cha">
		<table width="915px" border="0" class="stripe" cellpadding="0" cellspacing="0"> 
						<tr> 
							<td width="305px" style="text-align: center;">会员ID</td> 	
							<td width="305px" style="text-align: center;">商品ID</td>
                            <td width="305px" style="text-align: center;">商品名</td>
							<td width="304px" style="text-align: center;">次数</td>
						</tr>  
    '''
    end = '''
  </table> 
	</div>
</body>
</html>
    '''
    f = open('./templates/recom.html', 'w', encoding='utf8')
    f.write(begin)
    for data in datas:
        x = v.query_item_info(data[1])
        print(x)
        f.write("<tr>\n")
        f.write('<td width="305px" style="text-align: center;">%s</td> \n' % data[0])
        f.write('<td width="305px" style="text-align: center;">%s</td> \n' % data[1])
        f.write('<td width="305px" style="text-align: center;">%s</td>\n' % x[0][1])
        f.write('<td width="304px" style="text-align: center;">%s</td> \n' % data[2])
        f.write("</tr>\n")
    f.write(end)
    f.close()


def make_predict(data):
    """
    动态更新商品销量和商品预测
    :param data:
    :return:
    """
    begin = '''
     <!DOCTYPE html>
<html lang="ch">
<head>
	<meta charset="UTF-8">
	<title>商品分类</title>
	<link rel="stylesheet" type="text/css" href="/static/css/classgoods.css"/>
	<link rel="stylesheet" type="text/css" href="/static/css/common.css"/>
</head>
<body>
    <div id="top">
		<div class="top">
			<div class="logo">
				<a href="/system/"><img src="/static/img/logo.png"/></a>
			</div>
		</div>
	</div>
    <div class="search">
			<form action=" " method="post">
			<input type="text" class="text"  placeholder="请输入商品ID或商品名" name="id_or_name" />
			<input type="submit" class="search_l" value="搜索">
			</form>
			<!-- <input type="text" class="text" name="" id="" value="搜索" onfocus="if (value =='搜索'){value =''}" onblur="if (value ==''){value='搜索'}" /> -->
			<!-- <input type="button" class="button" name="" id="" value="" /> -->
    </div>
    '''
    end = '''
  </body>
    '''
    f = open('./templates/predict.html', 'w', encoding='utf8')
    f.write(begin)
    f.write('<div style="width:750px; margin:auto">\n<img src="/static/predict/%s.png" style="margin: auto">\n</div>' % data)
    f.write(end)
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


# 本函数过于复杂，没有写出来
# def predict_make_pic():
#     """
#     商品销量，和商品预测产生并保存图片
#     :return:
#     """
#     # 待拟合的数据
#     X = np.array([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30])
#     Y=np.array([94.8,20,29.5,47,62,18.3,29.1,90,10,59,76,89,79,98,69,109,105,110,99,96,123,65,45,67,34,45,67,86,54,36])
#     # Y=np.array([34.8,42.6,54.3,46.7,56.6,60.1,45.6,69.8,78.8,89.7,98.8,120.5,100.6,86.5,66.3,70.8,45.6,34.6,25.4,30.2,43.2,20.7,16.8,22.5,45.6,34.6,24.6,21.1,22.2,15.6])
#
#     print(len(X))
#     print(len(Y))
#     # 二次函数的标准形式
#     def func(params, x):
#         a, b, c = params
#         return a * x * x + b * x + c
#
#
#     # 误差函数，即拟合曲线所求的值与实际值的差
#     def error(params, x, y):
#         return func(params, x) - y
#
#
#     # 对参数求解
#     def slovePara():
#         p0 = [10, 10, 10]
#         Para = leastsq(error, p0, args=(X, Y))
#         return Para
#
#
#     # 输出最后的结果
#     def solution():
#         Para = slovePara()
#         a, b, c = Para[0]
#         print ("a=",a," b=",b," c=",c)
#         print ("cost:" + str(Para[1]))
#         print ("求解的曲线是:")
#         print("y="+str(round(a,2))+"x*x+"+str(round(b,2))+"x+"+str(c))
#
#         plt.figure(figsize=(8,6))
#         pylab.plot(X, Y, 'gv--', label="Sales Volume", linewidth=1.5)
#
#         #   画拟合直线
#         x=np.linspace(0,35,100) ##在0-15直接画100个连续点
#         y=a*x*x+b*x+c ##函数式
#         plt.plot(x,y,color="red",label="Fitting Result",linewidth=2)
#         plt.legend() #绘制图例
#         pylab.savefig(f"D:/1.png",dpi=96)
#         plt.show()
#
#     solution()
