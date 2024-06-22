delimiter //
create trigger reserve_add after insert on reserve for each row
begin
    SET SQL_SAFE_UPDATES = 0;
	SET FOREIGN_KEY_CHECKS = 0;
    update book 
    set book.bookStatus = 2 
    where book.bookId = new.bookId 
      and book.bookLibId = new.bookLibId;

    update book 
    set book.bookReserveTimes = book.bookReserveTimes + 1 
    where book.bookId = new.bookId 
      and book.bookLibId = new.bookLibId;
    SET FOREIGN_KEY_CHECKS = 1;
	SET SQL_SAFE_UPDATES = 1;
end //
delimiter ;

delimiter //
create trigger takeBook after update on reserve for each row
begin
    declare counts int default 0;
    -- 检查是否还有人在预约该书
    select count(*) into counts 
    from reserve 
    where reserve.bookId = old.bookId 
      and reserve.bookLibId = old.bookLibId 
      and reserve.takeDate is null;
    -- 若没有人在预约该书，则将该书的状态改为不可借，因为这个地方只是表示有一个人拿到了预约的书籍
    if counts = 0 then
        SET SQL_SAFE_UPDATES = 0;
        SET FOREIGN_KEY_CHECKS = 0;
        update book 
        set book.bookStatus = 1 
        where book.bookId = old.bookId 
            and book.bookLibId = old.bookLibId;
        SET FOREIGN_KEY_CHECKS = 1;
	    SET SQL_SAFE_UPDATES = 1;
    end if;
end //
delimiter ;

delimiter //
create trigger reserve_del after delete on reserve for each row
begin
    declare counts int default 0;
    -- 检查是否还有人在预约该书
    select count(*) into counts 
    from reserve 
    where reserve.bookId = old.bookId 
      and reserve.bookLibId = old.bookLibId 
      and reserve.takeDate is null;
    -- 若没有人在预约该书，则将该书的状态改为不可借，因为这个地方只是表示有一个人拿到了预约的书籍
    if counts = 0 then
        SET SQL_SAFE_UPDATES = 0;
        SET FOREIGN_KEY_CHECKS = 0;
        update book 
        set book.bookStatus = 1 
        where book.bookId = old.bookId 
          and book.bookLibId = old.bookLibId;
        SET FOREIGN_KEY_CHECKS = 1;
        SET SQL_SAFE_UPDATES = 1;
    end if;
end //
