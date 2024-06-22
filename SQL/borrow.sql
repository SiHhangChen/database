delimiter //
create procedure borrowBook(In stuId char(10), in bookId char(8), in borrowLibId char(8), in bookLibId char(8))
begin
    declare counts int default 0;
    declare counts_1 int default 0;
    -- 检查是否今天以及借阅了本书
    select count(*) into counts 
    from borrow 
    where borrow.bookId = bookId 
      and borrow.stuId = stuId 
      and borrow.borrowDate = curdate() 
      and borrow.bookLibId = bookLibId;
    -- 检查该书是否还有库存
    select book.bookNum into counts_1 
    from book 
    where book.bookId = bookId 
      and book.bookLibId = bookLibId;

    -- 若今天没有借阅过本书，则可以借阅
    if(counts = 0) then
        -- 查看是否借阅书籍数量超过30本
        select count(*) into counts 
        from borrow 
        where borrow.stuId = stuId 
          and borrow.returnDate is null;

        if(counts < 3) then
            insert into borrow(bookId, stuId, bookLibId, borrowDate, PreReturnDate, returnDate, borrowLibId, returnLibId, overDays)
            value(bookId, stuId, bookLibId, curdate(), date_add(curdate(), interval 30 day), null, borrowLibId, null, 0);
            
            SET SQL_SAFE_UPDATES = 0;
            SET FOREIGN_KEY_CHECKS = 0;
            if(counts_1 = 1) then
                -- 若该书只有一本，则将该书的状态改为不可借，因为这一本已经被借出了
                update book 
                set bookStatus = 1 
                where book.bookId = bookId 
                  and book.bookLibId = bookLibId;
            end if;
            -- 更新借书次数
            update book 
            set bookBorrowTimes = bookBorrowTimes + 1,
                bookNum = bookNum - 1
            where book.bookId = bookId 
              and book.bookLibId = bookLibId;

            SET FOREIGN_KEY_CHECKS = 1;
            SET SQL_SAFE_UPDATES = 1;
            select "借书成功！" as info;
        else
            select "您已借书30本啦!请读完再来吧!" as error_info;
        end if;
    else
        select "您今天已经借阅过本书了哦！" as error_info;
    end if;
end //
delimiter ;