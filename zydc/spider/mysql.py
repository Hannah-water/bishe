#-*-coding:utf-8 -*-

import MySQLdb
import time

class Mysql:

	#获取当前时间
	def getCurrentTime(self):
		return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))

	#数据库初始化
	def __init__(self):
		try:
			self.db = MySQLdb.connect(host='localhost',user='root',passwd='121261',db='zy_db',port=3306,charset='utf8')
			self.cur = self.db.cursor()
		except MySQLdb.Error,e:
			print self.getCurrentTime(),"连接数据库错误，原因%d: %s" % (e.args[0],e.args[1])

	#插入数据
	def insertData(self,table,my_dict):
		try:
			self.db.set_character_set('utf8')
			cols = ', '.join(my_dict.keys())
			values = '"," '.join(my_dict.values())
			#sql = "INSERT INTO %s(%s) VALUES(%s) WHERE NOT EXISTS (SELECT * FROM %s WHERE %s = %s)" % (table, cols, '"'+values+'"', table, cols, '"'+values+'"')
			#sql = "INSERT INTO %s(%s) VALUES(%s)" % (table, cols, '"'+values+'"')
			sql = "INSERT INTO %s(%s) VALUES(%s) ON DUPLICATE KEY UPDATE %s=%s" % (table, cols, '"'+values+'"', cols, '"'+values+'"')
			try:
				result = self.cur.execute(sql)
				insert_id = self.db.insert_id()
				self.db.commit()
				#判断是否执行成功
				if result:
					return insert_id
				else:
					return 0
			except MySQLdb.Error,e:
				#发生错误时回滚
				self.db.rollback()
				#主键唯一，无法插入
				if "key 'PRIMARY'" in e.args[1]:
					print self.getCurrentTime(),"数据已存在，未插入数据"
				else:
					print self.getCurrentTime(),"插入数据失败，原因%d: %s" % (e.args[0], e.args[1])
		except MySQLdb.Error,e:
			print self.getCurrentTime(),"数据库错误，原因%d: %s" % (e.args[0], e.args[1])


	#查询数据
	def selectData(self,table,col):
		try:
			self.db.set_character_set('utf8')
			sql = "SELECT %s FROM %s" % (col, table)
			try:
				self.cur.execute(sql)
				result = self.cur.fetchall()
				self.db.commit()
				return result
				#判断是否执行成功
				if result:
					return 1
				else:
					return 0
			except MySQLdb.Error,e:
				print self.getCurrentTime(),"查询数据失败，原因%d: %s" % (e.args[0], e.args[1])
		except MySQLdb.Error,e:
			print self.getCurrentTime(),"数据库错误，原因%d: %s" % (e.args[0], e.args[1])