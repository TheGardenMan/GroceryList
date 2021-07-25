import sqlite3


def get_con():
	# https://stackoverflow.com/a/63091236
	connection = sqlite3.connect("grocery.db")
	cursor = connection.cursor()
	return connection,cursor

def add_item(user_id,item_title,item_description,item_tag,date_to_buy):
	# https://stackoverflow.com/a/63091236
	connection,cursor = get_con()
	data=(user_id,item_title,item_description,item_tag,date_to_buy,)
	cursor.execute("insert into items (user_id,title,description,tag,date_to_buy) values (?,?,?,?,?)",data)
	connection.commit()
	return

def show_items(user_id,date_to_buy):
	connection,cursor = get_con()
	if date_to_buy:
		# get posts from given date..
		data = (user_id,date_to_buy,)
		cursor.execute("select count(title) from items where user_id = ? and  date_to_buy = ? ;",(data));
		item_count = cursor.fetchall()[0][0]
		if item_count == 0:
			return False
		cursor.execute("select item_id,title,description,tag,date_to_buy from items where user_id = ? and date_to_buy = ?;",(data))
		item_details = cursor.fetchall()
		# 	[('1','d', 'hih', 'PENDING', '2021-07-02'), ('2',d', 'hih', 'PENDING', '2021-07-02')]
		item_details_list = list(map(list, item_details))
		print(item_details_list)
		return item_details_list
	else:
		data = (user_id,)
		cursor.execute("select count(title) from items where user_id = ?;",(data));

		item_count = cursor.fetchall()[0][0]
		if item_count == 0:
			return False
		cursor.execute("select item_id,title,description,tag,date_to_buy from items where user_id = ?;",(data))
		item_details = cursor.fetchall()
		# 	[('1','d', 'hih', 'PENDING', '2021-07-02'), ('2',d', 'hih', 'PENDING', '2021-07-02')]
		item_details_list = list(map(list, item_details))
		print(item_details_list)
		return item_details_list

def delete_item(user_id,item_id):
	connection,cursor = get_con()
	data=(user_id,item_id,)
	cursor.execute("delete from items where user_id = ? and item_id = ?;",(data))
	connection.commit()
	return

def get_item_details(user_id,item_id):
	connection,cursor = get_con()
	data = (user_id,item_id,)
	cursor.execute("select title,description,tag,date_to_buy from items where user_id = ? and item_id=?;",(data))
	return cursor.fetchall()[0]

def update_item(user_id,item_id,item_title,item_description,item_tag,date_to_buy):
	connection,cursor = get_con()
	data = (item_title,item_description,item_tag,date_to_buy,user_id,item_id)
	cursor.execute("update items set title=?,description=?,tag=?,date_to_buy=? where user_id=? and item_id=? ;",(data))
	connection.commit()
	return