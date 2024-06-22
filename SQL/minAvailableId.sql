    -- 获得当前图书馆中最小的可用的图书编号
    -- 返回值：最小的可用的图书编号
    delimiter //
    create function minAvailableId(LibId char(8))
    returns char(8)
    DETERMINISTIC
    READS SQL DATA
    begin
        declare minId char(8);
        declare i int;
        set i = 1;
        while i <= 1000 do
            set minId = concat('B', lpad(i, 3, '0'));
            if not exists(select * from book where bookId = minId and bookLibId = LibId) then
                return minId;
            end if;
            set i = i + 1;
        end while;
        return null;
    end //
    delimiter ;