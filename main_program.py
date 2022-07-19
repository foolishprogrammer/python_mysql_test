# This is an assessent mini-task

# Separating the function to connect to database server
import connect_db as db

# The task ask for function, but I have the habit to lose track of variable naming
# so I choose to put all I need related to the database into a class and class method.

# data class for the data database
class dataDatabase:
    response_id: list[int] = []
    user_id: list[int] = []
    prompt: list[str] = []
    response: list[str] = []
    confirmed: list[str] = []

    def __init__(self, data_query) -> None:
        for i in data_query:
            self.response_id.append(i[0])
            self.user_id.append(i[1])
            self.prompt.append(i[2])
            self.response.append(i[3])
            self.confirmed.append(i[4])

    # this is the function for sorting key
    def sort_key(self, key) -> int:
        return key[1]

    # rank the user based on the top user
    def top_rank(self, rank: int, choice: str) -> list[tuple[int]]:
        data_uid = list(set(self.user_id))

        uid_confirmed = [
            (self.user_id[i], self.confirmed[i]) for i in range(len(self.user_id))
        ]
        # function to call for each choice
        def confirmed_yes(data=uid_confirmed) -> list[tuple[int]]:
            value_count = []

            for i in data_uid:
                value_count.append((i, data.count(i, "yes")))

            return value_count

        def confirmed_no(data=uid_confirmed) -> list[tuple[int]]:
            value_count = []

            for i in data_uid:
                value_count.append((i, data.count(i, "no")))

            return value_count

        def confirmed_all(data=uid_confirmed) -> list[tuple[int]]:
            value_count = []

            for i in data_uid:
                value_count.append(
                    (i, (data.count((i, "yes")) + data.count((i, "no"))))
                )

            return value_count

        # using dictionary rather than if else
        OPTION = {"yes": confirmed_yes, "no": confirmed_no}
        # use confirmed_all as the default value
        ranked = OPTION.get(choice, confirmed_all)()
        ranked.sort(self.sort_key, reverse=True)
        return ranked[:rank]


# user class for the user database
class userDatabase:
    uid: list[int] = []
    uname: list[str] = []

    def __init__(self, user_query) -> None:
        for i in user_query:
            self.uid.append(i[0])
            self.uname.append(i[1])


# Running the program
def main() -> None:
    query = db.connect.cursor()

    user_sql = "SELECT * FROM users"

    query.execute(user_sql)

    user_db = query.fetchall()

    user = userDatabase(user_db)

    data_sql = "SELECT * FROM data"

    query.execute(data_sql)

    data_db = query.fetchall()

    data = dataDatabase(data_db)


if __name__ == "__main__":
    main()
