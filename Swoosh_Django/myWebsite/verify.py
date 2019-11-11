import time
from myWebsite import db

class Verify:
	def __init__(self):
		self.db = db.Db()
	def __is_valid_date(self,str):
		'''判断是否是一个有效的日期字符串'''
		try:
			time.strptime(str, "%Y-%m-%d")
			return True
		except:
			return False

	def __test_username(self, name):
		vname = str(name)
		vnamelen = len(vname)
		num = 0
		for v in vname:
			if v in '_' or v.isalnum()==True:
				continue
			else:
				num += 1
		if num == 0 and (vnamelen>0 and vnamelen<=20):
			return True
		else:
			print("用户名不能为空或者大于二十位，只能包含'_'")
			return False

	def __test_pw(self,pw):
		vpw=str(pw)
		vpwlen = len(vpw)
		if vpwlen>0 or vpwlen<=20:
			return True
		else:
			print("密码不能为空或者大于二十位！")
			return False

	def __test_license(self,li):
		listr=str(li)
		lilen=len(listr)
		if (lilen==20):
			return True
		else:
			print("商家证书只能是二十位！")
			return False

	def __test_customer_id(self,customer_id):
		cidstr = str(customer_id)
		cidlen = len(cidstr)
		if (cidlen == 7)and cidstr.isdigit()==True:
			return True
		else:
			print("客户ID只能为7位数字")
			return False

	def __test_name(self, name):
		cname=str(name)
		cnamelen=len(cname)
		if (cnamelen > 0 and cnamelen <= 10):
			return True
		else:
			print("名字不得大于十位！")
			return False

	def __test_customer_birthday(self,customer_birthday):
		if(self.__is_valid_date(customer_birthday)==True):
			return True
		else:
			print("生日必须是“xxxx-xx-xx”格式！")
			return False

	def __test_customer_gender(self,customer_gender):
		cgstr=str(customer_gender)
		if cgstr.find(u"男") != -1 or cgstr.find(u"女") != -1:
			return True
		else:
			print("性别只能是男或女！")
			return False

	def __test_customer_phone(self,customer_phone):
		cphone=str(customer_phone)
		cphonelen=len(cphone)
		if(cphonelen==11 and cphone.isdigit()==True):
			return True
		else:
			print("手机号只能是11位！")
			return False

	def __test_is_member(self,is_member):
		isstr=str(is_member)
		if isstr.find(u"是") != -1 or isstr.find(u"否") != -1:
			return True
		else:
			print("是否会员只能填写是或否！")
			return False

	def __test_item_id(self,item_id):
		iid = str(item_id)
		ilen = len(iid)
		if (ilen > 0 and ilen <= 20) and item_id.isdigit()==True:
			return True
		else:
			print("商品id必须是小于20位的数字！")
			return False	  

	def __test_item_price(self,item_price):
		try:
			iprice = float(item_price)
			if  iprice < 100000:
				return True
			else:
				print("商品价格必须小于10万")
				return False
		except:
			print('格式不正确')
			return False

	def __test_item_type(self,item_type):
		itype=str(item_type)
		itype = itype.replace('，', '')
		itype = itype.replace(',', '')
		if(len(itype)<20):
			return True
		else:
			print("商品种类必须小于20位！")
			return False

	def __test_order_id(self,order_id):
		cid = str(customer_id)
		cidlen = len(cid)
		if (cidlen == 15) and cid.isdigit()==True:
			return True
		else:
			print("订单号必须是15位的数字！")
			return False

	def vendor_login(self, vendor_name, vendor_pw):
		'''
		商家登陆
		'''
		n = self.db.query_vendor_login(vendor_name,vendor_pw)
		if n:
			return True
		else:
			return False

	def vendor_verify(self, vendor_name, vendor_pw, license):
		'''
		商家认证
		'''
		if not self.__test_username(vendor_name):
			return 'username'
		if not self.__test_pw(vendor_pw):
			return 'pw'
		try:
			self.db.add_vendor_login(vendor_name, vendor_pw, license)
			return True
		except Exception as e:
			# print(e)
			if str(e) == 'LICENSE 不存在或已被使用':
				return 'nolicense'
			else:
				return 'license'

	def member_login(self, member_name, member_pw):
		'''
		会员登陆
		'''
		n = self.db.query_member_login(member_name,member_pw)
		if n:
			return True
		else:
			return False

	def member_sign_up(self,member_username,member_pw,member_name,member_birthday,member_gender,member_phone):
		'''
		会员注册
		'''
		# print('要执行')
		if not (self.__test_username(member_username) and self.__test_pw(member_pw)):
			# print('123456')
			return False
		try:
			if not self.db.query_member_if_exists(member_username):
				customer_id = self.db.add_customer_info(member_name,member_birthday,member_gender,member_phone,'是')
				self.db.add_member_login(member_username,member_pw,customer_id)
				# print('不可执行')
				return customer_id
			else:
				# print('执行了吗')
				return False
		except Exception as e:
			print(e)
			# print(e)
			# return False
			return str(e)

	def query_customer_info(self, id_or_name):
		'''
		搜索客户，可用客户ID、会员名，返回查询后的信息
		'''
		if not id_or_name.isdigit():
			return self.db.query_customer_info_by_name(id_or_name)
		else:
			n = self.db.query_customer_info_by_name(id_or_name)
			m = self.db.query_customer_info_by_id(id_or_name)
			if m != ():
				return m
			else:
				return n

	def query_order_by_id(self, id):
		'''
		查询订单，可用订单ID、客户ID，返回查询后的信息
		'''
		info = []
		m = self.db.query_order_by_order_id(id)
		n = self.db.query_order_by_customer_id(id)
		info.extend(m)
		info.extend(n)
		info = set(info)
		return tuple(info)

	def query_order_by_time(self, time):
		'''
		查询订单，根据时间
		'''
		return self.db.query_order_by_time(time)

	def query_item_info(self, id_or_name):
		'''
		搜索商品信息，可用商品ID、商品名，返回查询后的信息
		'''
		if not id_or_name.isdigit():
			return self.db.query_item_info_by_name(id_or_name)
		else:
			n = self.db.query_item_info_by_name(id_or_name)
			m = self.db.query_item_info_by_id(id_or_name)
			if m != ():
				return m
			else:
				return n		

	def query_item_info_by_type(self, type, type_phase):
		'''
		查询商品信息，根据不同级别的类别
		'''
		type_phase = str(type_phase)
		if type_phase == '1':
			return self.db.query_item_info_by_type1(type)
		elif type_phase == '2':
			return self.db.query_item_info_by_type2(type)
		elif type_phase == '3':
			return self.db.query_item_info_by_type3(type)
		else:
			print('只有3种等级的分类')
			return False

	def query_item_discount(self):
		'''
		查询商品优惠
		'''
		return self.db.query_item_discount()

	def add_item_discount_by_item_id(self, item_id,price, discount,discount_start_time,discount_end_time,kucun=0,qudao=''):
		'''
		增加商品优惠，根据商品ID
		'''
		self.db.add_item_discount_by_item_id(item_id,price,discount,discount_start_time,discount_end_time,kucun,qudao)

	def update_kucun(self, item_id, number):
		'''
		修改库存，根据商品ID
		'''
		self.db.update_kucun(item_id,number)

	def delete_item_discount_by_item_id(self, item_id):
		'''
		删除商品优惠，根据商品ID
		'''
		self.db.delete_item_discount_by_item_id(item_id)

	def add_item_info(self, item_name,item_price,item_type, discount='',discount_start_time='',discount_end_time='', item_id='',kucun=0,qudao=''):
		'''
		添加商品，商品ID可自动生成也可输入
		'''
		try:
			if item_id == '':
				item_id = self.db.create_item_id()
			self.db.add_item_info(item_id,item_name,item_price,item_type, discount,discount_start_time,discount_end_time,kucun,qudao)
			return True
		except Exception as e:
			print(e)
			return False

	def delete_item_info(self, item_id):
		'''
		删除商品信息，根据商品ID
		'''
		try:
			self.db.delete_item_info_by_item_id(item_id)
			return True
		except Exception as e:
			print(e)
			return False

	def add_order(self,customer_id,items_id,items_single_price,items_number,total_price,submitter):
		'''
		添加订单
		'''
		try:
			self.db.add_order(customer_id,items_id,items_single_price,items_number,total_price,submitter)
			return True
		except Exception as e:
			print(e)
			return False

	def update_member_pw(self, member_name, member_pre_pw, member_pw):
		'''
		修改会员密码
		'''
		try:
			self.db.update_member_pw(member_name, member_pre_pw, member_pw)
			return True
		except Exception as e:
			print(e)
			return False

	def update_vendor_pw(self, vendor_name, vendor_pre_pw, vendor_pw):
		'''
		修改商家密码
		'''
		try:
			self.db.update_vendor_pw(vendor_name, vendor_pre_pw, vendor_pw)
			return True
		except Exception as e:
			print(e)
			return False

	def update_member_info(self,customer_id,member_name,member_birthday,member_gender,member_phone):
		'''
		修改会员信息，根据用户ID
		'''
		try:
			self.db.update_customer_name(customer_id,member_name)
			self.db.update_customer_birthday(customer_id,member_birthday)
			self.db.update_customer_gender(customer_id,member_gender)
			self.db.update_customer_phone(customer_id,member_phone)
			return True
		except Exception as e:
			print(e)
			return False

	def update_item_info(self,item_id,item_name,item_price,item_type,discount='',discount_start_time='',discount_end_time=''):
		'''
		修改商品信息，根据商品ID
		'''
		try:
			self.db.update_item_name(item_id,item_name)
			self.db.update_item_price(item_id,item_price)
			self.db.update_item_type(item_id,item_type)
			self.db.update_item_discount(item_id,discount,discount_start_time,discount_end_time)
			return True
		except Exception as e:
			print(e)
			return False

if __name__ == '__main__':
	v = Verify()
	# print(v.vendor_login('teee','test'))
	# print(v.vender_verify('teee','test','12345678912345678912'))
	# print(v.member_sign_up('tt','te','测试','1998-12-12','女','18145626984'))
	# print(v.member_login('tt','tt'))
	# print(v.query_customer_info('测试'))
	# print(v.query_order_by_id('1'))
	# print(v.query_order_by_time('2018-08-28'))
	# print(v.query_item_info('8'))
	# print(v.query_item_info_by_type('泡面',2))
	# print(v.query_item_discount())
	# print(v.add_item_discount_by_item_id('95957069000623258762','五折','2018-09-11','2018-10-13'))
	# print(v.delete_item_discount_by_item_id('82317980291747625700'))
	# print(v.add_item_info('手机','5000','电子，手机，iPhone'))
	# print(v.delete_item_info('82317980291747625700'))
	# print(v.add_order('1123546','123456,123456789','6.5,15','1,1','21.5','李凯'))
	# print(v.update_member_pw('rot','root','rot'))
	# print(v.update_vendor_pw('rot','root','rot'))
	# print(v.update_member_info('3404213','','','',''))
	# print(v.update_item_info('95957069000623258762','','','','五折'))

	help(Verify)