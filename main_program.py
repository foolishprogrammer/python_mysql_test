# This is an assessent mini-task

# Separating the function to connect to database server
import connect_db as db
import time

# The task ask for function, but I have the habit to lose track of variable naming
# so I choose to put all I need related to the database into a class and class method.

# data class for the data database
class dataDatabase:
    response_id: list[int] = []
    user_id: list[int] = []
    prompt: list[str] = []
    response: list[str] = []
    confirmed: list[str] = []

    def __init__(self, data_query: list) -> None:
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
    def top_rank(self, rank: int, choice: str) -> list:
        data_uid = list(set(self.user_id))

        uid_confirmed = [
            (self.user_id[i], self.confirmed[i]) for i in range(len(self.user_id))
        ]
        # function to call for each choice
        def confirmed_yes(data=uid_confirmed) -> list:
            value_count = []

            for i in data_uid:
                value_count.append((i, data.count((i, "yes"))))

            return value_count

        def confirmed_no(data=uid_confirmed) -> list:
            value_count = []

            for i in data_uid:
                value_count.append((i, data.count((i, "no"))))

            return value_count

        def confirmed_all(data=uid_confirmed) -> list:
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
        ranked.sort(key=self.sort_key, reverse=True)
        return ranked[:rank]

    # counting the difference between prompt and response
    # and count how many times the each user id that fit the condition given
    # (in this case, if the difference is bigger than given value)
    def top_difference(
        self, condition: int, confirmation: str = "all", rank: int = 1
    ) -> list:
        ranked: list = []

        def prompt_response_difference(prompt: str, response: str) -> int:
            return len(response.split()) - len(prompt.split())

        difference_count: list = [
            self.user_id[i]
            for i in range(len(self.user_id))
            if (
                abs(prompt_response_difference(self.prompt[i], self.response[i]))
                >= condition
            )
            and (confirmation == self.confirmed[i] or confirmation == "all")
        ]

        data_uid = list(set(self.user_id))

        for i in data_uid:
            ranked.append((i, difference_count.count(i)))

        ranked.sort(key=self.sort_key, reverse=True)
        return ranked[:rank]


# user class for the user database
class userDatabase:
    uid: list[int] = []
    uname: list[str] = []

    def __init__(self, user_query) -> None:
        for i in user_query:
            self.uid.append(i[0])
            self.uname.append(i[1])

    def retrieve_name(self, check_uid: list) -> list[str]:
        name_list: list = []

        for i in check_uid:
            name_list.append(self.uname[self.uid.index(i[0])])

        return name_list


# Running the program
def main() -> None:

    prompt: str = ""

    prompt = input("Do you want to see the basic function of this program? (Y/n) \n")

    if prompt.lower() == "y":
        print("\nThis is the 3 top ranked user with the most confirmed response.")
        time.sleep(1)
        ranked_list: list[str] = user.retrieve_name(data.top_rank(3, "yes"))

        for i in ranked_list:
            print("Rank " + str(ranked_list.index(i) + 1) + " : " + i)
            time.sleep(1)

        print(
            "\nThis is the top user with the difference more than 6 between prompt and response."
        )
        time.sleep(1)
        ranked_difference: list[str] = user.retrieve_name(data.top_difference(7, "all"))

        for i in ranked_difference:
            print(("Rank " + str(ranked_difference.index(i) + 1) + " : " + i))
            time.sleep(1)

        print(
            "\nFrom here on, you can try accessing the data with user defined parameter."
        )

        data_selection(data, user)

        prompt = input("\nDo you want to re-run the program again? (Y/n)\n")
        if prompt.lower() == "y":
            return main()


def data_selection(data: dataDatabase, user: userDatabase) -> None:
    print("\nFrom here, you can access the data with differenct parameter!")

    prompt: str = ""

    prompt = input(
        "\nWhat do you want to do ? \n1. Ranked user overall. \n2. Ranked user based on prompt and response. \n>"
    )

    def ranked_overall(data, user) -> None:
        confirmation_prompt: str = ""

        user_prompt: int = 0

        confirmation_prompt = input(
            "\nWhich one of confirmation status you are looking for? (yes/no/all) \n>"
        )

        user_prompt = int(input("\nHow many user do you want to see? (max: 5) \n>"))

        ranked: list = user.retrieve_name(
            data.top_rank(user_prompt, confirmation_prompt)
        )

        print(
            "The top "
            + str(user_prompt)
            + ' that confirmed "'
            + confirmation_prompt
            + '" : '
        )

        for i in ranked:
            print("Rank " + str(ranked.index(i) + 1) + " : " + i)
            time.sleep(1)

        confirm = input("\nDo you want to try again? (Y/n) \n")
        if confirm.lower() == "y":
            return ranked_overall(data, user)

    def ranked_conditional(data, user) -> None:

        confirmation_prompt: str = ""
        conditional_prompt: int = 0
        user_prompt: int = 0

        confirmation_prompt = input(
            "Which one of confirmation status you are looking for? (yes/no/all) \n>"
        )

        conditional_prompt = int(
            input("How many the limit of minimum words for the difference? \n>")
        )

        user_prompt = int(input("How many user do you want to see? (max: 5) \n>"))

        ranked: list = user.retrieve_name(
            data.top_difference(conditional_prompt, confirmation_prompt, user_prompt)
        )

        print(
            "The top "
            + str(user_prompt)
            + ' that confirmed "'
            + confirmation_prompt
            + '" with difference of '
            + str(conditional_prompt)
            + ": "
        )

        for i in ranked:
            print("Rank " + str(ranked.index(i) + 1) + " : " + i)
            time.sleep(1)

        confirm = input("Do you want to try again? (Y/n) \n")
        if confirm.lower() == "y":
            return ranked_conditional(data, user)

    def default_option(data, user) -> bool:
        print("Continue to the next prompt!")
        return data == user

    OPTION: dict = {"1": ranked_overall, "2": ranked_conditional}

    OPTION.get(prompt, default_option)(data, user)

    if (
        input(
            "Do you want to retry the custom parameter function again? (Y/n) \n"
        ).lower()
        == "y"
    ):
        return data_selection(data, user)


if __name__ == "__main__":

    print(
        """
This is the program to access the databse given.
This program will retrieve data from database and output
ranked user on certain parameter.
    """
    )
    # This is the connection to the daatabase
    query = db.connect.cursor()

    user_sql = "SELECT * FROM users"

    query.execute(user_sql)

    user_db = query.fetchall()

    user = userDatabase(user_db)

    data_sql = "SELECT * FROM data"

    query.execute(data_sql)

    data_db = query.fetchall()

    data = dataDatabase(data_db)

    main()
