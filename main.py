import sqlite3
import sys
import program_messages as pm
import queries as q
from datetime import datetime
from os import path
from random import randrange
import getpass


login_credentials = {}
active_user = ""

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
    pwd = getpass.getpass(prompt="Your Password: ")


    if uid in login_credentials.keys():
        # If the uid matches its associated pwd, return True
        if login_credentials[uid] == pwd:
            # active_user = uid
            return (True, uid)
        else:
            print(pm.password_incorrect)
    else:
        # TODO: Allow user to try again
        print(pm.uid_not_exist)
    

def register_birth(database, user):
    """The agent should be able to register a birth by providing the first name, the last name, 
    the gender, the birth date, the birth place of the newborn, as well as the first and last 
    names of the parents."""
    regno = randrange(1001, 9867699)
    fname = str(input("First Name: "))
    lname = str(input("Last Name: "))
    gender = str(input("Gender(F/M): ").upper())
    birth_date = str(input("Birth Date(YYYY-MM-DD): "))
    birth_place = str(input("Birth Place: "))
    f_fname = str(input("Father's First Name: "))
    f_lname = str(input("Father's Last Name: "))
    m_fname = str(input("Mother's First Name: "))
    m_lname = str(input("Mother's Last Name: "))
    regdate = datetime.today().strftime('%Y-%m-%d')

    # print("User: ", user)
    c = database.cursor()
    c.execute(q.get_user_city, (user,))
    user_city = c.fetchone()
    city = user_city[0]
    regplace = city

    try:
        c.execute(q.get_phone_address, (m_fname, m_lname, ))
        phone = c.fetchone()[0]
        address = c.fetchone()[1]
    except:
        print(pm.something_went_wrong)
        sys.exit()
    
    reg_birth_data = [regno, fname, lname, regdate, regplace, gender, f_fname, f_lname, m_fname, m_lname]
    person_data = [fname, lname, birth_date, birth_place, address, phone]

    c.execute(q.insert_into_births, reg_birth_data)
    c.execute(q.insert_into_persons, person_data)
    
    # TODO: If parents not in db, system should get fn, ln, bd, bp, address, phone
    


def register_marriage(database, user):
    """
    The user should be able to provide the names of the partners and the system should assign the registration 
    date and place and a unique registration number as discussed in registering a birth. If any of the partners
    is not found in the database, the system should get information about the partner including first name,
    last name, birth date, birth place, address and phone. For each partner, any column other than the first name
    and last name can be null if it is not provided.
    """
    regno = randrange(1001, 9867699)
    regdate = datetime.today().strftime('%Y-%m-%d')
    
    c = database.cursor()
    c.execute(q.get_user_city, (user,))
    user_city = c.fetchone()
    city = user_city[0]
    regplace = city

    p1_fname = str(input("Person 1 First Name: "))
    p1_lname = str(input("Person 1 Last Name: "))
    p2_fname = str(input("Person 2 First Name: "))
    p2_lname = str(input("Person 2 Last Name: "))

    # If partner is not found in the database, add them
    c.execute(q.get_first_last_name, (p1_fname, p1_lname))
    result = c.fetchall()
    # if person1 doesn't exist in the persons database 
    if len(result) == 0:
        # ask the additional questions here
        print("Please add information for person 1 to persons table by answering the ff questions.")
        fname = str(input("First Name: "))
        lname = str(input("Last Name: "))
        bdate = str(input("Birth Date(YYYY-MM-DD): "))
        bplace = str(input("Birth Place: "))
        address = str(input("Address: "))
        phone = str(input("Phone(XXX-XXX-XXXX): "))
        person1_data = [fname, lname, bdate, bplace, address, phone]

        # Insert into persons table
        c.execute(q.insert_into_persons, person1_data)
        
    
    c.execute(q.get_first_last_name, (p2_fname, p2_lname))
    result = c.fetchall()
    if len(result) == 0:
        # ask the additional questions here
        print("Please add information for person 2 to persons table by answering the ff questions.")
        fname = str(input("First Name: "))
        lname = str(input("Last Name: "))
        bdate = str(input("Birth Date(YYYY-MM-DD): "))
        bplace = str(input("Birth Place: "))
        address = str(input("Address: "))
        phone = str(input("Phone(XXX-XXX-XXXX): "))
        person2_data = [fname, lname, bdate, bplace, address, phone]

        # Insert into persons table
        c.execute(q.insert_into_persons, person2_data)
    
    
    # Insert into marriages
    c.execute(q.insert_into_marriages, (regno, regdate, regplace, p1_fname, p1_lname, p2_fname, p2_lname))    



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
    status, active_user = login(database)
    if status:
        print(pm.logged_in)
        print("User in main: ", active_user)
        

        for command in pm.help_commands:
            # list all available commands
            print(command)
       
        command = str(input("Command: ")).upper()
        
        # If command not in the list of commands, keep asking user
        # for a valid command.
        while command not in pm.lst_of_commands:
            print(pm.invalid_command)
            command = str(input("Command: ")).upper()
            
        if command == "QUIT":
            print(pm.quit_message)
            sys.exit()

        elif command == "REGBIR":
            # for registering birth
            print(pm.register_birth)
            register_birth(database, active_user)
        
        elif command == "REGMAR":
            print(pm.register_marriage)
            register_marriage(database, active_user)

    else:
        print("Not logged in.")    

    # # register birth
    # if active_user != "":
    #     register_birth(database, active_user)


    database.commit()
    database.close()


if __name__ == '__main__':
    main()