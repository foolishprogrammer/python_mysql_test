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
        self.user_user_id = [i[0] for i in user_query]
        self.user_name = [i[1] for i in user_query]
        
        self.data_confirmed_count = []
        for i in range(1, len(self.user_user_id)+1):
            self.data_confirmed_count.append([i, self.data_user_id.count(i)])
        
        self.data_confirmed_yes_count =[]
        for i in range(1,len(self.user_user_id)+1):
            self.data_confirmed_yes_count.append([i, self.data_confirmed_yes.count(i)])
        
        self.data_confirmed_no_count = []
        for i in range(1,len(self.user_user_id)+1):
            self.data_confirmed_no_count.append([i, self.data_confirmed_no.count(i)])

        self.data_confirmed_yes_count.sort(reverse=True, key=self.top_sort)
        self.data_confirmed_no_count.sort(reverse=True, key=self.top_sort)
        self.data_confirmed_count.sort(reverse=True, key=self.top_sort)

    def top_sort(self, value) :
        return value[1]

    def show_top_ranked(self, value=1, choice = 0):
        self.rank_top = []
        if choice == 1 :
            for i in self.data_confirmed_yes_count[:value]:
                self.rank_top.append([self.user_name[self.user_user_id.index(i[0])], i[0], i[1]])
        elif choice== 2 :
            for i in self.data_confirmed_no_count[:value]:
                self.rank_top.append([self.user_name[self.user_user_id.index(i[0])], i[0], i[1]])
        else :
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

    def ranked_response_to_prompt(self, value = 0, comparator = "all", rank = 1):
        response_prompt = self.response_to_prompt(value, comparator)
        response_to_prompt_id_list = [i[1] for i in response_prompt]
        self.response_to_prompt_id_count =[]
        for i in range(len(self.user_user_id)):
            self.response_to_prompt_id_count.append([self.user_name[self.user_user_id.index(i+1)],self.user_user_id[i], response_to_prompt_id_list.count(i)])
        
        self.response_to_prompt_id_count.sort(reverse=True, key=self.ranked_response_to_prompt_sort)

        return self.response_to_prompt_id_count[:rank]


    def ranked_response_to_prompt_sort(self, value) :
        return value[2]

            
        

def first_task(database_object):
    print("First task is to display the top 3 users with most confirmed responses!")
    print("What the confirmation status you are looking for?")
    task_input_1 = input ("0 for all, 1 for \"yes\", 2 for \"no\" (default 0) \n> ")
    print("How many top users do you want to display?")
    task_input_2 = input("From 1 to 5 : ")
    print(database_object.show_top_ranked(int(task_input_2), int(task_input_1)))

    print("Do you want to try again?")
    task_input_3 = input("Y/n ")

    if task_input_3.lower() == "y" :
        return first_task(database_object)

    else :
        return 0

def second_task(database_object):
    print("Second task is to display the name of the user who has the most responses with difference of more than 6 from the prompt")
    print("What the confirmation status you are looking for?")   
    task_input_1 = input ("0 for all, 1 for \"yes\", 2 for \"no\" (default 0) \n> ")
    print("How many words the difference between response and prompt?")
    task_input_2 = input("Input the number : ")
    if int(task_input_1) == 1 :
        choice = "yes"
    elif int(task_input_1) == 2 :
        choice = "no"
    else :
        choice = "all"
    print("How many top user(s) do you want to display?")
    task_input_3 = input("Input the number (Max 5): ")

    print(database_object.ranked_response_to_prompt(int(task_input_2), choice, int(task_input_3)))

    print("Do you want to try again?")
    task_input_4 = input("Y/n ")

    if task_input_4.lower() == "y" :
        return second_task(database_object)
    else :
        return 0


query = db.connect.cursor()

user_sql = "SELECT * FROM users"

query.execute(user_sql)

user_list = query.fetchall()

data_sql = "SELECT * FROM data"

query.execute(data_sql)

data_list = query.fetchall()

database_test = database(data_list, user_list)

print("This is the Take Home Coding Test!\n")

first_task(database_test)

second_task(database_test)
