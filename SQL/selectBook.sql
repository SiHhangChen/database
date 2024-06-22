delimiter //
create procedure selectBook (In bname char(20))
begin
    CREATE TEMPORARY table temp AS select * from book where book.bname = bname;
end //
delimiter ;