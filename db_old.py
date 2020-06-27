import sqlite3
connection = sqlite3.Connection('data.db')

cursor = connection.cursor()
create_table = "CREATE TABLE users (id int,username text,password text)"


cursor.execute(create_table)

user = (1, 'najh', 'njh123')

insert_query = "INSERT INTO users VALUES (?,?,?)"
cursor.execute(insert_query, user)


users = [
    (2, 'ali', 'ali123'),
    (3, 'huda', 'huda123')
]
cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"

for row in cursor.execute(select_query):
    print(row)


connection.commit()
connection.close()
