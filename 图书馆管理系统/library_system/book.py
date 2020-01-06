from datetime import *
__metaclass__ = type
class Book:
	'''一个书本信息类，包括书本名字，作者名字和书本简单信息'''
	def __init__(self, bookName = "", author = ""):
		self.bookName = bookName                                      #书本名字
		self.author = author                                          #作者名字
		self.add_date = date.today()                                  #书本添加日期

	def setBookName(self, name):
		self.bookName = name

	def getBookName(self):
		return self.bookName

	def setAuthor(self, author):
		self.author = author

	def getAuthor(self):
		return self.author


	def getAddDate(self):
		return self.add_date
