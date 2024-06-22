-- 该测试样例是根据数据库规则设计好的
-- 不需要事先定义任何存储过程和触发器，定义好基本表后直接运行即可
-- 对测试样例有任何问题都可以联系yxy助教

-- 插入系别数据
insert into department (depId, depName)
values
('D001', 'CS'),
('D002', 'EE'),
('D003', 'ME');

insert into library (LibId, LibName, LibAddress)
VALUES
('E', 'East Library', 'Engineering Building'),
('W', 'West Library', 'West Building'),
('H', 'High Library', 'Humanities Building');

-- 插入读者数据
insert into student (stuId, stuName, stuMajor, stuGrade)
values
('R001', 'Alice', 'CS', 1),
('R002', 'Bob', 'EE', 2),
('R003', 'Charlie', 'ME', 3),
('R004', 'David', 'CS', 1),
('R005', 'Eve', 'EE', 2),
('R006', 'Frank', 'ME', 3);

-- 插入图书数据
insert into book (bookId, bookName, bookAuthor, bookPrice, bookStatus, bookBorrowTimes, bookReserveTimes, bookLibId, bookNum, bookReadPath)
VALUES 
('B001', 'The Hobbit', 'J.R.R. Tolkien', 18.99, 2, 4, 5, 'E', 0, "D:\\MySQL\\read\\The Hobbit-J.R.R. Tolkien.txt"), -- 预约次数最多比借阅次数少藏书本次，
('B002', 'Harry Potter and the Chamber of Secrets', 'J.K. Rowling', 25.50, 0, 2, 1, 'E', 1, "D:\\MySQL\\read\\Harry Potter and the Chamber of Secrets-J.K. Rowling.txt"),
('B003', 'Harry Potter and the Philosopher\'s Stone', 'J.K. Rowling', 14.7, 0, 21, 10, 'E', 5, "D:\\MySQL\\read\\Harry Potter and the Philosopher's Stone-J.K. Rowling.txt"),
('B004', 'Learning MySQL: Get a Handle on Your Data', 'Seyed M.M. (Saied) Tahaghoghi, Hugh E. Williams', 29.99, 1, 5, 1, 'E', 0, "D:\\MySQL\\read\\Learning MySQL-Get a Handle on Your Data-Seyed M.M. (Saied) Tahaghoghi, Hugh E. Williams.txt"),
('B005', 'The Catcher in the Rye', 'J.D. Salinger', 11.20, 1, 2, 2, 'E', 0, "D:\\MySQL\\read\\The Catcher in the Rye-J.D. Salinger.txt"),
('B006', 'Animal Farm', 'George Orwell', 8.99, 2, 1, 3, 'E', 0, "D:\\MySQL\\read\\Animal Farm-George Orwell.txt"),
('B007', 'Test your trigger here', 'TA', 10.4, 0, 0, 0, 'E', 1, "D:\\MySQL\\read\\Test your trigger here-TA.txt"),

('B001', 'To Kill a Mockingbird', 'Harper Lee', 12.99, 2, 15, 15, 'W',0, "D:\\MySQL\\read\\To Kill a Mockingbird-Harper Lee.txt"),
('B002', '1984', 'George Orwell', 10.50, 2, 2, 5, 'W', 0, "D:\\MySQL\\read\\1984-George Orwell.txt"),
('B003', 'MySQL Cookbook: Solutions for Database Developers and Administrators', 'Paul DuBois', 35.50, 2, 1, 6, 'W', 0, "D:\\MySQL\\read\\MySQL Cookbook-Solutions for Database Developers and Administrators-Paul DuBois.txt"),

('B001', 'Pride and Prejudice', 'Jane Austen', 14.25, 0, 2, 1, 'H', 1, "D:\\MySQL\\read\\Pride and Prejudice-Jane Austen.txt"),
('B002', 'Brave New World', 'Aldous Huxley', 13.80, 1, 1, 0, 'H', 0, "D:\\MySQL\\read\\Brave New World-Aldous Huxley.txt"),
('B003', 'The Hobbit', 'J.R.R. Tolkien', 18.99, 0, 4, 2, 'H', 1, "D:\\MySQL\\read\\The Hobbit-J.R.R. Tolkien.txt");


-- 插入借阅数据
INSERT INTO borrow (bookId, stuId, bookLibId, borrowDate, PreReturnDate, returnDate, borrowLibId, returnLibId, overDays)
VALUES
('B001', 'R001', 'E', '2024-03-01', '2024-03-31', '2024-03-21', 'E', 'E', 0),
('B003', 'R002', 'E', '2024-03-03', '2024-04-02', '2024-03-29', 'E', 'E', 0),
('B005', 'R004', 'E', '2024-03-05', '2024-04-04', '2024-03-25', 'E', 'W', 0),
('B001', 'R005', 'W', '2024-03-07', '2024-04-06', '2024-03-27', 'W', 'W', 0),
('B002', 'R006', 'W', '2024-03-09', '2024-04-08', '2024-03-29', 'W', 'W', 0),
('B003', 'R001', 'H', '2024-03-11', '2024-04-10', '2024-03-15', 'H', 'H', 0),
('B001', 'R002', 'H', '2024-03-13', '2024-04-12', '2024-04-18', 'E', 'H', 6),
('B002', 'R003', 'H', '2024-03-15', '2024-04-14', '2024-04-03', 'H', 'H', 0),
('B003', 'R004', 'H', '2024-03-17', '2024-04-16', '2024-04-05', 'H', 'W', 0),
('B001', 'R005', 'H', '2024-03-19', '2024-04-18', null, 'H', null, 0),
('B007', 'R006', 'E', '2024-03-01', '2024-03-31', null, 'E', null, 0),
('B003', 'R003', 'E', '2024-03-29', '2024-04-28', null, 'H', null, 0),
('B002', 'R002', 'W', '2024-03-29', '2024-04-28', null, 'H', null, 0),
('B001', 'R003', 'E', '2024-03-30', '2024-04-29', null, 'H', null, 0);

-- 插入预约数据
insert into reserve (bookId, stuId, reserveLibId, bookLibId, reserveDate, takeDate)
values
('B003', 'R003', 'H', 'E', '2024-03-09', '2024-03-29'),
('B001', 'R005', 'H', 'H', '2024-03-11', null),
('B003', 'R001', 'E', 'E', '2024-03-01', '2024-03-03'),
('B001', 'R005', 'W', 'W', '2024-03-05', '2024-03-07'),
('B003', 'R003', 'H', 'E', '2024-03-17', '2024-03-29'),
('B002', 'R001', 'W', 'W', '2024-03-19', null);


-- 插入管理员数据
insert into administrator (adminId, adminLibId, adminName, adminPhone, adminEmail, adminAge, adminAddress)
values
('A001', 'E', 'Alice', '12345678904', '456.com', 33, 'Alice\'s address'),
('A001', 'W', 'Bob', '12345678905', '567.com', 34, 'Bob\'s address'),
('A001', 'H', 'Charlie', '12345678906', '678.com', 35, 'Charlie\'s address'),
('A002', 'E', 'David', '12345678907', '789.com', 36, 'David\'s address'),
('A002', 'W', 'Ever', '12345678908', '890.com', 37, 'Ever\'s address'),
('A002', 'H', 'Franker', '12345678909', '901.com', 38, 'Franker\'s address');

-- 插入馆长数据
insert into curator (curId, curLibId, curName, curPhone, curEmail, curAge, curAddress)
values
('C001', 'E', 'Eve', '12345678901', '123.com', 30, 'Eve\'s address'),
('C002', 'W', 'Frank', '12345678902', '234.com', 31, 'Frank\'s address'),
('C003', 'H', 'Grace', '12345678903', '345.com', 32, 'Grace\'s address');
