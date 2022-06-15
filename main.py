import sys
import pyodbc

conn_str = (
    r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};'
    r'DBQ=D:\PyCharm\courseprogram_access\tournament.accdb;'
)
# REMEMBER TO CHANGE THE ABOVE DIRECTORY TO THE FOLDER WHERE THE DATABASE IS LOCATED...


def display_help():
    # Function to explain options in the menu
    print('''
=======================================================================================
Choosing option 1 will allow you to add a new contestant or team into the tournament
Choosing option 2 will allow you to edit existing contestant information
Choosing option 3 will allow you to add or change event info
Choosing option 4 will allow you to add or update scores
Choosing option 5 will allow you to see previous scores
Choosing option 6 will show you this help message.
Choosing option 7 will prompt you to confirm you wish to exit the program.
=======================================================================================
    ''')


def test():

    sql = "SELECT * FROM tbl_contestants"
    ssl = "SELECT * FROM tbl_contestants WHERE contestant_type = 'i'"

    mydb = pyodbc.connect(conn_str)
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    sql_first_row = mycursor.fetchone()
    print(sql_first_row)
    mycursor.execute(ssl)
    ssl_first_row = mycursor.fetchone()
    print(ssl_first_row)

    # for row in result:
    #    c_id = row[0]
    #    c_name = row[1]
    #    c_type = row[2]
    #    print("ID: {}\nName: {}\nType: {}\n".format(c_id, c_name, c_type))
    mydb.close()

    # mydb = mysql.connector.connect(host=host, user=user, passwd=password, database=db)
    # mycursor = mydb.cursor()
    # mycursor.execute(sql)
    # result = mycursor.fetchall()
    # print(result)
    # mydb.close()


def add_contestant():
    # Function that allows user to add a new contestant
    print("A contestant can be either an individual or a team.")
    try:
        count = int(input("How many contestants would you like to add? "))
        x = 0
        sql = "SELECT * FROM tbl_contestants"
        while True:
            mydb = pyodbc.connect(conn_str)
            mycursor = mydb.cursor()
            if x != count:
                c_name = input("What is the name of the contestant? ")
                c_type = input(
                    "Is the contestant an individual(i) or a team(t)? ")
                contestant_type = 0
                if c_type == "i" or c_type == "I":
                    contestant_type = "i"
                    individuals = "SELECT * FROM tbl_contestants WHERE contestant_type = 'i'"
                    mycursor.execute(individuals)
                    individual_count = mycursor.fetchall()
                    i = 0
                    for row in individual_count:
                        i += 1
                    if i >= 20:
                        contestant_type = 0

                elif c_type == "t" or c_type == "T":
                    contestant_type = "t"

                    teams = "SELECT * FROM tbl_contestants WHERE contestant_type = 't'"
                    mycursor.execute(teams)
                    team_count = mycursor.fetchall()
                    t = 0
                    for row in team_count:
                        t += 1
                    if t >= 4:
                        contestant_type = 0
                else:
                    print(
                        "The value you have entered is not valid. Please enter 'i' or 't'")

                if contestant_type != 0:
                    mydb = pyodbc.connect(conn_str)
                    mycursor = mydb.cursor()
                    sql = "INSERT INTO tbl_contestants (contestant_name, contestant_type) VALUES (?, ?)"
                    value = (c_name, contestant_type)
                    mycursor.execute(sql, value)
                    mydb.commit()
                    mydb.close()
                    print("Contestant " + c_name + " has been added.")
                    x += 1
                else:
                    print(
                        "The maximum number of contestants of this type has been reached.")
                    mydb.close()
                    break
            else:
                print("Returning to Menu")
                mydb.close()
                menu()
    except ValueError:
        print("Please enter the number of contestants you wish to add.")


def edit_contestant():
    print('''
=====================================
Type 1 to edit a contestant's name
Type 2 to change a contestant's type
Type 3 to delete a contestant
Type 4 to list contestants
Type 5 to cancel
=====================================
    ''')
    try:
        option = int(input("Please choose which change you want to make: "))
        if option == 1:
            count = int(input("How many users would you like to update? "))
            x = 0
            while True:
                if x != count:
                    c_id = input(
                        "What is the ID of the contestant you wish to change? ")
                    mydb = pyodbc.connect(conn_str)
                    mycursor = mydb.cursor()
                    sql = "SELECT * FROM tbl_contestants WHERE contestant_id =" + c_id
                    mycursor.execute(sql)
                    result = mycursor.fetchall()
                    a = 0
                    for row in result:
                        a += 1
                        row_count = a
                    if row_count == 0:
                        print("Sorry, we couldn't find ID: " + c_id +
                              ", in the database. Please try again.")
                    elif row_count == 1:
                        n_name = input(
                            "What would you like the name to be changed to? ")
                        sql = "UPDATE tbl_contestants SET contestant_name ='" + \
                            n_name+"' WHERE contestant_id ="+c_id
                        mycursor.execute(sql)
                        print("Contestant name updated.")
                        mydb.commit()
                        mydb.close()
                        x += 1
                    else:
                        rows = str(row_count)
                        print("We found: " + rows + " contestants.")
                        print("Sorry, something went wrong. Please try again.")
                else:
                    print("Returning to menu")
                    break

        elif option == 2:
            count = int(input("How many users would you like to update?"))
            x = 0
            while True:
                if x != count:
                    c_id = input(
                        "What is the ID of the contestant you wish to change? ")
                    mydb = pyodbc.connect(conn_str)
                    mycursor = mydb.cursor()
                    sql = "SELECT * FROM tbl_contestants WHERE contestant_id =" + c_id
                    mycursor.execute(sql)
                    result = mycursor.fetchall()
                    c = 0
                    for row in result:
                        c += 1
                        row_count = c
                    if row_count == 0:
                        print("Sorry, we couldn't find ID: " + c_id +
                              ",in the database. Please try again.")
                    elif row_count == 1:
                        n_type = input(
                            "What would you like this contestant's type to be? ")
                        if n_type == "i" or n_type == "I":
                            sql = "UPDATE tbl_contestants SET contestant_type ='i' WHERE contestant_id ="+c_id
                            mycursor.execute(sql)
                            print("Contestant type changed to Individual")
                            mydb.commit()
                            mydb.close()
                            x += 1
                        elif n_type == "t" or n_type == "T":
                            sql = "UPDATE tbl_contestants SET contestant_type ='t' WHERE contestant_id ="+c_id
                            mycursor.execute(sql)
                            print("Contestant type changed to Team")
                            mydb.commit()
                            mydb.close()
                            x += 1
                    else:
                        print("Sorry, something went wrong. Please try again.")
                else:
                    print("Returning to menu.")
                    menu()
        elif option == 3:
            print(
                "You have chosen to delete a contestant. Please remember this will also delete their scores.")
            count = int(input("How many users would you like to delete? "))
            x = 0
            while True:
                if x != count:
                    c_id = input(
                        "What is the ID of the contestant you wish to delete: ")
                    mydb = pyodbc.connect(conn_str)
                    mycursor = mydb.cursor()
                    sql = "SELECT * FROM tbl_contestants WHERE contestant_id =" + c_id
                    mycursor.execute(sql)
                    result = mycursor.fetchall()
                    a_name = "An unknown error has occurred."
                    for row in result:
                        a_id = row[0]
                        a_name = row[1]
                        a_type = row[2]
                        print("\nID: {}\nName: {}\nType: {}\n".format(
                            a_id, a_name, a_type))
                    choice = input(
                        "Are you sure you want to delete '"+a_name+"' [Y/N]: ")
                    if choice == "y" or choice == "Y":
                        print("Deleting contestant...")
                        delete = "DELETE FROM tbl_contestants WHERE contestant_id =" + c_id
                        mycursor.execute(delete)
                        mydb.commit()
                        mydb.close()
                        x += 1
                    elif choice == "n" or choice == "N":
                        print("Operation cancelled.")
                        print("Returning to menu.")
                        x = count
                        edit_contestant()
                    else:
                        print("That is not a valid choice. Operation cancelled.")
                        print("Returning to menu.")
                        x = count
                        edit_contestant()
                else:
                    print("Returning to menu...")
                    menu()
        elif option == 4:
            print("Getting contestants...")
            mydb = pyodbc.connect(conn_str)
            mycursor = mydb.cursor()
            search = "SELECT * FROM tbl_contestants"
            mycursor.execute(search)
            contestants = mycursor.fetchall()
            rows = "An Unknown error has occurred."
            x = 0
            for row in contestants:
                c_id = row[0]
                c_name = row[1]
                c_type = row[2]
                x += 1
                print("\nContestant ID: {}\nContestant Name: {}\nContestant Type: {}".format(
                    c_id, c_name, c_type))
            rows = str(x)
            print("Retrieved " + rows + " Contestants.")
            edit_contestant()
        elif option == 5:
            print("Returning to menu...")
            menu()
        else:
            print("The value you have entered is not an option. Please try again.")
    except ValueError:
        print("The value you have entered is invalid. Please try again.")


def edit_event():
    print('''
=============================
Type 1 to add a new event
Type 2 to delete an event
Type 3 to change event type
Type 4 to change event name
Type 5 to show all events
Type 6 to cancel
=============================
    ''')
    try:
        option = int(input("Please choose which change you want to make: "))
        if option == 1:
            count = int(input("How many events would you like to add? "))
            x = 0
            while True:
                if x != count:
                    i_name = input("What is the name of the new event? ")
                    i_type = input(
                        "Is the event an Individual(i) or Team(t) event? ")
                    e_type = 0
                    if i_type == "i" or i_type == "I":
                        e_type = "i"
                    elif i_type == "t" or i_type == "T":
                        e_type = "t"
                    else:
                        print(
                            "The type you have entered is not valid. Please choose either 'i' or 't'")

                    if e_type != 0:
                        mydb = pyodbc.connect(conn_str)
                        mycursor = mydb.cursor()
                        sql = "INSERT INTO tbl_events (event_name, event_type) VALUES (?, ?)"
                        values = (i_name, e_type)
                        mycursor.execute(sql, values)
                        mydb.commit()
                        mydb.close()
                        print("Event " + i_name + " with type: " +
                              e_type + ", has been added. ")
                        x += 1
                    else:
                        print("Sorry, something went wrong. Please try again.")
                else:
                    print("Returning to menu...")
                    menu()
        elif option == 2:
            print("You have chosen to delete an event.")
            print(
                "Please remember that this will also delete the scores associated with this event.")
            print(
                "You will only be able to delete one event at a time for safety purposes.")
            x = 0
            count = 1
            while True:
                if x != count:
                    e_id = input(
                        "Enter the ID of the event you wish to delete: ")
                    mydb = pyodbc.connect(conn_str)
                    mycursor = mydb.cursor()
                    select = "SELECT * FROM tbl_events WHERE event_id =" + e_id
                    mycursor.execute(select)
                    events = mycursor.fetchall()
                    a_id = "An unknown error has occurred."
                    a_name = "An unknown error has occurred."
                    for row in events:
                        a_id = row[0]
                        a_name = row[1]
                        a_type = row[2]
                        print("\nEvent ID: {}\nEvent Name: {}\nEvent Type: {}".format(
                            a_id, a_name, a_type))
                    choice = input(
                        "Are you sure you want to delete event: '" + a_name + "' [Y/N]: ")
                    if choice == "y" or choice == "Y":
                        print("Deleting contestant...")
                        s_id = str(a_id)
                        delete = "DELETE FROM tbl_events WHERE event_id =" + s_id
                        mycursor.execute(delete)
                        mydb.commit()
                        mydb.close()
                        x += 1
                    elif choice == "n" or choice == "N":
                        print("Operation cancelled.")
                        print("Returning to menu...")
                        x = count
                        edit_event()
                    else:
                        print("That is not a valid choice. Operation Cancelled.")
                        print("Returning to menu...")
                        x = count
                        edit_event()
                else:
                    print("Returning to menu...")
                    menu()
        elif option == 3:
            count = int(input("How many events would you like to change? "))
            x = 0
            while True:
                if x != count:
                    e_id = input(
                        "What is the ID of the event you wish to change? ")
                    mydb = pyodbc.connect(conn_str)
                    mycursor = mydb.cursor()
                    sql = "SELECT * FROM tbl_events WHERE event_id =" + e_id
                    mycursor.execute(sql)
                    result = mycursor.fetchall()
                    b = 0
                    for row in result:
                        b += 1
                        row_count = b
                    if row_count == 0:
                        print("Sorry, we couldn't find event ID: " +
                              e_id + ", in the database. Please try again.")
                    elif row_count == 1:
                        n_type = input(
                            "What would you like this event's type to be? ")
                        if n_type == "i" or n_type == "I":
                            update = "UPDATE tbl_events SET event_type = 'i' WHERE event_id =" + e_id
                            mycursor.execute(update)
                            print("Event type changed to Individual.")
                            mydb.commit()
                            mydb.close()
                            x += 1
                        elif n_type == "t" or n_type == "T":
                            update = "UPDATE tbl_events SET event_type = 't' WHERE event_id =" + e_id
                            mycursor.execute(update)
                            print("Event type changed to Team.")
                            mydb.commit()
                            mydb.close()
                            x += 1
                    else:
                        print("Sorry, something went wrong. Please try again.")
                else:
                    print("Returning to menu...")
                    menu()
        elif option == 4:
            count = int(input("How many events would you like to change?"))
            x = 0
            while True:
                if x != count:
                    e_id = input(
                        "What is the id of the event you wish to change?")
                    mydb = pyodbc.connect(conn_str)
                    mycursor = mydb.cursor()
                    select = "SELECT * FROM tbl_events WHERE event_id =" + e_id
                    mycursor.execute(select)
                    result = mycursor.fetchall()
                    c = 0
                    for row in result:
                        c += 1
                        row_count = c
                    if row_count == 0:
                        print("Sorry, we couldn't find event ID: " +
                              e_id + ", in the database. Please try again.")
                    elif row_count == 1:
                        n_name = input(
                            "What would you like the name to be changed to? ")
                        update = "UPDATE tbl_events SET event_name ='" + \
                            n_name + "' WHERE event_id =" + e_id
                        mycursor.execute(update)
                        print("Event name updated.")
                        mydb.commit()
                        mydb.close()
                        x += 1
                    else:
                        print("Sorry, something went wrong. Please try again.")
                else:
                    print("Returning to menu...")
                    menu()
        elif option == 5:
            print("Getting Events...")
            mydb = pyodbc.connect(conn_str)
            mycursor = mydb.cursor()
            search = "SELECT * FROM tbl_events"
            mycursor.execute(search)
            events = mycursor.fetchall()
            rows = "An Unknown error has occurred."
            x = 0
            for row in events:
                e_id = row[0]
                e_name = row[1]
                e_type = row[2]
                x += 1
                print("\nEvent ID: {}\nEvent Name: {}\nEvent Type: {}".format(
                    e_id, e_name, e_type))
            rows = str(x)
            print("Retrieved " + rows + " Events.")
            edit_event()
        elif option == 6:
            print("Returning to menu.")
            menu()
        else:
            print("The option you have selected is not valid. Please try again.")
    except ValueError:
        print("The value you have entered is not valid. Please try again.")


def edit_scores():
    print('''
==================================================
Type 1 to add contestants score in an event
Type 2 to change a contestants score in an event
Type 3 to delete a score
Type 4 to cancel
==================================================
    ''')
    try:
        choice = int(input("What would you like to do?"))
        if choice == 1:
            # FUNCTION TO ADD SCORES
            print("Competitors can only be registered for either 1 or 5 events.")
            count = int(input("How many scores would you like to add? "))
            x = 0
            while True:
                if x != count:
                    c_id = str(
                        input("What is the ID of the contestant you wish to add a score for? "))
                    e_id = str(
                        input("What is the ID of the event which the score relates to?"))
                    c_type = 0
                    e_type = 0
                    mydb = pyodbc.connect(conn_str)
                    mycursor = mydb.cursor()
                    check_contestant = "SELECT * FROM tbl_contestants WHERE contestant_id =" + c_id
                    check_event = "SELECT * FROM tbl_events WHERE event_id =" + e_id
                    #  search for contestant
                    mycursor.execute(check_contestant)
                    contestant_result = mycursor.fetchall()
                    e = 0
                    for row in contestant_result:
                        e += 1
                        contestant_count = e
                    #  search for event
                    mycursor.execute(check_event)
                    event_result = mycursor.fetchall()
                    f = 0
                    for row in event_result:
                        f += 1
                        event_count = f
                    #  check if event and contestant exists
                    if contestant_count == 1 and event_count == 1:
                        # check if contestant is correct type for event
                        for row in contestant_result:
                            c_id = row[0]
                            c_type = row[2]
                        for row in event_result:
                            e_id = row[0]
                            e_type = row[2]
                        if e_type == c_type:
                            presence = "SELECT * FROM tbl_event_participation WHERE contestant_id =" + c_id
                            mycursor.execute(presence)
                            result = mycursor.fetchall()
                            g = 0
                            row_count = 0
                            for row in result:
                                g += 1
                                row_count = g
                            if row_count == 0:
                                print("Event and contestant found.")
                                score = str(
                                    input("Please enter the score the contestant achieved: "))
                                insert = "INSERT INTO tbl_event_participation (contestant_id, event_id, score) VALUES (?, ?, ?)"
                                values = (c_id, e_id, score)
                                mycursor.execute(insert, values)
                                print("Scores added successfully.")
                                mydb.commit()
                                mydb.close()
                                x += 1
                            else:
                                print(
                                    "This contestant's scores have already been entered.")
                                mydb.rollback()
                                mydb.close()
                        else:
                            print(
                                "This contestant can not compete in this event. Please try again.")
                            mydb.rollback()
                    elif contestant_count == 0 and event_count == 0:
                        print(
                            "Neither the event nor contestant that you entered could be found. Please try again.")
                    elif contestant_count == 0:
                        print("Contestant not found. Please try again.")
                    elif event_count == 0:
                        print("Event not found. Please try again.")
                else:
                    print("Returning to menu...")
                    menu()
        elif choice == 2:
            print("Edit score")
            count = int(input("How many scores would you like to change? "))
            x = 0
            while True:
                if x != count:
                    s_id = input(
                        "What is the ID of the score you wish to change? ")
                    mydb = pyodbc.connect(conn_str)
                    mycursor = mydb.cursor()
                    select = "SELECT * FROM tbl_event_participation WHERE id =" + s_id
                    mycursor.execute(select)
                    result = mycursor.fetchall()
                    h = 0
                    for row in result:
                        h += 1
                        row_count = h
                    if row_count == 0:
                        print("Sorry, we couldn't find the score ID: " +
                              s_id + ", in the database. Please try again.")
                        mydb.close()
                    elif row_count == 1:
                        print("Here's what we found:")
                        for row in result:
                            s_id = row[0]
                            c_id = row[1]
                            e_id = row[2]
                            score = row[3]
                            print("\nScore ID: {}\nContestant ID: {}\nEvent ID: {}\nScore: {}".format(
                                s_id, c_id, e_id, score))
                        n_score = input(
                            "What would you like the score to be changed to?")
                        update = "UPDATE tbl_event_participation SET score ='" + \
                            n_score + "' WHERE id ='" + s_id
                        mycursor.execute(update)
                        print("Score updated.")
                        mydb.commit()
                        mydb.close()
                        x += 1
                    else:
                        print("Sorry, something went wrong. Please try again.")
                        mydb.close()
                else:
                    print("Returning to menu...")
                    menu()
        elif choice == 3:
            print("You have chosen to delete a score.")
            print("Please remember this action can not be undone.")
            print(
                "For safety purposes you will only be able to delete one score at a time.")
            x = 0
            count = 1
            while True:
                if x != count:
                    s_id = input(
                        "Enter the ID of the score you wish to delete: ")
                    mydb = pyodbc.connect(conn_str)
                    mycursor = mydb.cursor()
                    select = "SELECT * FROM tbl_event_participation WHERE id =" + s_id
                    mycursor.execute(select)
                    scores = mycursor.fetchall()
                    s_id = "An unknown error has occurred."
                    c_id = "An unknown error has occurred."
                    e_id = "An unknown error has occurred."
                    score = "An unknown error has occurred."
                    for row in scores:
                        s_id = row[0]
                        c_id = row[1]
                        e_id = row[2]
                        score = row[3]
                        print("\nScore ID: {}\nContestant ID: {}\nEvent ID: {}\nScore: {}".format(
                            s_id, c_id, e_id, score))
                    option = input(
                        "Are you sure you want to delete this event? [Y/N]: ")
                    if option == "y" or option == "Y":
                        print("Deleting contestant...")
                        delete = "DELETE FROM tbl_event_participation WHERE id =" + s_id
                        mycursor.execute(delete)
                        mydb.commit()
                        mydb.close()
                    elif option == "n" or option == "N":
                        print("Operation cancelled.")
                        print("Returning to menu...")
                        x = count
                        edit_scores()
                    else:
                        print("That is not a valid option. Operation Cancelled.")
                        print("Returning to menu...")
                        x = count
                        edit_scores()
                else:
                    print("Returning to menu...")
                    menu()
        elif choice == 4:
            print("Returning to menu...")
            menu()
        else:
            print("The value you have entered is not a valid option. Please try again.")
            menu()
    except ValueError:
        print("The value you have entered is not valid. Please try again.")


def read_scores():
    while True:
        try:
            p_or_e = input(
                "Would you like to search by event(e) or contestant(c)?")
            if p_or_e == "e" or p_or_e == "E":
                print("Searching by event...")
                event = input("Enter the event ID you wish to search for: ")
                mydb = pyodbc.connect(conn_str)
                mycursor = mydb.cursor()
                search = "SELECT * FROM tbl_event_participation WHERE event_id =" + event
                mycursor.execute(search)
                results = mycursor.fetchall()
                print("Scores for event: " + event)
                for row in results:
                    s_id = row[0]
                    c_id = row[1]
                    e_id = row[2]
                    score = row[3]
                    print("\nScore ID: {}\nContestant ID: {}\nEvent ID: {}\nScore: {}".format(
                        s_id, c_id, e_id, score))
                mydb.close()
                break
            elif p_or_e == "c" or p_or_e == "C":
                print("Searching by contestant...")
                contestant = input(
                    "Enter the contestant ID you wish to search for: ")
                mydb = pyodbc.connect(conn_str)
                mycursor = mydb.cursor()
                search = "SELECT * FROM tbl_event_participation WHERE contestant_id =" + contestant
                mycursor.execute(search)
                results = mycursor.fetchall()
                print("Scores for contestant: " + contestant)
                for row in results:
                    s_id = row[0]
                    c_id = row[1]
                    e_id = row[2]
                    score = row[3]
                    print("\nScore ID: {}\nContestant ID: {}\nEvent ID: {}\nScore: {}".format(
                        s_id, c_id, e_id, score))
                mydb.close()
                break
        except ValueError:
            print("The value you have entered is not valid. Please try again.")


def menu():
    # Function to give the user choice of what they want to do.
    while True:
        print('''
=======================================
Type 1 to add a new contestant or team
Type 2 to edit contestant info
Type 3 to edit event info
Type 4 to edit or update scores
Type 5 to show previous scores
Type 6 to show help
Type 7 to exit the program
=======================================
        ''')
        try:
            choice = int(input("What would you like to do? "))
            if choice == 1:
                add_contestant()
            elif choice == 2:
                edit_contestant()
            elif choice == 3:
                edit_event()
            elif choice == 4:
                edit_scores()
            elif choice == 5:
                read_scores()
            elif choice == 6:
                display_help()
            elif choice == 7:
                confirm_exit = input("Are you sure you want to exit? [Y/N]: ")
                if confirm_exit == "y" or confirm_exit == "Y":
                    print("Program will now exit.")
                    sys.exit()
                else:
                    print("Returning to menu...")
            else:
                print("The option you have chosen is not valid. Please try again.")
        except ValueError:
            print("The option you have chosen is not valid. Please try again.")


def main():
    menu()


main()
