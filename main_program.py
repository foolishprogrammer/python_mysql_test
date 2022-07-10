import connect_db as db

data_db_column = {
    "response_id": 0,
    "user_id": 1,
    "prompt": 2,
    "response": 3,
    "confirmed": 4
}

user_db_column = {
    "user_id":0,
    "name":1,
}

class data_tables:
    def __init__(self, data_query):
        self.response_id = [i[0] for i in data_query]
        self.user_id = [i[1] for i in data_query]
        self.prompt = [i[2] for i in data_query]
        self.response =  [i[3] for i in data_query]
        self.confirmed = [i[4] for i in data_query]
        self.confirmed_count =[]
        for i in range(1,6):
            self.confirmed_count.append([i, self.user_id.count(i)])
        self.confirmed_count.sort(reverse=True, key=self.top_sort)
    
    def top_sort(self, value):
        return value[1]

    def



query = db.connect.cursor()

user_sql = "SELECT * FROM users"

data_sql = "SELECT * FROM data WHERE confirmed = 'yes' ORDER BY user_id"

query.execute(data_sql)

data_list = query.fetchall()

data_test = data_tables(data_list)

print(data_test.confirmed_count)

