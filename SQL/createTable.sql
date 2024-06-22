create table library(
    LibId char(8), 
    LibName varchar(100),
    LibAddress varchar(100),
    constraint LibPK primary key(LibId, LibName)
);

create table administrator(
    adminId char(18),
    adminLibId char(8),
    adminName varchar(20),
    adminPhone char(11),
    adminEmail varchar(50),
    adminAge int,
    adminAddress varchar(100),
    constraint adminPK primary key(adminId, adminLibId),
    constraint adminFK foreign key(adminLibId) references library(LibId)
);

create table curator(
    curId char(18),
    curLibId char(8),
    curName varchar(20),
    curPhone char(11),
    curEmail varchar(50),
    curAge int,
    curAddress varchar(100),
    constraint curPK primary key(curId, curLibId),
    constraint curFK foreign key(curLibId) references library(LibId)
);

create table book(
    bookId char(8),
    bookName varchar(100),
    bookAuthor varchar(50),
    bookPrice float,
    bookStatus int default 0, 
    bookBorrowTimes int default 0, 
    bookReserveTimes int default 0,
    bookLibId char(8), 
    bookNum int,
    bookWillBeDel int default 0,
    bookReadPath varchar(255),
    constraint bookPK primary key(bookId, bookLibId),
    constraint bookBS check(bookStatus in (0, 1, 2)),
    constraint bookWBDC check(bookWillBeDel in (0, 1)),
    constraint bookFK foreign key(bookLibId) references library(LibId)
);

create table student(
    stuId char(10), 
    stuName varchar(20), 
    stuMajor varchar(50), 
    stuGrade int, 
    constraint stuPK primary key(stuId)
);

create table borrow(
    bookId char(8), 
    stuId char(10), 
    bookLibId char(8), 
    borrowDate date, 
    PreReturnDate date, 
    returnDate date default null, 
    borrowLibId char(8),
    returnLibId char(8) default null, 
    overDays int default 0,
    constraint borrowPK primary key(bookId, stuId, bookLibId, borrowDate, PreReturnDate),
    constraint borrowFK foreign key(bookId, bookLibId) references book(bookId, bookLibId),
    constraint stuFK foreign key(stuId) references student(stuId)
);

create table reserve(
    bookId char(8), 
    stuId char(10), 
    reserveLibId char(8), 
    bookLibId char(8), 
    reserveDate date default (curdate()), 
    takeDate date default null, 
    constraint reservePK primary key(bookId, stuId, reserveDate, bookLibId),
    constraint takeDateCK check(takeDate >= reserveDate),
    constraint reserveFK foreign key(bookId, bookLibId) references book(bookId, bookLibId),
    constraint stuFK2 foreign key(stuId) references student(stuId)
);

create table department(
    depId char(8),
    depName varchar(50),
    constraint depPK primary key(depId)
);