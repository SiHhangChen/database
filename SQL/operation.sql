call borrowBook('R001', 'B001', 'E', 'E');
call borrowBook('R004', 'B005', 'W', 'E');

call borrowBook('R001', 'B002', 'E', 'E');
call borrowBook('R001', 'B003', 'E', 'E');
call borrowBook('R001', 'B004', 'E', 'E');
call borrowBook('R001', 'B001', 'E', 'W');

DELETE FROM borrow where stuId = 'R004' and bookId = 'B005' and borrowLibId = 'W' and bookLibId = 'E';
call returnBook('R001', 'B001', 'E', 'E');
call returnBook('R004', 'B005', 'W', 'E');
call returnBook('R003', 'B003', 'H', 'E');
call returnBook('R002', 'B002', 'W', 'W');

insert reserve (bookId, stuId, reserveLibId, bookLibId, reserveDate, takeDate)
VALUES
('B001', 'R001', 'W', 'E', CURDATE(), NULL),
('B001', 'R001', 'W', 'E', CURDATE(), NULL);

select * from reserve where stuId = 'R001' and bookId = 'B001' and bookLibId = 'E' and reserveDate = CURDATE();

select minAvailableId('E');