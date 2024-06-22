from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String,Float, Text, DateTime, ForeignKey, func

class Base(DeclarativeBase):
    pass

class library(Base):
    __tablename__ = 'library'
    LibId = Column(String(8), primary_key=True)
    LibName = Column(String(100), primary_key=True)
    LibAddress = Column(String(100))

class administrator(Base):
    __tablename__ = 'administrator'
    adminId = Column(String(18), primary_key=True)
    adminLibId = Column(String(8), primary_key=True)
    adminName = Column(String(20))
    adminPhone = Column(String(11))
    adminEmail = Column(String(50))
    adminAge = Column(Integer)
    adminAddress = Column(String(100))

class curator(Base):
    __tablename__ = 'curator'
    curId = Column(String(18), primary_key=True)
    curLibId = Column(String(8), primary_key=True)
    curName = Column(String(20))
    curPhone = Column(String(11))
    curEmail = Column(String(50))
    curAge = Column(Integer)
    curAddress = Column(String(100))

class book(Base):
    __tablename__ = 'book'
    bookId = Column(String(8), primary_key=True)
    bookName = Column(String(100))
    bookAuthor = Column(String(50))
    bookPrice = Column(Float)
    bookStatus = Column(Integer, default=0)
    bookBorrowTimes = Column(Integer, default=0)
    bookReserveTimes = Column(Integer, default=0)
    bookLibId = Column(String(8), ForeignKey('library.LibId'), primary_key=True)
    bookWillBeDel = Column(Integer, default=0)
    bookNum = Column(Integer)
    bookReadPath = Column(String(255))
    
class student(Base):
    __tablename__ = 'student'
    stuId = Column(String(10), primary_key=True)
    stuName = Column(String(20))
    stuMajor = Column(String(50))
    stuGrade = Column(Integer)

class borrows(Base):
    __tablename__ = 'borrow'
    bookId = Column(String(8), ForeignKey('book.bookId'), primary_key=True)
    stuId = Column(String(10), ForeignKey('student.stuId'), primary_key=True)
    bookLibId = Column(String(8), ForeignKey('book.bookLibId'), primary_key=True)
    borrowDate = Column(DateTime, primary_key=True)
    PreReturnDate = Column(DateTime, primary_key=True)
    returnDate = Column(DateTime, default=None)
    borrowLibId = Column(String(8))
    returnLibId = Column(String(8), default=None)
    overDays = Column(Integer, default=0)

class reserve(Base):
    __tablename__ = 'reserve'
    bookId = Column(String(8), ForeignKey('book.bookId'), primary_key=True)
    stuId = Column(String(10), ForeignKey('student.stuId'), primary_key=True)
    reserveLibId = Column(String(8), primary_key=True)
    bookLibId = Column(String(8), ForeignKey('book.bookLibId'), primary_key=True)
    reserveDate = Column(DateTime,default=func.now(), primary_key=True)
    takeDate = Column(DateTime, default=None)

class department(Base):
    __tablename__ = 'department'
    depId = Column(String(8), primary_key=True)
    depName = Column(String(50))