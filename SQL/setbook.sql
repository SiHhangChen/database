start transaction;
-- 把书籍的状态改为不可预约和借阅
SET SQL_SAFE_UPDATES = 0;
update borrow
set borrow.overDays = datediff(curdate(), borrow.PreReturnDate)
where borrow.returnDate is null
  and borrow.PreReturnDate < curdate();
SET SQL_SAFE_UPDATES = 1;
commit;
