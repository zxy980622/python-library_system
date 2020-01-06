
import wx
from book import *
from dbhelper import *
from lendmessage import *

class Searchframe(wx.Frame):
    '''搜索书籍弹出的小窗口'''

    def __init__(self, parent, title):
        '''初始化该小窗口的布局'''

        self.mainframe = parent
        wx.Frame.__init__(self, parent, title = title, size = (200, 200), pos = (150,150))

        self.panel = wx.Panel(self, pos = (0, 0), size = (200, 250))
        self.panel.SetBackgroundColour("#FFFFFF")
        bookName_tip = wx.StaticText(self.panel, label = "书名:", pos = (5, 8), size = (35, 25))
        bookName_tip.SetBackgroundColour("#FFFFFF")
        bookName_text = wx.TextCtrl(self.panel, pos = (40, 5), size = (100, 25))
        self.name = bookName_text
        save_button = wx.Button(self.panel, label = "搜索书籍", pos = (40, 60))
        self.Bind(wx.EVT_BUTTON, self.Search_book, save_button)

    def Search_book(self,txt):
        bookName = self.name.GetValue()
        # 需要用到的数据库接口
        self.dbhelper = DBHelper()

        datass = self.dbhelper.getBookByName(bookName)
        Num = self.mainframe.list.GetItemCount()
        for num in range(0,Num):
            self.mainframe.list.DeleteItem(0)
        if datass == None:
            warn = wx.MessageDialog(self, message="没有这本书", caption="错误警告")
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        index = self.mainframe.list.InsertItem(self.mainframe.list.GetItemCount(), str(datass[0]))
        self.mainframe.list.SetItem(index, 1, str(datass[1]))
        self.mainframe.list.SetItem(index, 2, str(datass[2]))
        self.Destroy()

class AddFrame(wx.Frame):

    '''添加书籍弹出的小窗口'''

    def __init__(self, parent, title):
        '''初始化该小窗口的布局'''

        self.mainframe = parent
        wx.Frame.__init__(self, parent, title = title, pos = (250,200),size = (255, 200))
        self.panel = wx.Panel(self, pos = (500, 50), size = (255, 200))
        self.panel.SetBackgroundColour("#FFFFFF")
        #背景为白色

        bookName_tip = wx.StaticText(self.panel, label = "书名:", pos = (5, 8), size = (35, 25))
        bookName_tip.SetBackgroundColour("#FFFFFF")
        bookName_text = wx.TextCtrl(self.panel, pos = (40, 5), size = (150, 25))
        self.name = bookName_text

        author_tip = wx.StaticText(self.panel, label = "作者:", pos = (5, 38), size = (35, 25))
        author_tip.SetBackgroundColour("#FFFFFF")
        author_text = wx.TextCtrl(self.panel, pos = (40, 35), size = (150, 25))
        self.author = author_text

        save_button = wx.Button(self.panel, label = "保存书籍", pos = (40, 70))
        self.Bind(wx.EVT_BUTTON, self.saveBook, save_button)

        #需要用到的数据库接口
        self.dbhelper = DBHelper()


    def saveBook(self, evt):
        bookName = self.name.GetValue()
        author = self.author.GetValue()
        #content = self.content.GetValue()
        if bookName == "" or author == "": #or content == "":
            warn = wx.MessageDialog(self, message = "不能为空", caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()                                             #提示错误
            warn.Destroy()
            return
        self.dbhelper = DBHelper()
        datas = self.dbhelper.getAllBook()
        datass = self.dbhelper.getAllLendBook()
        for data in datas:
            if data[1] == bookName:
                warn = wx.MessageDialog(self, message="重复书名", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
                warn.ShowModal()  # 提示错误
                warn.Destroy()
                return
        for data in datass:
            if data[1] == bookName:
                warn = wx.MessageDialog(self, message="重复书名", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
                warn.ShowModal()  # 提示错误
                warn.Destroy()
                return
        book = Book(bookName, author)# content)
        book_id = self.dbhelper.insertBook(book)
        Num = self.mainframe.list.GetItemCount()
        for num in range(0, Num):
            self.mainframe.list.DeleteItem(0)
        self.mainframe.dbhelper = DBHelper()
        datas = self.mainframe.dbhelper.getAllBook()
        for data in datas:
            index = self.mainframe.list.InsertItem(self.mainframe.list.GetItemCount(), str(data[0]))
            self.mainframe.list.SetItem(index, 1, str(data[1]))
            self.mainframe.list.SetItem(index, 2, str(data[2]))
        self.Destroy()

class UpdateFrame(wx.Frame):
    def __init__(self, parent, title, select_id):
        '''初始化更新图书信息界面总布局'''
        wx.Frame(parent, title = title, size = (400, 250))

        #用来调用父frame,便于更新
        self.mainframe = parent
        #生成一个300*300的框
        wx.Frame.__init__(self, parent, title = title, size = (300, 200))

        self.panel = wx.Panel(self, pos = (0, 0), size = (300, 200))
        self.panel.SetBackgroundColour("#FFFFFF")                              #背景为白色

        #三个编辑框，分别用来编辑书名，作者，书籍相关信息
        bookName_tip = wx.StaticText(self.panel, label = "书名:", pos = (5, 8), size = (35, 25))
        bookName_tip.SetBackgroundColour("#FFFFFF")
        bookName_text = wx.TextCtrl(self.panel, pos = (40, 5), size = (200, 25))
        self.name = bookName_text

        author_tip = wx.StaticText(self.panel, label = "作者:", pos = (5, 38), size = (35, 25))
        author_tip.SetBackgroundColour("#FFFFFF")
        author_text = wx.TextCtrl(self.panel, pos = (40, 35), size = (200, 25))
        self.author = author_text

        save_button = wx.Button(self.panel, label = "保存修改", pos = (40, 65))
        self.Bind(wx.EVT_BUTTON, self.saveUpdate, save_button)

        #选中的id和bookid
        self.select_id = select_id
        self.bookid = self.mainframe.list.GetItem(select_id, 0).Text             #获取第select_id行的第0列的值
        #需要用到的数据库接口
        self.dbhelper = DBHelper()
        self.showAllText()                     #展现所有的text原来取值


    def showAllText(self):
        '''显示概述本原始信息'''
        data = self.dbhelper.getBookById(self.bookid)                      #通过id获取书本信息
        self.name.SetValue(data[0])                                        #设置值
        self.author.SetValue(data[1])

    def saveUpdate(self, evt):
        '''保存修改后的值'''
        bookName = self.name.GetValue()                                    #获得修改后的值
        author = self.author.GetValue()

        print("书名:"+bookName)
        if bookName == "" or author == "" :#or content == "":
            warn = wx.MessageDialog(self, message = "所有信息不能为空", caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()                                                             #提示错误
            warn.Destroy()
            return
        else:
            print("开始将修改后的数据保存到数据库中")
            book = Book(bookName, author)                 #将数据封装到book对象中
            self.dbhelper.saveUpdate(self.bookid, book)
            self.mainframe.list.SetItem(self.select_id, 1, bookName)
            self.mainframe.list.SetItem(self.select_id, 2, author)
        self.Destroy()                                                     #修改完后自动销毁

class ShowFrame(wx.Frame):
    '''用来显示书籍的信息'''

    def __init__(self, parent, title, select_id):
        '''初始化该小窗口的布局'''

        #便于调用父窗口
        self.mainframe = parent

        #生成一个的框
        wx.Frame.__init__(self, parent, title = title, size = (300, 200), pos = (150,150))

        self.panel = wx.Panel(self, pos = (0, 0), size = (300, 200))
        self.panel.SetBackgroundColour("#FFFFFF")                          #背景为白色

        bookName_tip = wx.StaticText(self.panel, label = "书名:", pos = (5, 8), size = (35, 25))
        bookName_tip.SetBackgroundColour("#FFFFFF")
        bookName_text = wx.TextCtrl(self.panel, pos = (40, 5), size = (200, 25))
        bookName_text.SetEditable(False)
        self.name = bookName_text

        author_tip = wx.StaticText(self.panel, label = "作者:", pos = (5, 38), size = (35, 25))
        author_tip.SetBackgroundColour("#FFFFFF")
        author_text = wx.TextCtrl(self.panel, pos = (40, 35), size = (200, 25))
        author_text.SetEditable(False)
        self.author = author_text

        #选中的id和bookid
        self.select_id = select_id
        self.bookid = self.mainframe.list.GetItem(select_id, 0).Text             #获取第select_id行的第0列的值

        #需要用到的数据库接口
        self.dbhelper = DBHelper()
        self.showAllText()                     #展现所有的text原来取值

    def showAllText(self):
        '''显示概述本原始信息'''
        data = self.dbhelper.getBookById(self.bookid)                      #通过id获取书本信息

        self.name.SetValue(data[0])                                        #设置值
        self.author.SetValue(data[1])

class Lend_Message(wx.Frame):
    def __init__(self,parent, title):
        '''初始化系统总体布局，包括各种控件'''
        self.mainframe = parent

        #生成一个宽为400，高为400的frame框
        wx.Frame.__init__(self, parent, title=title, size=(400, 400))

        #定一个网格布局
        self.main_layout = wx.BoxSizer(wx.VERTICAL)


        #生成一个列表
        self.list = wx.ListCtrl(self, -1, size = (400,300), style = wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES) #| wx.LC_SINGLE_SEL
        #列表有散列，分别是书本ID,书名，添加日期
        self.list.InsertColumn(0, "学生名")
        self.list.InsertColumn(1, "书名")
        self.list.InsertColumn(2, "借书日期")
        #设置各列的宽度
        self.list.SetColumnWidth(0, 60)                                         #设置每一列的宽度
        self.list.SetColumnWidth(1, 150)
        self.list.SetColumnWidth(2, 200)

        #添加一组按钮，实现增删改查,用一个panel来管理该组按钮的布局
        self.panel = wx.Panel(self, pos = (0, 300), size = (400, 100))
        back_button = wx.Button(self.panel, label="还书", pos=(170, 25), size=(60, 30))  # , size = (75, 30)
        self.Bind(wx.EVT_BUTTON, self.backbook, back_button)


        self.dbhelper = DBHelper()
        datas = self.dbhelper.getAllLendBook()

        for data in datas:
            index = self.list.InsertItem(self.list.GetItemCount(), str(data[0]))
            self.list.SetItem(index, 1, data[1])
            self.list.SetItem(index, 2, str(data[2]))


    def backbook(self,evt):
        '''还书，先把数据插入图书库，再从已借阅图书删除，删除显示信息'''
        selectId = self.list.GetFirstSelected()
        if selectId == -1:
            warn = wx.MessageDialog(self, message="没选书", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        else:
            bookname = self.list.GetItem(selectId, 1).Text
            bookdata=self.dbhelper.getdata(bookname)
            book1=Book(bookdata[0][0],bookdata[0][1])
            book_id=self.dbhelper.insertBook(book1)
            self.dbhelper.delLendMessgae(bookname)
            self.list.DeleteItem(selectId)
            self.mainframe.addToList(book_id, book1)

class LendBook(wx.Frame):
    def __init__(self, parent, title, select_id,bookid):
        '''初始化更新图书信息界面总布局'''

        #用来调用父frame,便于更新
        self.bookid=bookid
        self.mainframe = parent
        #生成一个300*300的框
        wx.Frame.__init__(self, parent, title = title, size = (200 , 130))

        self.panel = wx.Panel(self, pos = (0, 0), size = (200, 130))
        self.panel.SetBackgroundColour("#FFFFFF")                              #背景为白色

        #三个编辑框，分别用来编辑书名，作者，书籍相关信息


        student_tip = wx.StaticText(self.panel, label = "学生名:", pos = (5, 20), size = (50, 25))
        student_tip.SetBackgroundColour("#FFFFFF")
        student_text = wx.TextCtrl(self.panel, pos = (60, 20), size = (100, 25))
        self.studentname = student_text

        lend_button = wx.Button(self.panel, label = "确定", pos = (95, 60))
        self.Bind(wx.EVT_BUTTON, self.lend, lend_button)

        #选中的id和bookid
        self.select_id = select_id
        #需要用到的数据库接口
        self.dbhelper = DBHelper()

    def lend(self,evt):
        '''删除列表中的值，删除数据库的值，增加借阅图书数据库的值'''
        if self.select_id == -1:
            warn = wx.MessageDialog(self, message="没选书", caption="错误警告")
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        else:
            stuname = self.studentname.GetValue()
            alldata=self.dbhelper.getBookById(self.bookid)
            bookname=alldata[0]
            author=alldata[1]
            lendbook=Lendbook(stuname,bookname,author)#,content)
            self.dbhelper.savelendbook(lendbook)
            self.dbhelper.deleteBook(self.bookid)
        self.Destroy()

class BackBook(wx.Frame):
    def __init__(self, parent, title):
        '''初始化更新图书信息界面总布局'''

        #用来调用父frame,便于更新
        self.mainframe = parent
        #生成一个300*300的框
        wx.Frame.__init__(self, parent, title = title, size = (200 , 130))

        self.panel = wx.Panel(self, pos = (0, 0), size = (200, 130))
        self.panel.SetBackgroundColour("#FFFFFF")                              #背景为白色

        book_tip = wx.StaticText(self.panel, label = "书名:", pos = (5, 20), size = (50, 25))
        book_tip.SetBackgroundColour("#FFFFFF")
        book_text = wx.TextCtrl(self.panel, pos = (60, 20), size = (100, 25))
        self.bookname = book_text

        lend_button = wx.Button(self.panel, label = "确定", pos = (95, 60))
        self.Bind(wx.EVT_BUTTON, self.back, lend_button)
        # 需要用到的数据库接口
        self.dbhelper = DBHelper()

    def back(self,evt):
        bkname=self.bookname.GetValue()
        bookdata=self.dbhelper.getBook_ByName(bkname)
        book1 = Book(bookdata[0], bookdata[1])
        book_id = self.dbhelper.insertBook(book1)
        self.dbhelper.delLendMessgae(bkname)
        self.mainframe.addToList(book_id, book1)
        self.Destroy()

class LibraryFrame(wx.Frame):
    def __init__(self, parent, title):
        '''初始化系统总体布局，包括各种控件'''

        #生成一个宽为400，高为400的frame框
        wx.Frame.__init__(self, parent, title=title, size=(800, 800), style=wx.DEFAULT_FRAME_STYLE)

        #定一个网格布局
        self.main_layout = wx.BoxSizer(wx.HORIZONTAL)


        #生成一个列表
        self.list = wx.ListCtrl(self, -1, pos=(10,10),size = (600,300), style = wx.LC_REPORT | wx.LC_HRULES | wx.LC_VRULES)
        #列表有散列，分别是书本ID,书名，添加日期
        self.list.InsertColumn(0, "ID")
        self.list.InsertColumn(1, "书名")
        self.list.InsertColumn(2, "作者")
        #设置各列的宽度
        self.list.SetColumnWidth(0, 200)                                         #设置每一列的宽度
        self.list.SetColumnWidth(1, 200)
        self.list.SetColumnWidth(2, 200)

        #添加一组按钮，实现增删改查,用一个panel来管理该组按钮的布局
        self.panel = wx.Panel(self, pos = (150, 300), size = (600, 300))

        #定义一组按钮
        add_button = wx.Button(self.panel, label="添加", pos=(10, 15), size=(60, 60))
        del_button = wx.Button(self.panel, label="删除", pos=(110, 15), size=(60, 60))
        update_button = wx.Button(self.panel, label="修改", pos=(10, 85), size=(60, 60))
        query_button = wx.Button(self.panel, label="查看", pos=(110, 85), size=(60, 60))
        lend_message_button = wx.Button(self.panel, label="借书信息", pos=(10, 165), size=(60, 60))
        lend_button = wx.Button(self.panel, label="借书", pos=(110, 165), size=(60, 60))
        back_button = wx.Button(self.panel, label="还书", pos=(10, 235), size=(60, 60))
        search_button = wx.Button(self.panel, label="搜索", pos=(110, 235), size=(60, 60))  # , size = (75, 30)


        #w为按钮绑定相应事件函数，第一个参数为默认参数，指明为按钮类事件，第二个为事件函数名，第三个为按钮名
        self.Bind(wx.EVT_BUTTON, self.addBook, add_button)
        self.Bind(wx.EVT_BUTTON, self.delBook, del_button)
        self.Bind(wx.EVT_BUTTON, self.updateBook, update_button)
        self.Bind(wx.EVT_BUTTON, self.queryBook, query_button)
        self.Bind(wx.EVT_BUTTON, self.lend_message, lend_message_button)
        self.Bind(wx.EVT_BUTTON, self.lendbook, lend_button)
        self.Bind(wx.EVT_BUTTON, self.backbook, back_button)
        self.Bind(wx.EVT_BUTTON, self.searchBook, search_button)




        #将列表和panel添加到主面板

        self.main_layout.Add(self.list)
        self.main_layout.Add(self.panel)

        self.SetSizer(self.main_layout)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground) #背景
        #添加数据库操作对象
        self.dbhelper = DBHelper()
        datas = self.dbhelper.getAllBook()
        for data in datas:
            index = self.list.InsertItem(self.list.GetItemCount(), str(data[0]))
            self.list.SetItem(index, 1, data[1])
            self.list.SetItem(index, 2, data[2])

    def OnEraseBackground(self, evt):
        dc = evt.GetDC()

        if not dc:
            dc = wx.ClientDC(self)
            rect = self.GetUpdateRegion().GetBox()
            dc.SetClippingRect(rect)
        dc.Clear()
        bmp = wx.Bitmap("lib.jpeg")
        dc.DrawBitmap(bmp, 0, 0)

    def backbook(self,evt):
        b2=BackBook(self,'请输入书名:')
        b2.Show(True)

    def lend_message(self,evt):
        '''查看借阅信息'''
        l_message=Lend_Message(self,'已借图书信息')
        l_message.Show(True)

    def lendbook(self,evt):
        selectId = self.list.GetFirstSelected()
        if selectId == -1:
            warn = wx.MessageDialog(self, message="没选书", caption="错误警告")
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        else:
            bookid = self.list.GetItem(selectId, 0).Text  # 得到书本id
            lendbook=LendBook(self,'借书',selectId,bookid)
            lendbook.Show(True)

            self.list.DeleteItem(selectId)

    def searchBook(self, evt):
        '''查看按钮响应事件'''

        show_f = Searchframe(self, "搜索窗口")
        show_f.Show(True)

    def addBook(self, evt):
        '''添加书籍按钮，弹出添加书籍框'''
        add_bokk = AddFrame(self, "添加书籍窗口")
        add_bokk.Show(True)

    def delBook(self, evt):
        '''删除书籍按钮，先选中,然后删除'''
        selectId = self.list.GetFirstSelected()
        if selectId == -1:
            warn = wx.MessageDialog(self, message = "没选书", caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()                                                             #提示错误
            warn.Destroy()
            return
        else:
            bookid = self.list.GetItem(selectId, 0).Text                                 #得到书本id
            self.list.DeleteItem(selectId)                                               #先在listctrl中删除选中行
            self.dbhelper.deleteBook(bookid)

    def updateBook(self, evt):
        '''修改按钮响应事件，点击修改按钮，弹出修改框'''
        selectId = self.list.GetFirstSelected()
        if selectId == -1:
            warn = wx.MessageDialog(self, message = "没选书", caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()                                                             #提示错误
            warn.Destroy()
            return
        else:
            update_f = UpdateFrame(self, "修改书籍窗口", selectId)
            update_f.Show(True)

    def queryBook(self, evt):
        '''查看按钮响应事件'''
        selectId = self.list.GetFirstSelected()
        if selectId == -1:
            warn = wx.MessageDialog(self, message = "没选书", caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()                                                             #提示错误
            warn.Destroy()
            return
        else:
            show_f = ShowFrame(self, "查看书籍窗口", selectId)
            show_f.Show(True)

    def addToList(self, id, book):
        index = self.list.InsertItem(self.list.GetItemCount(), str(id))
        self.list.SetItem(index, 1, book.getBookName())
        self.list.SetItem(index, 2, book.author)

class LibraryApp(wx.App):
    def OnInit(self):
        frame = LibraryFrame(None, "zxy_lib")
        frame.Show()
        return True

if __name__ == "__main__":

    app = LibraryApp()
    app.MainLoop()

 
