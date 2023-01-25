# First, start the cassandra docker image

from cassandra.cluster import Cluster


def insert(s):
    f = input("\tEnter first name: ")
    l = input("\tEnter last name: ")
    e = input("\tEnter email: ")
    c = input("\tEnter favorite color: ")

    user_info = [f, l, e, c]

    insert_query = s.prepare("INSERT INTO users_keyspace.users "
                             "(firstname, lastname, email, \"favorite color\") "
                             "VALUES (?, ?, ?, ?) IF NOT EXISTS")

    try:
        s.execute(insert_query, user_info)
        print(f"\t{f} added!")
    except Exception as _:
        pass
        print("\tAdd failed.")


def show(s):
    rows = s.execute('SELECT firstname, lastname, email, "favorite color" FROM users')
    for user_row in rows:
        print("\t", user_row.firstname, user_row.lastname, user_row.email, user_row.favorite_color)


def clear(s):
    s.execute('TRUNCATE users_keyspace.users')
    print("\tList cleared!")


def instruct():
    print("Welcome! Commands:")
    print("\t'a': Add a person")
    print("\t's': Show all persons added")
    print("\t'c': Clear list of persons")
    print("\t'q': Quit")


if __name__ == "__main__":
    cluster = Cluster(['127.0.0.1'])

    session = cluster.connect()
    session.set_keyspace('users_keyspace')

    choice = "nonsense"

    while True:
        if choice == "a":
            insert(session)
        elif choice == "s":
            show(session)
        elif choice == "c":
            clear(session)
        elif choice == "q":
            print("\nThanks for using!")
            break
        else:
            instruct()
        choice = input("Enter Selection: ")
