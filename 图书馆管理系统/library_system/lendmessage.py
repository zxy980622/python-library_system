from datetime import *

class Lendbook():
	def __init__(self,student,bookname,author):

		self.student=student
		self.bookname=bookname
		self.author = author  # 作者名字
		self.l_date=date.today()

	def setStudent(self,student):
		self.student=student

	def getStudent(self):
		return self.student

	def setBookname(self,bookname):
		self.bookname=bookname

	def getBookname(self):
		return self.bookname

	def setAuthor(self, author):
		self.author = author

	def getAuthor(self):
		return self.author

	def getAddDate(self):
		return self.l_date




