delimiter //
create procedure returnBook(In stuId char(10), in bookId char(8), in returnLibId char(8), in bookLibId char(8))
begin
    declare counts int default 0;
    declare stuIdTmp char(10);
    declare borrowLibIdTmp char(8);
    -- 检查是否借阅了本书
    select count(*) into counts 
    from borrow 
    where borrow.bookId = bookId 
      and borrow.stuId = stuId 
      and borrow.bookLibId = bookLibId 
      and borrow.returnDate is null;
    if (counts > 0) then
        SET SQL_SAFE_UPDATES = 0;
		SET FOREIGN_KEY_CHECKS = 0;
        -- 更新借书表，将还书日期设置为当前日期
        update borrow 
        set borrow.returnDate = curdate(),
			borrow.returnLibId = returnLibId,
            borrow.overDays = datediff(curdate(), borrow.PreReturnDate)
		where borrow.bookId = bookId 
		  and borrow.stuId = stuId 
		  and borrow.bookLibId = bookLibId 
		  and borrow.returnDate is null;
        
        -- 检查是否有人预约了且还没有拿到书籍，若有则把该书籍放到最先预约者的预约柜中(直接设置为借书行动)，否则将该书籍状态改为0
        select count(*) into counts 
        from reserve 
        where reserve.bookId = bookId 
          and reserve.bookLibId = bookLibId 
          and reserve.takeDate is null;
        
        if (counts > 0) then
            -- 从预约表中找到最先预约的学生和预约的图书馆
            select reserve.stuId, reserve.reserveLibId 
            from reserve
            where reserve.bookId = bookId 
              and reserve.bookLibId = bookLibId 
              and reserve.takeDate is null
            order by reserve.reserveDate asc
            limit 1
            into stuIdTmp, borrowLibIdTmp;
            
            -- 更新借书表,直接把书籍放到最先预约者的预约柜中，并假设该学生已经拿到了书籍
            insert into borrow(bookId, stuId, bookLibId, borrowDate, PreReturnDate, returnDate, borrowLibId, returnLibId) 
            value(bookId, stuIdTmp, bookLibId, curdate(), date_add(curdate(), interval 30 day), null, borrowLibIdTmp, null);
            
            -- 更新预约表，将该学生的预约状态设置为已经拿到书籍
            update reserve 
            set takeDate = curdate() 
            where reserve.bookId = bookId 
              and reserve.stuId = stuIdTmp 
              and reserve.bookLibId = bookLibId 
              and reserve.takeDate is null;
        else
            -- 更新书籍状态为可借
            update book 
            set bookStatus = 0,
                bookNum = bookNum + 1
            where book.bookId = bookId 
              and book.bookLibId = bookLibId;
        end if;
        SET FOREIGN_KEY_CHECKS = 1;
		SET SQL_SAFE_UPDATES = 1;
        select "还书成功！" as info;
    else
        select "未借阅本书！" as info;
    end if;
end //
delimiter ;