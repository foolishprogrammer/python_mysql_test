import connect_db as db

query = db.connect.cursor()

users_query = "SELECT * FROM users"

if(query.execute(users_query)) !=0 :
    users_list = query.fetchall()

data_query = "SELECT * FROM data"

if (query.execute(data_query)) !=0 :
    data_list = query.fetchall()

for i in users_list :
    print(i)

for i in data_list :
    print(i)
