import MySQLdb, time, random

USERNAME = ""   # 请设置数据库的用户名
PSW = ""    # 请设置数据库的密码

class Db:
	'''
	该类主要是对MySQL数据库操作。
	属性：
		db: MySQLdb 
		cursor: db.cursor()
		database_name: str, 数据库名字
	方法：
		__init__: no return
		__del__: no return
	'''
	def __init__(self):
		'''
		连接到MySQL，创建数据库，可自定义数据库名称
		'''
		self.__connect()
		self.__create_database('Swoosh')	# 在这里命名数据库
		self.db.select_db(self.database_name)
		self.__create_table_vendor_login()
		self.__create_table_member_login()
		self.__create_table_customers_info()
		self.__create_table_items_info()
		self.__create_table_order()
		self.__create_table_LICENSES()

	def __del__(self):
		'''
		关闭数据库和corsor
		'''
		self.cursor.close()
		self.db.close()

	def __connect(self):
		'''
		连接到MySQL
		'''
		try:
			self.db = MySQLdb.connect("localhost", USERNAME, PSW, use_unicode=True, charset="utf8")
			self.cursor = self.db.cursor()
		except:
			print('用户名或密码不正确')

	def __create_database(self, database_name):
		'''
		创建数据库
		'''
		sql='''
		create database %s default charset=utf8
		'''%database_name
		self.database_name = database_name
		try:
			self.cursor.execute(sql)
		except:
			# print("数据库%s已经存在"%database_name)
			pass

	def __create_table_order(self):
		'''
		创建数据表，名称为 交易记录
		'''
		sql = '''
		create table 交易记录(
		order_id char(15),
		customer_id char(7) NOT NULL,
		items_id varchar(820) NOT NULL,
		items_single_price varchar(340) NOT NULL,
		items_number varchar(180) NOT NULL,
		total_price varchar(7) NOT NULL,
		time datetime NOT NULL,
		submitter varchar(30) NOT NULL,
		PRIMARY KEY(order_id)
		)default charset=utf8
		'''
		try:
			self.cursor.execute(sql)
		except:
			# print("'交易记录'表已经存在了")
			pass

	def __create_table_items_info(self):
		'''
		创建数据表，名称为 商品信息
		'''
		sql = '''
		create table 商品信息(
		item_id varchar(20),
		item_name varchar(30) NOT NULL,
		item_price varchar(8) NOT NULL,
		item_type varchar(65) NOT NULL,
		discount varchar(30),
		discount_start_time date,
		discount_end_time date,
		kucun int NOT NULL,
		qudao varchar(90) NOT NULL,
		PRIMARY KEY(item_id)
		)default charset=utf8
		'''
		try:
			self.cursor.execute(sql)
		except:
			# print("'商品信息'表已经存在了")	
			pass

	def __create_table_customers_info(self):
		'''
		创建数据表，名称为 顾客信息
		'''
		sql = '''
		create table 顾客信息(
		customer_id char(7),
		customer_name varchar(30),
		customer_birthday date,
		customer_gender char(3),
		customer_phone char(11),
		reg_time datetime NOT NULL,
		is_member char(1) NOT NULL,
		PRIMARY KEY(customer_id)
		)default charset=utf8
		'''
		try:
			self.cursor.execute(sql)
		except:
			# print("'顾客信息'表已经存在了")	
			pass

	def __create_table_member_login(self):
		'''
		创建数据表，名称为 会员登录
		'''
		sql = '''
		create table 会员登录(
		member_name varchar(20),
		member_pw varchar(20) NOT NULL,
		customer_id varchar(7) NOT NULL,
		PRIMARY KEY(member_name)
		)default charset=utf8
		'''
		try:
			self.cursor.execute(sql)
		except:
			# print("'会员登录'表已经存在了")
			pass

	def __create_table_vendor_login(self):
		'''
		创建数据表，名称为 商家登陆
		'''
		sql = '''
		create table 商家登录(
		vendor_name varchar(20),
		vendor_pw varchar(20) NOT NULL,
		PRIMARY KEY(vendor_name)
		)default charset=utf8
		'''
		try:
			self.cursor.execute(sql)
		except:
			# print("'LICENSES'表已经存在了")
			pass

	def __create_table_LICENSES(self):
		'''
		创建数据表，名称为 LICENSES
		'''
		sql = '''
		create table LICENSES(
		licenses char(20),
		vendor_name varchar(20),
		PRIMARY KEY(licenses)
		)default charset=utf8
		'''
		try:
			self.cursor.execute(sql)
		except:
			# print("'商家登录'表已经存在了")
			pass

	def __query_license_if_exists(self, li):
		'''
		查询LICENSES并返回是否存在
		'''
		sql = '''
		select licenses, vendor_name from LICENSES
		'''
		self.cursor.execute(sql)
		for (license,vendor_name) in self.cursor.fetchall():
			if li == license and (vendor_name == '' or vendor_name == None):
				return True
		return False

	def __get_time(self):
		'''
		返回时间，按照特定格式格式
		'''
		dt = time.localtime()
		return time.strftime("%Y-%m-%d %H:%M:%S",dt)

	def __create_customer_id(self):
		'''
		随机产生 客户ID
		'''
		sql = '''
		select customer_id from 顾客信息 
		'''
		self.cursor.execute(sql)
		temp = self.cursor.fetchall()
		x = 0
		while True:
			id = str(random.randrange(1000000,9999999))
			for t in temp:
				if t == id:
					x += 1
			if x == 0:
				return id
			x = 0

	def __create_order_id(self,customer_id):
		'''
		根据 客户ID 产生 订单ID
		'''
		dt = time.localtime()
		ti = time.strftime("%Y%m%d",dt)
		ti = ti[2:]
		sql = '''
		select order_id from 交易记录 
		'''
		self.cursor.execute(sql)
		temp = self.cursor.fetchall()
		x = 0
		while True:
			two = random.randrange(10,99)
			id = customer_id + str(two) + ti
			for t in temp:
				if t == id:
					x += 1
			if x == 0:
				return id
			x = 0

	def __add_LICENSES_vendor_name(self, license, vendor_name):
		'''
		在LICNESES表中添加商家用户名
		'''
		sql = '''
		update LICENSES set vendor_name='%s' where (licenses = '%s')
		'''%(vendor_name, license)
		self.cursor.execute(sql)
		self.db.commit()

	def __if_vendor_exists(self, vendor_name):
		'''
		
		'''
		sql = '''
		select * from 商家登录 where vendor_name='%s'
		'''%vendor_name
		self.cursor.execute(sql)
		return self.cursor.fetchall()

	def __if_member_exists(self, member_name):
		sql = '''
		select member_name,member_pw from 会员登录 where member_name='%s'
		'''%member_name
		self.cursor.execute(sql)
		return self.cursor.fetchall()

	def create_item_id(self):
		'''
		创建商品ID
		'''
		sql = '''
		select item_id from 商品信息 
		'''
		self.cursor.execute(sql)
		temp = self.cursor.fetchall()
		x = 0
		while True:
			id = str(random.randrange(10000000,99999999999999999999))
			for t in temp:
				if t == id:
					x += 1
			if x == 0:
				return id
			x = 0

	def add_vendor_login(self, vendor_name, vendor_pw, li):
		'''
		在有 LICENSE 时，可添加商家用户名、密码
		'''
		if not self.__query_license_if_exists(li):
			raise Exception('LICENSE 不存在或已被使用')
		else:
			sql = '''
			insert into 商家登录(vendor_name,vendor_pw) values('%s','%s')
			'''%(vendor_name, vendor_pw)
			try:
				self.cursor.execute(sql)
				self.db.commit()
				self.__add_LICENSES_vendor_name(li, vendor_name)
			except:
				raise Exception('商家用户名已存在')

	def add_member_login(self, member_name, member_pw, customer_id):
		'''
		会员注册
		'''
		sql = '''
		insert into 会员登录(member_name, member_pw, customer_id) values('%s', '%s', '%s')
		'''%(member_name, member_pw, customer_id)
		try:
			self.cursor.execute(sql)
			self.db.commit()
		except:
			raise Exception('会员用户名已存在')

	def add_customer_info(self, customer_name,customer_birthday,customer_gender,customer_phone,is_member):
		'''
		注册顾客信息
		'''
		customer_id = self.__create_customer_id()
		sql = '''
		insert into 顾客信息(customer_id,customer_name,customer_birthday,customer_gender,customer_phone,reg_time,is_member) values('%s','%s',str_to_date(\'%s\','%%Y-%%m-%%d'),'%s','%s',str_to_date(\'%s\','%%Y-%%m-%%d %%H:%%i:%%s'),'%s')
		'''%(customer_id,customer_name,customer_birthday,customer_gender,customer_phone,self.__get_time(),is_member)
		try:
			self.cursor.execute(sql)
			self.db.commit()
			return customer_id
		except:
			raise Exception('顾客信息添加失败')

	def add_item_info(self,item_id,item_name,item_price,item_type, discount,discount_start_time,discount_end_time,kucun,qudao):
		'''
		添加商品信息
		'''
		item_type = item_type.replace('，',',')
		sql = '''
		insert into 商品信息 (item_id,item_name,item_price,item_type,discount,discount_start_time,discount_end_time,kucun,qudao) values('%s','%s','%s','%s','%s',str_to_date(\'%s\','%%Y-%%m-%%d'),str_to_date(\'%s\','%%Y-%%m-%%d'),'%d','%s')
		'''%(item_id,item_name,item_price,item_type,discount,discount_start_time,discount_end_time,kucun,qudao)
		try:
			self.cursor.execute(sql)
			self.db.commit()
		except:
			raise Exception('商品信息添加失败')

	def add_item_discount_by_item_id(self, item_id, price, discount,discount_start_time,discount_end_time,kucun,qudao):
		'''
		添加商品优惠，根据商品ID
		'''
		sql = '''
		update 商品信息 set item_price='%s',discount='%s',discount_start_time=str_to_date(\'%s\','%%Y-%%m-%%d'),discount_end_time=str_to_date(\'%s\','%%Y-%%m-%%d'),kucun='%d',qudao='%s' where item_id='%s'
		'''%(price,discount,discount_start_time,discount_end_time,kucun,qudao,item_id)
		self.cursor.execute(sql)
		self.db.commit()

	def update_kucun(self, item_id, number):
		s = '''
		select kucun from 商品信息 where item_id='%s'
		'''%(item_id)
		self.cursor.execute(s)
		kucun = self.cursor.fetchall()
		# print(kucun)
		kucun = int(kucun[0][0]) - int(number)
		sql = '''
		update 商品信息 set kucun='%d' where item_id='%s'
		'''%(kucun,item_id)
		self.cursor.execute(sql)
		self.db.commit()

	def add_order(self,customer_id,items_id,items_single_price,items_number,total_price,submitter):
		'''
		添加交易记录
		'''
		items_id = items_id.replace('，',',')
		items_single_price = items_single_price.replace('，',',')
		items_number = items_number.replace('，',',')
		order_id = self.__create_order_id(customer_id)
		sql = '''
		insert into 交易记录(order_id,customer_id,items_id,items_single_price,items_number,total_price,time,submitter) values('%s','%s','%s','%s','%s','%s',str_to_date(\'%s\','%%Y-%%m-%%d %%H:%%i:%%s'),'%s')
		'''%(order_id,customer_id,items_id,items_single_price,items_number,total_price,self.__get_time(),submitter)
		try:
			self.cursor.execute(sql)
			self.db.commit()
			return order_id
		except:
			raise Exception('交易记录添加失败')

	def query_vendor_login(self, vendor_name, vendor_pw):
		'''
		查询商家登录信息是否存在
		'''
		sql = '''
		select * from 商家登录
		'''
		self.cursor.execute(sql)
		for (vn,vp) in self.cursor.fetchall():
			if vn == vendor_name and vp == vendor_pw:
				return True
		return False

	def query_member_login(self,member_name, member_pw):
		'''
		查询会员是否正确
		'''
		sql = '''
		select * from 会员登录
		'''
		self.cursor.execute(sql)
		for (mn,mp,mi) in self.cursor.fetchall():
			if mn == member_name and mp == member_pw:
				return mi
		return False


	def query_member_if_exists(self, member_name):
		'''
		查询会员是否存在
		'''
		sql = '''
		select * from 会员登录
		'''
		self.cursor.execute(sql)
		for (mn, mp, mi) in self.cursor.fetchall():
			if mn == member_name:
				return True
		return False

	def query_customer_info_by_id(self, id):
		'''
		根据顾客ID，查询顾客信息
		'''
		sql = '''
		select * from 顾客信息 where customer_id like '%{}%'
		'''.format(id)
		self.cursor.execute(sql)
		return self.cursor.fetchall()

	def __query_customer_info_by_whole_id(self, id):
		'''
		根据顾客ID，查询顾客信息
		'''
		sql = '''
		select * from 顾客信息 where customer_id = '%s'
		'''%id
		self.cursor.execute(sql)
		return self.cursor.fetchall()

	def query_customer_info_by_name(self, name):
		'''
		根据顾客姓名查询顾客信息
		'''
		sql = '''
		select * from 顾客信息 where customer_name like '%{}%'
		'''.format(name)
		self.cursor.execute(sql)
		return self.cursor.fetchall()

	def query_item_info_by_id(self, id):
		'''
		根据商品ID查询商品信息
		'''
		sql = '''
		select * from 商品信息 where item_id like '%{}%'
		'''.format(id)
		self.cursor.execute(sql)
		return self.cursor.fetchall()

	def __query_item_info_by_whole_id(self, id):
		'''
		根据商品ID查询商品信息
		'''
		sql = '''
		select * from 商品信息 where item_id = '%s'
		'''%(id)
		self.cursor.execute(sql)
		return self.cursor.fetchall()

	def query_item_info_by_name(self, name):
		'''
		根据商品姓名查询商品信息
		'''
		sql = '''
		select * from 商品信息 where item_name like '%{}%'
		'''.format(name)
		self.cursor.execute(sql)
		return self.cursor.fetchall()

	def __query_item_info_by_whole_name(self, name):
		'''
		根据商品姓名查询商品信息
		'''
		sql = '''
		select * from 商品信息 where item_name like '%s'
		'''%(name)
		self.cursor.execute(sql)
		return self.cursor.fetchall()

	def query_item_info_by_type1(self, type):
		'''
		根据商品分类1查询商品信息
		'''
		sql = '''
		select * from 商品信息 where item_type like '{},%'
		'''.format(type)
		self.cursor.execute(sql)
		return self.cursor.fetchall()

	def query_item_info_by_type2(self, type):
		'''
		根据商品分类2查询商品信息
		'''
		sql = '''
		select * from 商品信息 where item_type like '%,{}'
		'''.format(type)
		self.cursor.execute(sql)
		return self.cursor.fetchall()

	def query_item_info_by_type3(self, type):
		'''
		根据商品分类3查询商品信息
		'''
		sql = '''
		select * from 商品信息 where item_type like '%,{}'
		'''.format(type)
		self.cursor.execute(sql)
		return self.cursor.fetchall()

	def query_item_discount(self):
		'''
		查询商品优惠
		'''
		sql = '''
		select * from 商品信息 where ((discount is not null) and discount != '')
		'''
		self.cursor.execute(sql)
		return self.cursor.fetchall()

	def query_order_by_order_id(self, order_id):
		'''
		根据订单ID查询交易记录
		'''
		sql = '''
		select * from 交易记录 where order_id like '%{}%'
		'''.format(order_id)
		self.cursor.execute(sql)
		return self.cursor.fetchall()

	def query_order_by_customer_id(self, customer_id):
		'''
		根据顾客ID查询交易记录
		'''
		sql = '''
		select * from 交易记录 where customer_id like '%{}%'
		'''.format(customer_id)
		self.cursor.execute(sql)
		return self.cursor.fetchall()

	# def query_order_by_customer_name(self, customer_name):
	# 	sql = '''
	# 	select * from 交易记录 where customer_name = '%s'
	# 	'''%customer_name
	# 	self.cursor.execute(sql)
	# 	return self.cursor.fetchall()

	def query_order_by_time(self,time):
		'''
		查询订单，根据订单时间
		'''
		sql = '''
		select * from 交易记录 where time like  '{}%'
		'''.format(time)
		self.cursor.execute(sql)
		return self.cursor.fetchall()

	def delete_item_info_by_item_id(self, item_id):
		'''
		根据商品ID删除商品信息
		'''
		sql = '''
		delete from 商品信息 where item_id = %s
		'''%item_id
		if self.__query_item_info_by_whole_id(item_id) == ():
			raise Exception('该商品不存在，无法删除')
		self.cursor.execute(sql)
		self.db.commit()

	def delete_item_info_by_item_name(self, item_name):
		'''
		根据商品名称删除商品信息
		'''
		sql = '''
		delete from 商品信息 where item_name = '%s'
		'''%item_name
		if self.__query_item_info_by_whole_name(item_name) == ():
			raise Exception('该商品不存在，无法删除')
		self.cursor.execute(sql)
		self.db.commit()

	def delete_item_discount_by_item_id(self, item_id):
		'''
		删除商品优惠，根据商品ID
		'''
		sql = '''
		update 商品信息 set discount='',discount_start_time='0000-00-00',discount_end_time='0000-00-00' where item_id='%s'
		'''%(item_id)
		self.cursor.execute(sql)
		self.db.commit()

	def update_vendor_pw(self, vendor_name, vendor_pre_pw, vendor_pw):
		'''
		根据商家用户名和密码，修改密码
		'''
		sql = '''
		update 商家登录 set vendor_pw='%s' where vendor_name='%s'
		'''%(vendor_pw,vendor_name)
		for (a,b) in self.__if_vendor_exists(vendor_name):
			if a==vendor_name and b==vendor_pre_pw:
				self.cursor.execute(sql)
				self.db.commit()
				return
		raise Exception('用户名或密码不正确')

	def update_member_pw(self, member_name, member_pre_pw, member_pw):
		'''
		根据会员用户名和密码，修改会员密码
		'''
		sql = '''
		update 会员登录 set member_pw='%s' where member_name='%s'
		'''%(member_pw,member_name)
		for (a,b) in self.__if_member_exists(member_name):
			if a==member_name and b==member_pre_pw:
				self.cursor.execute(sql)
				self.db.commit()
				return
		raise Exception('用户名或密码不正确')

	def update_customer_name(self, customer_id, customer_name):
		'''
		根据顾客ID修改顾客姓名
		'''
		sql = '''
		update 顾客信息 set customer_name='%s' where customer_id='%s' 
		'''%(customer_name,customer_id)
		if self.__query_customer_info_by_whole_id(customer_id) == ():
			raise Exception('用户不存在')
		self.cursor.execute(sql)
		self.db.commit()

	def update_customer_birthday(self, customer_id, customer_birthday):
		'''
		根据顾客ID修改顾客出生日期
		'''
		sql = '''
		update 顾客信息 set customer_birthday=str_to_date(\'%s\','%%Y-%%m-%%d') where customer_id='%s' 
		'''%(customer_birthday,customer_id)
		if self.__query_customer_info_by_whole_id(customer_id) == ():
			raise Exception('用户不存在')
		self.cursor.execute(sql)
		self.db.commit()

	def update_customer_gender(self, customer_id, customer_gender):
		'''
		根据顾客ID修改顾客性别
		'''
		sql = '''
		update 顾客信息 set customer_gender='%s' where customer_id='%s' 
		'''%(customer_gender,customer_id)
		if self.__query_customer_info_by_whole_id(customer_id) == ():
			raise Exception('用户不存在')
		self.cursor.execute(sql)
		self.db.commit()

	def update_customer_phone(self, customer_id, customer_phone):
		'''
		根据顾客ID修改顾客手机号
		'''
		sql = '''
		update 顾客信息 set customer_phone='%s' where customer_id='%s' 
		'''%(customer_phone,customer_id)
		if self.__query_customer_info_by_whole_id(customer_id) == ():
			raise Exception('用户不存在')
		self.cursor.execute(sql)
		self.db.commit()

	def update_item_name(self, item_id, item_name):
		'''
		根据商品ID修改商品名称
		'''
		sql = '''
		update 商品信息 set item_name='%s' where item_id=%s
		'''%(item_name,item_id)
		if self.__query_item_info_by_whole_id(item_id) == ():
			raise Exception('商品不存在')
		self.cursor.execute(sql)
		self.db.commit()

	def update_item_price(self, item_id, item_price):
		'''
		根据商品ID修改商品价格
		'''
		sql = '''
		update 商品信息 set item_price='%s' where item_id=%s
		'''%(item_price,item_id)
		if self.__query_item_info_by_whole_id(item_id) == ():
			raise Exception('商品不存在')
		self.cursor.execute(sql)
		self.db.commit()

	def update_item_type(self, item_id, item_type):
		'''
		根据商品ID修改商品类型
		'''
		item_type = item_type.replace('，',',')
		sql = '''
		update 商品信息 set item_type='%s' where item_id=%s
		'''%(item_type,item_id)
		if self.__query_item_info_by_whole_id(item_id) == ():
			raise Exception('商品不存在')
		self.cursor.execute(sql)
		self.db.commit()

	def update_item_discount(self, item_id, discount,discount_start_time,discount_end_time):
		'''
		根据商品ID修改商品优惠
		'''
		sql = '''
		update 商品信息 set discount='%s',discount_start_time=str_to_date(\'%s\','%%Y-%%m-%%d'),discount_end_time=str_to_date(\'%s\','%%Y-%%m-%%d') where item_id=%s
		'''%(discount,discount_start_time,discount_end_time,item_id)
		if self.__query_item_info_by_whole_id(item_id) == ():
			raise Exception('商品不存在')
		self.cursor.execute(sql)
		self.db.commit()

if __name__ == '__main__':
	b = Db()

	# 添加数据
	# b.add_vendor_login('rot','root','12345678912345678912')
	# b.add_member_login('rot','root','1234568')
	# b.add_item_info('123456798','泡面','6.5','食品，泡面,康师傅泡面','','','')
	# b.add_customer_info('杨义军','1998-01-01','男','18101303936','是')
	# b.add_item_discount_by_item_id('123456789','五折')
	# b.add_order('1234567','123456789','6.5','1','65','李凯')

	# 查找数据
	# print(b.query_vendor_login('rot','root'))
	# print(b.query_member_login('ropot','rot'))
	# print(b.query_customer_info_by_id('46'))
	# print(b.query_customer_info_by_name('义'))
	# print(b.query_item_info_by_id('123'))
	# print(b.query_item_info_by_name('面'))
	# print(b.query_item_discount())
	# print(b.query_order_by_order_id('123456714180828'))
	# print(b.query_order_by_customer_id('67'))
	# print(b.query_order_by_time('2018-08-29'))

	# 删除数据
	# b.delete_item_info_by_item_id('123456789')
	# b.delete_item_info_by_item_name('泡面')
	# b.delete_item_discount_by_item_id('123456789')

	# 修改数据
	# b.update_vendor_pw('rot','root','roott')
	# b.update_member_pw('rot','root','roott')
	# b.update_customer_name('2230009','经济')
	# b.update_customer_gender('2230009','女')
	# b.update_customer_phone('2230009','12345678956')
	# b.update_customer_birthday('2230009','2020-10-10')
	# b.update_item_name('123456789','fdf')
	# b.update_item_price('123456789','66')
	# b.update_item_type('123456789','无')

	help(Db)
