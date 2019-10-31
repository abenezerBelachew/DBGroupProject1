import sqlite3
import sys
import program_messages as pm
import queries as q
from os import path


login_credentials = {}

def login(database):
    """ Returns true if login credentials work. """
    c = database.cursor()
    c.execute(q.get_uid_pwd)
    uid_pwd = c.fetchall()
    # Assign every username, password combination to the login_credentials dictionary
    for u_p in uid_pwd:
        login_credentials[u_p[0]] = u_p[1]

    # Ask user for uid and pwd
    uid = str(input("Your uid: "))
    pwd = str(input("Your password: "))


    if uid in login_credentials.keys():
        # If the uid matches its associated pwd, return True
        if login_credentials[uid] == pwd:
            return True
        else:
            print(pm.password_incorrect)
    else:
        # TODO: Allow user to try again
        print(pm.uid_not_exist)
    
    # c.execute(q.get_uid_pwd)
    # uid_pwd = c.fetchall()
    # for uid, pwd in uid_pwd:
    #     login_credentials[uid] = pwd
    



def get_database():
    # Checks if there is an argument provided
    if len(sys.argv) > 1:
        # Checks if it's a valid database
        if (path.exists(sys.argv[1])):
            try:
                # Connect to and return the database
                database = sqlite3.connect(sys.argv[1])
                return database
            except:
                print(pm.something_went_wrong)
                sys.exit()
        else:
            print(pm.db_not_found)
            sys.exit()
    else:
        print(pm.provide_db_name)
        sys.exit()

def main():
    """ Connects to database and other modules."""
    database = get_database()
    # If the user can log in
    if login(database):
        print("You're logged in.")
    else:
        print("Not logged in.")
   
    



    database.commit()
    database.close()


if __name__ == '__main__':
    main()