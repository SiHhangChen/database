from sqlalchemy import create_engine,Table,Column,Integer,String,MetaData,ForeignKey,DateTime,text, func, cast, Date, update, and_
from sqlalchemy.orm import scoped_session, sessionmaker
import random
from model import *

engine = create_engine(
        "mysql+pymysql://root:123456789@127.0.0.1:3306/lab2",
        echo=True,  # echo 设为 True 会打印出实际执行的 sql，调试的时候更方便
        future=True,  # 使用 SQLAlchemy 2.0 API，向后兼容
        pool_size=5, # 连接池的大小默认为 5 个，设置为 0 时表示连接无限制
        pool_recycle=3600, # 设置时间以限制数据库自动断开
    )

metaData = MetaData()
metaData.bind = engine

db_session = scoped_session(
    sessionmaker(
        autoflush=False,
        bind=engine
    )
)

session = db_session()

def init_db():
    metaData.create_all(engine, checkfirst=True)
    
def drop_db():
    metaData.drop_all(engine, checkfirst=True)
    
def login_db(username, libId):
    info = session.query(administrator).filter(administrator.adminId == username, administrator.adminLibId == libId).first()
    if info == None:
        info = session.query(student).filter(student.stuId == username).first()
        if info == None:
            return 0
        return 1
    return 2
        
def get_book(bookname, author):
    books = session.query(book).filter(book.bookName == bookname, book.bookAuthor == author).all()
    return books

def get_borrowed_book(username):
    borrowed = session.query(borrows).filter(borrows.stuId == username).all()
    return borrowed

def get_reserved_book(username):
    reserved = session.query(reserve).filter(reserve.stuId == username).all()
    return reserved

def reserve_book(stuId, bookId, bookLibId, reserveLibId):
    reserve_info = session.query(reserve).filter(reserve.stuId == stuId, reserve.bookId == bookId, reserve.bookLibId == bookLibId, cast(reserve.reserveDate, Date) == cast(func.now(), Date)).all()
    if len(reserve_info) != 0:
        return "you have reserved this book today"
    newreserve = reserve(stuId=stuId, bookId=bookId, bookLibId=bookLibId, reserveLibId=reserveLibId, reserveDate=func.now())
    session.add(newreserve) 
    session.commit()
    reserve_info = session.query(reserve).filter(reserve.stuId == stuId, reserve.bookId == bookId, reserve.bookLibId == bookLibId, cast(reserve.reserveDate, Date) == cast(func.now(), Date)).all()
    if len(reserve_info) == 0:
        return "Reserve Fail"
    return "Reserve Success"
    
def cancel_reserve(stuId, bookId, bookLibId, reserveLibId):
    reserve_info = session.query(reserve).filter(reserve.stuId == stuId, reserve.bookId == bookId, reserve.bookLibId == bookLibId, reserve.takeDate == None).all()
    if len(reserve_info) == 0:
        return "you have not reserved this book"
    cancel = session.query(reserve).filter(reserve.stuId == stuId, reserve.bookId == bookId, reserve.bookLibId == bookLibId, reserve.reserveLibId == reserveLibId, reserve.takeDate == None).first()
    session.delete(cancel)
    session.commit()
    reserve_info = session.query(reserve).filter(reserve.stuId == stuId, reserve.bookId == bookId, reserve.bookLibId == bookLibId, reserve.takeDate == None).all()
    if len(reserve_info) != 0:
        return "Cancel Reserve Fail"
    return "Cancel Reserve Success"

def borrow_book(stuId, bookId, bookLibId, borrowLibId):
    return_info = session.execute(text("call borrowBook(:stuId, :bookId, :borrowLibId, :bookLibId)")
                            , {'stuId':stuId, 'bookId':bookId, 'borrowLibId':borrowLibId, 'bookLibId':bookLibId})
    session.commit()
    return return_info
    
def return_book(stuId, bookId, bookLibId, returnLibId):
    return_info = session.execute(text("call returnBook(:stuId, :bookId, :returnLibId, :bookLibId)")
                            , {'stuId':stuId, 'bookId':bookId, 'returnLibId':returnLibId, 'bookLibId':bookLibId})
    session.commit()
    return return_info
    
def get_reccomend_book():
    rec = session.query(book).order_by(book.bookBorrowTimes.desc()).limit(5).all()
    return rec

def random_LibId():
    lib = ['E', 'W', 'H']
    return lib[random.randint(0, 2)]

def add_book(bookName, bookAuthor, bookPrice, bookLibId, bookNum, bookReadPath):
    bookId = session.query(func.minAvailableId(bookLibId)).first()[0]
    newbook = book(bookId=bookId, bookName=bookName, bookAuthor=bookAuthor, bookPrice=bookPrice, bookLibId=bookLibId, bookNum=bookNum, bookStatus=0, bookBorrowTimes=0, bookReserveTimes=0, bookReadPath=bookReadPath, bookWillBeDel=0)
    session.add(newbook)
    session.commit()
    return "添加成功"
    
def delete_book(bookName, author, bookLibId):
    deletes = session.query(book).filter(book.bookName == bookName, book.bookAuthor == author, book.bookLibId == bookLibId).first()
    if deletes == None:
        return "不存在这本书"
    else:
        if deletes.bookStatus == 0:
            borrow_info = session.query(borrows).filter(borrows.bookId == deletes.bookId, borrows.bookLibId == bookLibId).all()
            for borrow in borrow_info:
                session.delete(borrow)
            session.commit()
            reserve_info = session.query(reserve).filter(reserve.bookId == deletes.bookId, reserve.bookLibId == bookLibId).all()
            for reservebook in reserve_info:
                session.delete(reservebook)
            session.commit()
            session.delete(deletes)
            session.commit()
            return "删除成功"
        else:
            deletes.bookWillBeDel = 1
            session.commit()
            return "书籍被借出"

def get_book_content(path):
    with open(path, 'r') as f:
        return f.read()       
                
def update_overdays():
    # 写一个事务，更新逾期天数
    try:
    # 开始事务
        with session.begin():
            # 更新未还书籍的逾期时间
            stmt = (
                update(borrows)
                .where(
                    and_(
                        borrows.returnDate == None,
                        borrows.PreReturnDate < func.curdate()
                    )
                )
                .values(overDays=func.datediff(func.curdate(), borrows.PreReturnDate))
            )
            session.execute(stmt)

    # 提交事务
        session.commit()
    except Exception as e:
        # 出现异常时回滚事务
        session.rollback()
        print("Error: ", e)

if __name__ == '__main__':
    # user = login_db('R001')
    # borrowed1 = get_reserved_book('R001')
    # borrowed1 = get_borrowed_book('R003')
    # borrowed1 = session.query(book).all()
    
    update_overdays()
    
    # books = get_book('The Hobbit', 'J.R.R. Tolkien')
    
    
    # print("\n\n\n\n\n\n")
    # index = 0
    # for b in books:
    #     print(b.bookId, b.bookName, b.bookAuthor, b.bookPrice, b.bookStatus, b.bookBorrowTimes, b.bookReserveTimes, b.bookLibId, b.bookNum, b.bookWillBeDel)
    #     print(b.bookReadPath)
    #     # 根据路径读取文件，打印文件内容
    #     with open(b.bookReadPath, 'r') as f:
    #         print(f.read())
    # print(user.stuId, user.stuName, user.stuMajor, user.stuGrade)
    # index = 0
    # for borrows1 in borrowed1:
    #     print(borrows1.bookId, borrows1.stuId, borrows1.borrowDate, borrows1.PreReturnDate, borrows1.returnDate, borrows1.borrowLibId, borrows1.returnLibId, borrows1.overDays)
    #     index += 1
    # index = 0
    # for reserves1 in borrowed1:
    #     print(reserves1.bookId, reserves1.stuId, reserves1.reserveDate, reserves1.takeDate, reserves1.reserveLibId, reserves1.bookLibId)
    #     index += 1
    # index = 0
    # for books1 in borrowed1:
    #     print(books1.bookId, books1.bookName, books1.bookAuthor, books1.bookPrice, books1.bookStatus, books1.bookBorrowTimes, books1.bookReserveTimes, books1.bookLibId, books1.bookNum)
    #     index += 1
    # print("\n\n\n\n\n\n")
    # add_book('test', 'test', 10, 'E', 10)
    # delete_book('test', 'test', 'E')
    # returninfo = delete_book('The Hobbit', 'J.R.R. Tolkien', 'E')
    # print(returninfo)
    # returninfo = return_book('R003', 'B001', 'E', 'H')
    # print(returninfo.fetchone())
    # returninfo = delete_book('The Hobbit', 'J.R.R. Tolkien', 'E')
    # print(returninfo)
    # returninfo = reserve_book('R001', 'B001', 'E', 'E')
    # print('\n', returninfo, '\n')
    # returninfo = reserve_book('R001', 'B001', 'E', 'W')
    # print(returninfo)
    # returninfo = reserve_book('R001', 'B002', 'E', 'E')
    # print(returninfo)
    # returninfo = cancel_reserve('R001', 'B001', 'E', 'E')
    # print(returninfo)
    # returninfo = cancel_reserve('R001', 'B001', 'E', 'W')
    # print(returninfo)
    # borrow_book('R001', 'B003', 'H', 'E')
    # returninfo = return_book('R003', 'B003', 'E', 'H')
    # returninfo = borrow_book('R003', 'B003', 'E', 'H')
    # print(returninfo.fetchone())
    # returninfo = borrow_book('R003', 'B002', 'E', 'H')
    # print(returninfo.fetchone())
    # returninfo = borrow_book('R003', 'B007', 'E', 'H')
    # print(returninfo.fetchone())
    # returninfo = borrow_book('R003', 'B003', 'H', 'H')
    # print(returninfo.fetchone())
    # print("\n\n\n\n\n\n")
    # borrowed2 = get_reserved_book('R001')
    # borrowed2 = session.query(book).all()
    # borrowed2 = get_borrowed_book('R003')
    # index = 0
    # for borrows2 in borrowed2:
    #     print(borrows2.bookId, borrows2.stuId, borrows2.borrowDate, borrows2.PreReturnDate, borrows2.returnDate, borrows2.borrowLibId, borrows2.returnLibId, borrows2.overDays)
    #     index += 1
    # index = 0
    # for reserves2 in borrowed2:
    #     print(reserves2.bookId, reserves2.stuId, reserves2.reserveDate, reserves2.takeDate, reserves2.reserveLibId, reserves2.bookLibId)
    #     index += 1
    # index = 0
    # for books2 in borrowed2:
    #     print(books2.bookId, books2.bookName, books2.bookAuthor, books2.bookPrice, books2.bookStatus, books2.bookBorrowTimes, books2.bookReserveTimes, books2.bookLibId, books2.bookNum)
    #     index += 1
    # print("\n\n\n\n\n\n")
    
