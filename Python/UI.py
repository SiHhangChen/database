import customtkinter
from connect import *
from PIL import Image
import os

customtkinter.set_appearance_mode("dark")

class App(customtkinter.CTk):
    width = 1000
    height = 600

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.title("CustomTkinter example_background_image.py")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)
        
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure((0, 1, 2, 3), weight=1)
        
        # create sidebar frame
        self.sidebar_frame = customtkinter.CTkFrame(self, width=20, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsw") #rowspan表示占据的行数
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["20%","80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))
        
        # create login frame
        self.login_frame = customtkinter.CTkFrame(self, corner_radius=0, width=900, height=600)# corner_radius=0表示圆角半径为0
        self.login_frame.grid(row=0, column=1,rowspan=4, columnspan=3)
        self.login_label = customtkinter.CTkLabel(self.login_frame, text="USTC LIBRARY\nLogin Page",
                                                  font=customtkinter.CTkFont(size=40, weight="bold"))
        self.login_label.grid(row=0, column=1, padx=50, pady=50)
        self.username_entry = customtkinter.CTkEntry(self.login_frame, width=200, placeholder_text="username")
        self.username_entry.grid(row=1, column=1, padx=50, pady=(30, 15))
        self.radio_var = customtkinter.StringVar(value='\0')
        self.libE_button = customtkinter.CTkRadioButton(self.login_frame, text="E", variable=self.radio_var, value='E')
        self.libE_button.grid(row=1, column=2, padx=1, pady=(30, 15))
        self.libW_button = customtkinter.CTkRadioButton(self.login_frame, text="W", variable=self.radio_var, value='W')
        self.libW_button.grid(row=1, column=3, padx=1, pady=(30, 15))
        self.libH_button = customtkinter.CTkRadioButton(self.login_frame, text="H", variable=self.radio_var, value='H')
        self.libH_button.grid(row=1, column=4, padx=1, pady=(30, 15))
        self.password_entry = customtkinter.CTkEntry(self.login_frame, width=200, show="*", placeholder_text="password")
        self.password_entry.grid(row=3, column=1, padx=50, pady=(30, 15))
        self.login_button = customtkinter.CTkButton(self.login_frame, text="Login", command=self.login_event, width=200)
        self.login_button.grid(row=4, column=1, padx=50, pady=(15, 15))

        # create main frame
        self.main_frame = customtkinter.CTkFrame(self, corner_radius=0, width=600, height=1100)
        self.main_frame.grid_columnconfigure(0, weight=1) # 这函数的作用是
        self.main_label = customtkinter.CTkLabel(self.main_frame, text="中国科学技术大学\n读好书-来科大",
                                                 font=customtkinter.CTkFont(size=30, weight="bold", family="STXingkai"))
        self.main_label.grid(row=0, column=0, padx=30, pady=50, columnspan=3)
        self.personal_button = customtkinter.CTkButton(self.main_frame, text="personal", command=self.personal_event, width=200, height=50)
        self.personal_button.grid(row=1, column=0, padx=30, pady=30)
        self.br_button = customtkinter.CTkButton(self.main_frame, text="Borrow and reserve", command=self.br_event, width=200, height=50)
        self.br_button.grid(row=2, column=0, padx=30, pady=30)
        self.select_button = customtkinter.CTkButton(self.main_frame, text="Select", command=self.select_event, width=200, height=50)
        self.select_button.grid(row=3, column=0, padx=30, pady=30)
        self.back_button = customtkinter.CTkButton(self.main_frame, text="Back", command=self.mainBackLogin_event, width=200, height=50)
        self.back_button.grid(row=4, column=0, padx=30, pady=30)

        # personal frame
        # self.personal_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        # self.personal_frame.grid_remove()
        self.personal_frame = customtkinter.CTkScrollableFrame(self, width=700, height=500)
        self.personal_frame.grid_remove()
        # 个人界面的内容
        self.sidePerson_frame = customtkinter.CTkFrame(self, width=20, corner_radius=0)
        # self.sidePerson_frame.grid(row=0, column=0, rowspan=4, sticky="nsw") #rowspan表示占据的行数
        self.sidePerson_frame.grid_remove()
        self.sidePerson_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidePerson_frame, text="Personal", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidePerson_button_borrowed = customtkinter.CTkButton(self.sidePerson_frame, text="借书记录", command=self.sidebar_button_borrow_event)
        self.sidePerson_button_borrowed.grid(row=1, column=0, padx=20, pady=10)
        self.sidePerson_button_reserved = customtkinter.CTkButton(self.sidePerson_frame, text="预约记录", command=self.sidebar_button_reserve_event)
        self.sidePerson_button_reserved.grid(row=2, column=0, padx=20, pady=10)
        self.sidePerson_button_back = customtkinter.CTkButton(self.sidePerson_frame, text="back", command=self.personalBackMain_event)
        self.sidePerson_button_back.grid(row=3, column=0, padx=20, pady=10)
        # self.textbox = customtkinter.CTkTextbox(self, width=250)
        # self.textbox.grid_remove()
        
        #borrow frame
        self.br_frame = customtkinter.CTkFrame(self, corner_radius=0, width=500)
        self.br_frame.grid_remove()
        self.br_label = customtkinter.CTkLabel(self.br_frame, text="CustomTkinter\nborrow Page",
                                                    font=customtkinter.CTkFont(size=20, weight="bold"))
        self.br_label.grid(row=0, column=1, padx=30, pady=(50))
        self.brSearch_button = customtkinter.CTkButton(self.br_frame, text="Search", command=self.br2select_event, width=200)
        self.brSearch_button.grid(row=1, column=1, padx=30, pady=50)
        self.brBackMain_button = customtkinter.CTkButton(self.br_frame, text="Back", command=self.brBackMain_event, width=100, height=24)
        self.brBackMain_button.grid(row=8, column=1, padx=30, pady=30)
        
        # selcect frame
        self.select_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.select_frame.grid_remove()
        self.select_label = customtkinter.CTkLabel(self.select_frame, text="CustomTkinter\nselect Page",
                                                    font=customtkinter.CTkFont(size=20, weight="bold"))
        self.select_label.grid(row=0, column=1, padx=30, pady=50)
        self.search_bookname_entry = customtkinter.CTkEntry(self.select_frame, width=200, placeholder_text="bookname")
        self.search_bookname_entry.grid(row=1, column=0, padx=30, pady=15)
        self.search_author_entry = customtkinter.CTkEntry(self.select_frame, width=200, placeholder_text="author")
        self.search_author_entry.grid(row=1, column=1, padx=30, pady=15)
        self.search_button = customtkinter.CTkButton(self.select_frame, text="Search", command=self.search_event, width=200)
        self.search_button.grid(row=1, column=2, padx=30, pady=15)
        self.selectBackMain_button = customtkinter.CTkButton(self.select_frame, text="Back", command=self.selectBackMain_event, width=100, height=24)
        self.selectBackMain_button.grid(row=8, column=1, padx=30, pady=100)
        
        self.errorLogin_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.errorLogin_frame.grid_remove()
        self.errorLogin_label = customtkinter.CTkLabel(self.errorLogin_frame, text="ErrorLogin: Invalid username or password.", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.errorLogin_label.grid(row=0, column=0, padx=50, pady=50)
        self.errorLogin_button = customtkinter.CTkButton(self.errorLogin_frame, text="OK", command=self.errorLoginBackLogin_event, width=200)
        self.errorLogin_button.grid(row=1, column=0, padx=50, pady=50)
        
        self.afterBorrow_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.afterBorrow_frame.grid_remove()
        
        # 管理员专属界面, 只有三个按钮：添加书籍，删除书籍，修改书籍藏书地点
        self.admin_main_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.admin_main_frame.grid_remove()
        self.admin_main_label = customtkinter.CTkLabel(self.admin_main_frame, text="Admin Page", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.admin_main_label.grid(row=0, column=1, padx=30, pady=50)
        self.add_book_button = customtkinter.CTkButton(self.admin_main_frame, text="Add Book", command=self.gotoadd_event, width=200)
        self.add_book_button.grid(row=1, column=1, padx=30, pady=50)
        self.delete_book_button = customtkinter.CTkButton(self.admin_main_frame, text="Delete Book", command=self.gotodelete_event, width=200)
        self.delete_book_button.grid(row=2, column=1, padx=30, pady=50)
        self.update_button = customtkinter.CTkButton(self.admin_main_frame, text="Update overdays", command=self.gotoUpdate_event, width=200)
        self.update_button.grid(row=3, column=1, padx=30, pady=50)
        self.admin_back_button = customtkinter.CTkButton(self.admin_main_frame, text="Back", command=self.adminBackLogin_event, width=200)
        self.admin_back_button.grid(row=4, column=1, padx=30, pady=50)
        
        # 添加书籍界面
        self.add_book_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.add_book_frame.grid_remove()
        self.add_book_label = customtkinter.CTkLabel(self.add_book_frame, text="Add Book", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.add_book_label.grid(row=0, column=0, padx=30, pady=50)
        self.add_bookname_entry = customtkinter.CTkEntry(self.add_book_frame, width=200, placeholder_text="bookname")
        self.add_bookname_entry.grid(row=1, column=0, padx=30, pady=15)
        self.add_author_entry = customtkinter.CTkEntry(self.add_book_frame, width=200, placeholder_text="author")
        self.add_author_entry.grid(row=2, column=0, padx=30, pady=15)
        self.add_price_entry = customtkinter.CTkEntry(self.add_book_frame, width=200, placeholder_text="price")
        self.add_price_entry.grid(row=3, column=0, padx=30, pady=15)
        self.add_libid_entry = customtkinter.CTkEntry(self.add_book_frame, width=200, placeholder_text="libid")
        self.add_libid_entry.grid(row=4, column=0, padx=30, pady=15)
        self.add_num_entry = customtkinter.CTkEntry(self.add_book_frame, width=200, placeholder_text="num")
        self.add_num_entry.grid(row=5, column=0, padx=30, pady=15)
        self.add_readpath_entry = customtkinter.CTkEntry(self.add_book_frame, width=200, placeholder_text="readpath")
        self.add_readpath_entry.grid(row=6, column=0, padx=30, pady=15)
        self.add_book_button = customtkinter.CTkButton(self.add_book_frame, text="Add Book", command=self.add_book_event, width=200)
        self.add_book_button.grid(row=7, column=0, padx=30, pady=15)
        self.back_admin_button = customtkinter.CTkButton(self.add_book_frame, text="Back", command=self.addBackAdmin_event, width=200)
        self.back_admin_button.grid(row=8, column=0, padx=30, pady=15)
        
        # 删除书籍界面
        self.delete_book_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.delete_book_frame.grid_remove()
        self.delete_book_label = customtkinter.CTkLabel(self.delete_book_frame, text="Delete Book", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.delete_book_label.grid(row=0, column=0, padx=30, pady=50)
        self.delete_bookname_entry = customtkinter.CTkEntry(self.delete_book_frame, width=50, placeholder_text="bookname")
        self.delete_bookname_entry.grid(row=1, column=0, padx=30, pady=15)
        self.delete_author_entry = customtkinter.CTkEntry(self.delete_book_frame, width=50, placeholder_text="author")
        self.delete_author_entry.grid(row=2, column=0, padx=30, pady=15)
        self.delete_libid_entry = customtkinter.CTkEntry(self.delete_book_frame, width=50, placeholder_text="libid")
        self.delete_libid_entry.grid(row=3, column=0, padx=30, pady=15)
        self.delete_book_button = customtkinter.CTkButton(self.delete_book_frame, text="Delete Book", command=self.delete_book_event, width=200)
        self.delete_book_button.grid(row=4, column=0, padx=30, pady=15)
        self.back_admin_button = customtkinter.CTkButton(self.delete_book_frame, text="Back", command=self.deleteBackAdmin_event, width=200)
        self.back_admin_button.grid(row=5, column=0, padx=30, pady=15)
        
        self.read_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.read_frame.grid_remove()
        self.read_label = customtkinter.CTkLabel(self.read_frame, text="Read Book", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.read_label.grid(row=0, column=0, padx=30, pady=50)
        

    def errorLoginBackLogin_event(self):
        self.errorLogin_frame.grid_forget()
        self.login_frame.grid(row=0, column=1, columnspan=3, sticky="ns")
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsw")
        
    def login_event(self):
        print("Login pressed - username:", self.username_entry.get(), "password:", self.password_entry.get())
        self.login_frame.grid_forget()  # remove login frame
        self.sidebar_frame.grid_forget()
        user = login_db(self.username_entry.get(), self.radio_var.get())
        # user = True
        if user == 1:
            self.main_frame.grid(row=0, column=0, rowspan=4, columnspan=4, sticky="ns")
        elif user == 2:
            self.admin_main_frame.grid(row=0, column=0, rowspan=4, columnspan=4, sticky="ns")
        else:
            self.errorLogin_frame.grid(row=0, column=1, sticky="ns")

    def mainBackLogin_event(self):
        self.main_frame.grid_forget()  # remove main frame
        self.login_frame.grid(row=0, column=1, columnspan=3, sticky="ns")  # show login frame, sticky="ns"表示将窗口大小调整为适应窗口大小
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsw")
        
    def personalBackMain_event(self):
        self.personal_frame.grid_forget()  # remove personal frame
        self.sidePerson_frame.grid_forget()
        # self.textbox.grid_forget()
        self.main_frame.grid(row=0, column=0, rowspan=4, columnspan=4, sticky="ns")
    
    def selectBackMain_event(self):
        self.select_frame.grid_forget()  # remove personal frame
        self.main_frame.grid(row=0, column=0, rowspan=4, columnspan=4, sticky="ns")
    
    def brBackMain_event(self):
        self.br_frame.grid_forget()
        self.main_frame.grid(row=0, column=0, rowspan=4, columnspan=4, sticky="ns")
    
    def personal_event(self):
        print("personal pressed")
        self.main_frame.grid_forget()  # remove main frame
        self.afterBorrow_frame.grid_remove()
        self.sidePerson_frame.grid(row=0, column=0, rowspan=4, sticky="nsw")
        self.personal_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        # self.textbox.grid(row=0, column=1,  rowspan=4, columnspan=3, padx=(20, 0), pady=(20, 0), sticky="nsew")
        
    def br_event(self):
        print("Borrow pressed")
        self.main_frame.grid_forget()
        self.br_frame.grid_forget()
        self.read_frame.grid_forget()
        self.afterBorrow_frame.grid_forget()
        self.br_frame.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="nsew")
        self.reccomend_book()
    
    def select_event(self):
        print("Select pressed")
        self.main_frame.grid_forget()
        self.afterBorrow_frame.grid_forget()
        self.read_frame.grid_forget()
        self.select_frame.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="ns")

    def br2select_event(self):
        print("br2select pressed")
        self.br_frame.grid_forget()
        self.select_frame.grid(row=0, column=2, rowspan=4, columnspan=4, sticky="nsw")
    
    def sidebar_button_borrow_event(self):
        print("borrow pressed")
        #删除之前的内容
        for widget in self.personal_frame.winfo_children():
            widget.destroy()
        borrowed_books= get_borrowed_book(self.username_entry.get())
        # 按照借书时间排序，最新借的书在最前面，且对于每本书，显示书名和作者，以及还书按钮，
        # 如果书籍已经逾期，则显示逾期天数， 如果书籍已经还书，则显示还书日期，代替还书按钮
        # 如果书籍未逾期，且未还书，则显示延期按钮
        borrowed_books.sort(key=lambda x: x.borrowDate, reverse=True)
        index = 0
        for book in borrowed_books:
            book_label = customtkinter.CTkLabel(self.personal_frame, text=f"书名: {book.bookId}, 借书日期: {book.borrowDate}, 应还日期: {book.PreReturnDate}, 书籍藏书图书馆: {book.bookLibId}")
            book_label.grid(row=index+2, column=0, padx=5, pady=5)
            if book.returnDate is not None:
                return_label = customtkinter.CTkLabel(self.personal_frame, text=f"还书日期: {book.returnDate}")
                return_label.grid(row=index+2, column=1, padx=5, pady=5)
            else:
                return_button = customtkinter.CTkButton(self.personal_frame, text="还书", command=lambda b=book: self.return_book_event(b))
                return_button.grid(row=index+2, column=1, padx=5, pady=5)
                
            if book.overDays > 0:
                overdue_label = customtkinter.CTkLabel(self.personal_frame, text=f"逾期{book.overDays}天")
                overdue_label.grid(row=index+2, column=2, padx=5, pady=5)
            else:
                extend_button = customtkinter.CTkLabel(self.personal_frame, text="未逾期")
                extend_button.grid(row=index+2, column=2, padx=5, pady=5)
            index += 1
        
    def sidebar_button_reserve_event(self):
        print("reserve pressed")
        # 删除之前的内容
        for widget in self.personal_frame.winfo_children():
            widget.destroy()
        reserved_books = get_reserved_book(self.username_entry.get())
        
        # 按照预约时间排序，最新预约的书在最前面，且对于每本书，显示书名和作者，
        # 如果takeDate不为none，则显示取消预约按钮
        reserved_books.sort(key=lambda x: x.reserveDate, reverse=True)
        index = 0
        for book in reserved_books:
            book_label = customtkinter.CTkLabel(self.personal_frame, text=f"书名: {book.bookId}, 预约日期: {book.reserveDate}, 书籍藏书图书馆: {book.bookLibId}")
            book_label.grid(row=index+2, column=0, padx=5, pady=5)
            if book.takeDate is None:
                cancel_button = customtkinter.CTkButton(self.personal_frame, text="取消预约", command=lambda b=book: self.cancel_reserve_event(b))
                cancel_button.grid(row=index+2, column=1, padx=5, pady=5)
            else:
                take_label = customtkinter.CTkLabel(self.personal_frame, text=f"取书日期: {book.takeDate}")
                take_label.grid(row=index+2, column=1, padx=5, pady=5)
            index += 1
        
    def reccomend_book(self):
        print("reccomend event")
        books = get_reccomend_book()
        # 按照借阅次数排序，借阅次数最多的书在最前面，显示书名和作者，以及借书按钮和预约按钮
        books.sort(key=lambda x: x.bookBorrowTimes, reverse=True)
        index = 0
        for book in books:
            book_label = customtkinter.CTkLabel(self.br_frame, text=f"书名: {book.bookId}, 作者: {book.bookAuthor}, 藏书馆: {book.bookLibId}, 馆藏数量: {book.bookNum}")
            book_label.grid(row=index+2, column=0, padx=5, pady=5)
            if book.bookWillBeDel == 1:
                delete_button = customtkinter.CTkButton(self.br_frame, text="禁止BR", command=lambda b=book: self.delete_book_event(b))
                delete_button.grid(row=index+2, column=1, padx=5, pady=5)
            else:
                if book.bookStatus == 0:
                    borrow_button = customtkinter.CTkButton(self.br_frame, text="借书", command=lambda b=book: self.borrow_book_event(b, 0))
                    borrow_button.grid(row=index+2, column=1, padx=5, pady=5)
                else:
                    reserve_button = customtkinter.CTkButton(self.br_frame, text="预约", command=lambda b=book: self.reserve_book_event(b, 0))
                    reserve_button.grid(row=index+2, column=1, padx=5, pady=5)

            read_button = customtkinter.CTkButton(self.br_frame, text="阅读", command=lambda b=book: self.read_book_event(b, 0))
            read_button.grid(row=index+2, column=2, padx=5, pady=5)
            index += 1
    
    def search_event(self):
        print("Search pressed")
        self.afterBorrow_frame.grid_forget()
        bookname = self.search_bookname_entry.get()
        author = self.search_author_entry.get()
        books = get_book(bookname, author)
        # 按照借阅次数排序，借阅次数最多的书在最前面，显示书名和作者，以及借书按钮和预约按钮
        # 展示：书名，作者，价格，状态，借阅次数，预约次数，馆藏图书馆，馆藏数量
        # 如果状态为0，则显示借书按钮
        # 如果状态为1或者2，则显示预约按钮
        index = 0
        for book in books:
            book_label = customtkinter.CTkLabel(self.select_frame, text=f"书名: {book.bookId}, 作者: {book.bookAuthor}, 状态: {book.bookStatus}, 馆藏数量: {book.bookNum}")
            book_label.grid(row=index+2, column=0, padx=5, pady=5)
            if book.bookWillBeDel == 1:
                reserve_label = customtkinter.CTkLabel(self.select_frame, text="禁止")
                reserve_label.grid(row=index+2, column=1, padx=5, pady=5)
            else:
                if book.bookStatus == 0:
                    borrow_button = customtkinter.CTkButton(self.select_frame, text="借书", command=lambda b=book: self.borrow_book_event(b, 1))
                    borrow_button.grid(row=index+2, column=1, padx=5, pady=5)
                else:
                    reserve_button = customtkinter.CTkButton(self.select_frame, text="预约", command=lambda b=book: self.reserve_book_event(b, 1))
                    reserve_button.grid(row=index+2, column=1, padx=5, pady=5)
            read_button = customtkinter.CTkButton(self.br_frame, text="阅读", command=lambda b=book: self.read_book_event(b, 1))
            read_button.grid(row=index+2, column=2, padx=5, pady=5)
            index += 1
    
    
    def read_book_event(self, book, frame):
        print("read book pressed")
        self.select_frame.grid_forget()
        self.read_frame.grid(row=0, column=0, rowspan=4, columnspan=4, sticky="ns")
        # 读取书籍内容
        for widget in self.read_frame.winfo_children():
            widget.destroy()
        book_content = get_book_content(book.bookReadPath)
        self.book_content_label = customtkinter.CTkLabel(self.read_frame, text=book_content, font=customtkinter.CTkFont(size=20, weight="bold"))
        self.book_content_label.grid(row=1, column=0, padx=30, pady=50)
        if frame == 0:
            self.back_button = customtkinter.CTkButton(self.read_frame, text="Back", command=self.br_event, width=200)
            self.back_button.grid(row=2, column=0, padx=30, pady=50)
        else:
            self.back_button = customtkinter.CTkButton(self.read_frame, text="Back", command=self.search_event, width=200)
            self.back_button.grid(row=2, column=0, padx=30, pady=50)
    
    
    def return_book_event(self, book): # 只能在personal界面中调用 
        print("return book pressed")
        # 把returninfo的信息显示在afterBorrow_frame中
        returninfo = return_book(self.username_entry.get(), book.bookId, book.bookLibId, self.radio_var.get())
        for widget in self.afterBorrow_frame.winfo_children():
            widget.destroy()
        self.afterBorrow_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="ns")
        self.afterBorrow_label = customtkinter.CTkLabel(self.afterBorrow_frame, text="afterReturn:" + returninfo.fetchone()[0], font=customtkinter.CTkFont(size=20, weight="bold"))
        self.afterBorrow_label.grid(row=0, column=0, columnspan=3, padx=50, pady=50, sticky="ns")
        self.afterBorrow_button = customtkinter.CTkButton(self.afterBorrow_frame, text="OK", command=self.personal_event, width=200)
        self.afterBorrow_button.grid(row=1, column=1, padx=50, pady=50)
        # self.sidebar_button_borrow_event()
        
    def borrow_book_event(self, book, frame): 
        # frame表示是哪个frame的借书按钮, 0表示br_frame,1表示select_frame
        print("borrow book pressed")
        returninfo = borrow_book(self.username_entry.get(), book.bookId, book.bookLibId, self.radio_var.get())
        for widget in self.afterBorrow_frame.winfo_children():
            widget.destroy()
        if(frame == 0):
            self.afterBorrow_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="ns")
            self.afterBorrow_label = customtkinter.CTkLabel(self.afterBorrow_frame, text="afterBorrow:" + returninfo.fetchone()[0], font=customtkinter.CTkFont(size=20, weight="bold"))
            self.afterBorrow_label.grid(row=0, column=0, columnspan=3, padx=50, pady=50, sticky="ns")
            self.afterBorrow_button = customtkinter.CTkButton(self.afterBorrow_frame, text="OK", command=self.br_event, width=200)
            self.afterBorrow_button.grid(row=1, column=1, padx=50, pady=50)
        else:
            self.afterBorrow_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="ns")
            self.afterBorrow_label = customtkinter.CTkLabel(self.afterBorrow_frame, text="afterBorrow:" + returninfo.fetchone()[0], font=customtkinter.CTkFont(size=20, weight="bold"))
            self.afterBorrow_label.grid(row=0, column=0, columnspan=3, padx=50, pady=50, sticky="ns")
            self.afterBorrow_button = customtkinter.CTkButton(self.afterBorrow_frame, text="OK", command=self.search_event, width=200)
            self.afterBorrow_button.grid(row=1, column=1, padx=50, pady=50)
        
    def reserve_book_event(self, book, frame):
        print("reserve book pressed")
        for widget in self.afterBorrow_frame.winfo_children():
            widget.destroy()
        returninfo = reserve_book(self.username_entry.get(), book.bookId, book.bookLibId, self.radio_var.get())
        if frame == 0:
            self.afterBorrow_frame.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="ns")
            self.afterBorrow_label = customtkinter.CTkLabel(self.afterBorrow_frame, text="afterReserve:" + returninfo, font=customtkinter.CTkFont(size=20, weight="bold"))
            self.afterBorrow_label.grid(row=0, column=0, columnspan=3, padx=50, pady=50, sticky="ns")
            self.afterBorrow_button = customtkinter.CTkButton(self.afterBorrow_frame, text="OK", command=self.br_event, width=200)
            self.afterBorrow_button.grid(row=1, column=1, padx=50, pady=50)
        else:
            self.afterBorrow_frame.grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="ns")
            self.afterBorrow_label = customtkinter.CTkLabel(self.afterBorrow_frame, text="afterReserve:" + returninfo.fetchone, font=customtkinter.CTkFont(size=20, weight="bold"))
            self.afterBorrow_label.grid(row=0, column=0, columnspan=3, padx=50, pady=50, sticky="ns")
            self.afterBorrow_button = customtkinter.CTkButton(self.afterBorrow_frame, text="OK", command=self.search_event, width=200)
            self.afterBorrow_button.grid(row=1, column=1, padx=50, pady=50)
    
    def cancel_reserve_event(self, book):
        print("cancel reserve pressed")
        returninfo = cancel_reserve(self.username_entry.get(), book.bookId, book.bookLibId, book.reserveLibId)
        for widget in self.afterBorrow_frame.winfo_children():
                widget.destroy()
        self.afterBorrow_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="ns")
        self.afterBorrow_label = customtkinter.CTkLabel(self.afterBorrow_frame, text="aftercancleReserve:" + returninfo, font=customtkinter.CTkFont(size=20, weight="bold"))
        self.afterBorrow_label.grid(row=0, column=0, columnspan=3, padx=50, pady=50, sticky="ns")
        self.afterBorrow_button = customtkinter.CTkButton(self.afterBorrow_frame, text="OK", command=self.personal_event, width=200)
        self.afterBorrow_button.grid(row=1, column=1, padx=50, pady=50)
    
    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)
    
    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)
    
    def gotoadd_event(self):
        self.admin_main_frame.grid_forget()
        self.add_book_frame.grid_forget()
        self.afterBorrow_frame.grid_forget()
        self.add_book_frame.grid(row=0, column=0, rowspan=4, columnspan=3, sticky="ns")
    
    def add_book_event(self):
        print("add book pressed")
        # 如果什么都没有输入，则不进行操作
        bookname = self.add_bookname_entry.get()
        author = self.add_author_entry.get()
        price = self.add_price_entry.get()
        libid = self.add_libid_entry.get()
        num = self.add_num_entry.get()
        paths = self.add_readpath_entry.get()
        if bookname == "" or author == "" or price == "" or libid == "" or num == "" or paths == "":
            returninfo = "信息不完整"
        else:
            returninfo = add_book(bookname, author, price, libid, num, paths)
        self.add_book_frame.grid_forget()
        for widget in self.afterBorrow_frame.winfo_children():
            widget.destroy()
        self.afterBorrow_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="ns")
        self.afterBorrow_label = customtkinter.CTkLabel(self.afterBorrow_frame, text="afteraddbook:" + returninfo, font=customtkinter.CTkFont(size=20, weight="bold"))
        self.afterBorrow_label.grid(row=0, column=0, columnspan=3, padx=50, pady=50, sticky="ns")
        self.afterBorrow_button = customtkinter.CTkButton(self.afterBorrow_frame, text="OK", command=self.gotoadd_event, width=200)
        self.afterBorrow_button.grid(row=1, column=1, padx=50, pady=50)
        
        
    def gotodelete_event(self):
        self.admin_main_frame.grid_forget()
        self.delete_book_frame.grid_forget()
        self.afterBorrow_frame.grid_forget()
        self.delete_book_frame.grid(row=0, column=0, rowspan=4, columnspan=4, sticky="ns")
    
    def delete_book_event(self):
        print("delete book pressed")
        bookname = self.delete_bookname_entry.get()
        author = self.delete_author_entry.get()
        libid = self.delete_libid_entry.get()
        if bookname == "" or author == "" or libid == "":
            returninfo = "信息不完整"
        else:
            returninfo = delete_book(bookname, author, libid)
        self.delete_book_frame.grid_forget()
        for widget in self.afterBorrow_frame.winfo_children():
            widget.destroy()
        self.afterBorrow_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="ns")
        self.afterBorrow_label = customtkinter.CTkLabel(self.afterBorrow_frame, text="afterdeletebook:" + returninfo, font=customtkinter.CTkFont(size=20, weight="bold"))
        self.afterBorrow_label.grid(row=0, column=0, columnspan=3, padx=50, pady=50, sticky="ns")
        self.afterBorrow_button = customtkinter.CTkButton(self.afterBorrow_frame, text="OK", command=self.gotodelete_event, width=200)
        self.afterBorrow_button.grid(row=1, column=1, padx=50, pady=50)
            
    def gotoUpdate_event(self):
        update_overdays()
    
    def adminBackLogin_event(self):
        self.admin_main_frame.grid_forget()
        self.login_frame.grid(row=0, column=1, columnspan=3, sticky="ns")
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsw")
        
    def addBackAdmin_event(self):
        self.add_book_frame.grid_forget()
        self.admin_main_frame.grid(row=0, column=0, rowspan=4, columnspan=4, sticky="ns")
    
    def deleteBackAdmin_event(self):
        self.delete_book_frame.grid_forget()
        self.admin_main_frame.grid(row=0, column=0, rowspan=4, columnspan=4, sticky="ns")
        
if __name__ == "__main__":
    app = App()
    app.mainloop()