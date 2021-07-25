-- write sqlite3 queries
create table IF NOT EXISTS 	items (item_id integer primary key autoincrement,  user_id integer,title varchar(15),description varchar(200),tag varchar(15),date_to_buy date);

insert into items (user_id,title,description,tag,date_to_buy) values (1,'banana','10pcs','pending','2021-07-24');

update items set title='apple',description='2pcs',tag='bought',date_to_buy='2021-07-25' where user_id=1;

select title,description,tag,date_to_buy from items where user_id = '1';
select title,description,tag,date_to_buy from items where user_id = '1' and item_id='1';


select title,description,tag,date_to_buy from items where user_id = '1' and date_to_buy='2021-07-25';

delete from items where item_id='1' and user_id='1';