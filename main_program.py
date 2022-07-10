import connect_db as db

class database:
    def __init__(self, data_query, user_query) :
        self.data_response_id = [i[0] for i in data_query]
        self.data_user_id = [i[1] for i in data_query]
        self.data_prompt = [i[2] for i in data_query]
        self.data_response =  [i[3] for i in data_query]
        self.data_confirmed = [i[4] for i in data_query]
        self.data_confirmed_yes = []
        self.data_confirmed_no = []

        for i in range(len(self.data_confirmed)):
            if self.data_confirmed[i] == "yes":
                self.data_confirmed_yes.append(self.data_user_id[i])
            elif self.data_confirmed[i] == "no":
                self.data_confirmed_no.append(self.data_user_id[i])
        self.data_confirmed_yes_count =[]
        for i in range(1,6):
            self.data_confirmed_yes_count.append([i, self.data_confirmed_yes.count(i)])
        self.data_confirmed_no_count = []
        for i in range(1,6):
            self.data_confirmed_no_count.append([i, self.data_confirmed_no.count(i)])
        self.data_confirmed_yes_count.sort(reverse=True, key=self.top_sort)
        self.data_confirmed_no_count.sort(reverse=True, key=self.top_sort)
        self.user_user_id = [i[0] for i in user_query]
        self.user_name = [i[1] for i in user_query]
        

    def top_sort(self, value) :
        return value[1]

    def show_top_ranked(self, value):
        self.rank_top = []
        for i in self.data_confirmed_count[:value]:
            self.rank_top.append([self.user_name[self.user_user_id.index(i[0])], i[0], i[1]])
        return self.rank_top
    
    def show_bottom_ranked(self,value) :
        self.rank_bottom =[]
        for i in self.data_confirmed_count[-abs(value):]:
            self.rank_bottom.append([self.user_name[self.user_user_id.index(i[0])], i[0], i[1]])
        return self.rank_bottom
    
    def response_prompt_filter(self, value, comparator):
        if comparator==value :
            return True
        elif comparator=="all" :
            return True
        else :
            return False

    def response_to_prompt(self, value = 0, comparator = "all") :
        self.response_prompt_list_count=[]
        for i in range(len(self.data_confirmed)):
            prompt_count = len(self.data_prompt[i].split())
            response_count = len(self.data_response[i].split())
            response_prompt_difference = response_count - prompt_count
            if response_prompt_difference > value  and self.response_prompt_filter(self.data_confirmed[i], comparator):
                self.response_prompt_list_count.append([self.user_name[self.user_user_id.index(self.data_user_id[i])], self.data_user_id[i] , prompt_count, response_count, response_prompt_difference])
            else:
                continue
                            
        return self.response_prompt_list_count  
    


query = db.connect.cursor()

user_sql = "SELECT * FROM users"

query.execute(user_sql)

user_list = query.fetchall()

data_sql = "SELECT * FROM data"

query.execute(data_sql)

data_list = query.fetchall()

database_test = database(data_list, user_list)


