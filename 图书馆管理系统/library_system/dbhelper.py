import pymysql
from datetime import *

class DBHelper:

	def getCon(self):

		conn = pymysql.connect(host = "localhost", port = 3306, user = "root", password = "root", db = "library", charset = "utf8")

		return conn

	def getdata(self, bookname):
		sql='select * from lend_message where book_name=%s'
		conn = self.getCon()
		if conn == None:
			return
		cursor = conn.cursor()
		cursor.execute(sql, (bookname,))
		rows = cursor.fetchall()
		list = []

		for item in rows:
			# print(type(item[4]))
			bitem = (item[1], item[2], item[3])

			list.append(bitem)

		conn.commit()
		cursor.close()
		conn.close()
		return list

	def delLendMessgae(self,bookname):
		sql = 'delete from lend_message where book_name=%s'
		conn = self.getCon()
		if conn == None:
			return
		cursor = conn.cursor()
		cursor.execute(sql,(bookname,))

		conn.commit()
		cursor.close()
		conn.close()


	def savelendbook(self,lendbook):
		sql="insert into lend_message(student_name,book_name, author, date) values(%s, %s, %s,%s)"
		conn=self.getCon()
		if conn ==None:
			return
		cursor = conn.cursor()
		cursor.execute(sql, (lendbook.getStudent(),lendbook.getBookname(), lendbook.getAuthor(),  date.today()))
		conn.commit()
		cursor.close()
		conn.close()

	def insertBook(self, book):
		'''向数据库中book表插入书本信息，book为Book类对象，包含书本基本信息'''
		sql = "insert into book(name, author, add_date) values(%s, %s, %s)"

		conn = self.getCon()
		if conn ==None:
			return

		cursor = conn.cursor()
		cursor.execute(sql, (book.getBookName(), book.getAuthor(), book.getAddDate()))

		conn.commit()
		cursor.close()
		conn.close()

		new_id = cursor.lastrowid

		return new_id


	def getAllLendBook(self):
		sql='select * from lend_message'
		conn=self.getCon()
		if conn == None:
			return

		cursor = conn.cursor()
		rownum = cursor.execute(sql)
		rows = cursor.fetchall()
		print(rows)
		list = []
		for item in rows:
			# print(type(item[4]))
			bitem = (item[0], item[1], item[3])

			list.append(bitem)
		cursor.close()
		conn.close()
		return list


	def getAllBook(self):
		'''返回数据库中，book表中所有的书本信息'''
		sql = "select *from book"

		conn = self.getCon()
		if conn == None:
			return

		cursor = conn.cursor()
		rownum = cursor.execute(sql)              #执行并返回找到的行数

		#获取查询结果
		rows = cursor.fetchall()
		print(rows)
		list = []

		for item in rows:
			# print(type(item[4]))
			bitem = (item[0], item[1], item[2])

			list.append(bitem)
		# print(list) #111111111111111111111111
		conn.commit()
		cursor.close()
		conn.close()

		return list

	def getBookById(self, bookid):
		'''根据书本id值来寻找书本信息'''

		sql = "select book.name, book.author from book  where id=%s"

		conn = self.getCon()
		if conn == None:
			return

		cursor = conn.cursor()
		cursor.execute(sql, (bookid, ))                     #参数以元组形式给出
		row = cursor.fetchone()                             #取到第一个结果

		conn.commit()
		cursor.close()
		conn.close()

		return row


	def getBookByName(self, bookname):
		sql = "select book.id, book.name, book.author from book  where name=%s"
		conn = self.getCon()
		if conn == None:
			return
		cursor = conn.cursor()
		cursor.execute(sql, (bookname,))  # 参数以元组形式给出
		row = cursor.fetchone()
		print(type(row))
		conn.commit()
		cursor.close()
		conn.close()

		return row

	def getBook_ByName(self, bookname):
		sql = "select book_name, author from lend_message  where book_name=%s"
		conn = self.getCon()
		if conn == None:
			return
		cursor = conn.cursor()
		cursor.execute(sql, (bookname,))  # 参数以元组形式给出
		row = cursor.fetchone()
		conn.commit()
		cursor.close()
		conn.close()

		return row


	def saveUpdate(self, bookid, book):
			'''用book对象来修改id为bookid的书本信息'''
			sql = "update book set book.name=%s, book.author=%s where book.id=%s"

			conn = self.getCon()
			if conn == None:
				return

			cursor = conn.cursor()
			cursor.execute(sql, (book.getBookName(), book.getAuthor(),  bookid))

			conn.commit()
			cursor.close()
			conn.close()

	def deleteBook(self, bookid):
		'''根据书本id来删除书籍'''
		sql = "delete from book where book.id = %s"

		conn = self.getCon()
		if conn == None:
			return

		cursor = conn.cursor()
		cursor.execute(sql, (bookid, ))

		conn.commit()
		cursor.close()
		conn.close()

