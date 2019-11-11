import MySQLdb, os

USERNAME = ""   # 数据库用户名
PSW = ""    # 数据库密码

# 在服务器上运行，使用了本地（即服务器）数据库
db = MySQLdb.connect("localhost", USERNAME, PSW, use_unicode=True, charset="utf8")  
cursor = db.cursor()
db.select_db('Swoosh')

while True:
	st = input('请输入LICENSE(只能是20位): ')
	sql = '''
	insert into LICENSES(licenses) values('%s')
	'''%st
	if len(st) == 20:
		try:
			cursor.execute(sql)
			db.commit()
			break
		except Exception as e:
			print(e)
			
cursor.close()
db.close()
os.system("pause")
