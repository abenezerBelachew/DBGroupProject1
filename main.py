import sqlite3
import sys
import program_messages as pm
import queries as q
from datetime import datetime, date
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
            sys.exit()
    else:
        # TODO: Allow user to try again
        print(pm.uid_not_exist)
        sys.exit()
    

def register_birth(database, user):
    """
    Register a birth.The agent should be able to register a birth by providing the first name, the last name, 
    the gender, the birth date, the birth place of the newborn, as well as the first and last names of the parents.
     The registration date is set to the day of registration (today's date) and the registration place is set to
    the city of the user. The system should automatically assign a unique registration number to the birth record.
    The address and the phone of the newborn are set to those of the mother. If any of the parents is not in the
    database, the system should get information about the parent including first name, last name, birth date,
    birth place, address and phone. For each parent, any column other than the first name and last name can be 
    null if it is not provided.
    """
    c = database.cursor()
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


    # TODO: If parents not in db, system should get fn, ln, bd, bp, address, phone
    # check if father is in persons
    c.execute("SELECT fname, lname FROM persons WHERE fname = ? AND lname = ?", (f_fname, f_lname))
    father = c.fetchall()
    if len(father) == 0:
         print("It appears that your father is not in the database.")
         bdate = str(input("Father's Birth Date (YYYY-MM-DD): "))
         bplace = str(input("Father's Birth Place: "))
         address = str(input("Father's Address: "))
         phone = str(input("Father's Phone: "))

         # insert into database
         c.execute(q.insert_into_persons, (f_fname, f_lname, bdate, bplace, address, phone))

         database.commit()

    # check if mother is in persons
    c.execute("SELECT fname, lname FROM persons WHERE fname = ? AND lname = ?", (m_fname, m_lname))
    mother = c.fetchall()
    if len(mother) == 0:
         print("It appears that your mother is not in the database.")
         bdate = str(input("Mother's Birth Date (YYYY-MM-DD): "))
         bplace = str(input("Mother's Birth Place: "))
         address = str(input("Mother's Address: "))
         phone = str(input("Mother's Phone: "))

        # insert into database
         c.execute(q.insert_into_persons, (m_fname, m_lname, bdate, bplace, address, phone))

         database.commit()

    # print("User: ", user)
    
    c.execute(q.get_user_city, (user,))
    user_city = c.fetchone()
    city = user_city[0]
    regplace = city

    try:
        c.execute("SELECT phone, address FROM persons WHERE fname = ? AND lname = ?", (m_fname, m_lname))
        result = c.fetchone()
        phone = result[0]
        address = result[1]
    except:
        print(pm.something_went_wrong)
        sys.exit()
    
    reg_birth_data = [regno, fname, lname, regdate, regplace, gender, f_fname, f_lname, m_fname, m_lname]
    person_data = [fname, lname, birth_date, birth_place, address, phone]

    try:
        c.execute(q.insert_into_births, reg_birth_data)
        c.execute(q.insert_into_persons, person_data)
    except:
        print(pm.something_went_wrong)
        sys.exit()    
     


    database.commit()
    print(pm.all_done)


def register_marriage(database, user):
    """
    The user should be able to provide the names of the partners and the system should assign the registration 
    date and place and a unique registration number as discussed in registering a birth. If any of the partners
    is not found in the database, the system should get information about the partner including first name,
    last name, birth date, birth place, address and phone. For each partner, any column other than the first name
    and last name can be null if it is not provided.
    """
    try:
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

        
        if p1_fname == "" or p1_lname == "" or p2_fname == "" or p2_lname == "":
            print("You must enter first name and last name of both partners.")
            sys.exit()
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

            if fname == "" or lname == "":
                print("First and Last name must be provided.")
                sys.exit()

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

            if fname == "" or lname == "":
                print("First and Last name must be provided.")
                sys.exit()
            # Insert into persons table
            c.execute(q.insert_into_persons, person2_data)
        
        
        # Insert into marriages
        c.execute(q.insert_into_marriages, (regno, regdate, regplace, p1_fname, p1_lname, p2_fname, p2_lname))    
        print(pm.all_done)
    except:
        print(pm.something_went_wrong)
        sys.exit() 

def renew_registration(database, user):
    """
    Renew a vehicle registration.The user should be able to provide an existing registration number and 
    renew the registration. The system should set the new expiry date to one year from today's date if 
    the current registration either has expired or expires today. Otherwise, the system should set the
     new expiry to one year after the current expiry date.
    """
    try:
        print(pm.renew_registration)

        c = database.cursor()
        c.execute(q.get_reg_num_date)
        reg_num_date = c.fetchall()
        
        # contains the registration number as keys and date as values
        registration_dict = {}
        for num_date in reg_num_date:
            registration_dict[num_date[0]] = num_date[1]

        reg_number = str(input("Existing registration number: "))
        # check if reg_number exists in the database
        if int(reg_number) in registration_dict.keys():
            are_you_sure = str(input("Are you sure you want to renew your registration? (Y/N) ")).upper()
            if are_you_sure == 'Y':
                # The system should set the new expiry date to one year from today's date if 
                # the current registration either has expired or expires today. Otherwise, the system should set the
                # new expiry to one year after the current expiry date.
                the_date = datetime.today().strftime('%Y-%m-%d') # 2019-11-02 str
                todays_date = datetime.strptime(the_date, '%Y-%m-%d') # 2019-11-02 00:00:00 datetime.datetime
                # print(registration_dict[int(reg_number)])
                current_expiry = datetime.strptime(registration_dict[int(reg_number)], '%Y-%m-%d')

                # if the current expiry has passed or is today
                if  current_expiry <= todays_date:
                    c.execute(q.update_expiry, (add_years(todays_date, 1).strftime('%Y-%m-%d'), reg_number))

                else:
                    c.execute(q.update_expiry, (add_years(current_expiry, 1).strftime('%Y-%m-%d'), reg_number))
            else:
                print('OK, closing down.')
                sys.exit()
        else:
            # registration number not in database
            print(pm.reg_num_not_in_db)

        print(pm.all_done)
        database.commit()
        print(pm.all_done)
    except:
        print(pm.something_went_wrong)
        sys.exit() 

def add_years(d, years):
    """Return a date that's `years` years after the date (or datetime)
    object `d`. Return the same calendar date (month and day) in the
    destination year, if it exists, otherwise use the following day
    (thus changing February 29 to March 1).
    Source: https://stackoverflow.com/questions/15741618/add-one-year-in-current-date-python

    """
    try:
        return d.replace(year = d.year + years)
    except ValueError:
        return d + (date(d.year + years, 3, 1) - date(d.year, 3, 1))

# def process_payment(database, user):
#     """
#     Process a payment.The user should be able to record a payment by entering a valid ticket number 
#     and an amount. The payment date is automatically set to the day of the payment (today's date).
#     A ticket can be paid in multiple payments but the sum of those payments cannot exceed the fine
#     amount of the ticket.
#     """
#     tno = int(input("Ticket Number: "))
#     amount = int(input("Amount: "))
#     payment_date = datetime.today().strftime('%Y-%m-%d') # today


def issue_ticket(database, user):
    """ 
    Issue a ticket.The user should be able to provide a registration number and see the person name
    that is listed in the registration and the make, model, year and color of the car registered. 
    Then the user should be able to proceed and ticket the registration by providing a violation date,
    a violation text and a fine amount. A unique ticket number should be assigned automatically and
    the ticket should be recorded. The violation date should be set to today's date if it is not 
    provided.
    """
    try:
        # check if user is an officer
        c = database.cursor()
        c.execute('SELECT utype FROM users WHERE uid = ?', (user, ))
        user_type = c.fetchone()[0]

        # If user is an officer 
        if user_type == 'o':
            reg_num = int(input("Registration number: "))
            c.execute("""SELECT p.fname, p.lname, v.make, v.model, v.year, v.color FROM registrations r JOIN
            persons p ON (r.fname, r.lname) = (p.fname, p.lname) JOIN vehicles v ON r.vin = v.vin WHERE r.regno = ?""",(reg_num,))
            result = c.fetchone()
            fname = result[0]
            lname = result[1]
            make = result[2]
            model = result[3]
            year = result[4]
            color = result[5]
            print("\n--------------------------\nInformation\n--------------------------\n")
            print("First Name: ", fname)
            print("Last Name: ", lname)
            print("Make: ", make)
            print("Model: ", model)
            print("Year: ", year)
            print("Color: ", color)

            print("\n-------------------------\nTicket the registra: \n------------------------\n")
            violation_date = str(input("Violation Date: ")) # if not provided, today's date
            if violation_date == "":
                violation_date = datetime.today().strftime('%Y-%m-%d')
            violation_text = str(input("violation Text: "))
            amount = str(input("Amount: "))
            tno = randrange(1001, 9867699)

            c.execute(q.insert_into_tickets, (tno, reg_num, amount, violation_text, violation_date))

            database.commit()
            print(pm.all_done)
        # if user is not an officer
        else:
            print(pm.for_officers_only)
            sys.exit()
    except:
        print(pm.something_went_wrong)
        sys.exit() 
def find_car_owner(database, user):
    """
    Find a car owner.The user should be able to look for the owner of a car by providing one or more of 
    make, model, year, color, and plate. The system should find and return all matches. If there are more
    than 4 matches, you will show only the make, model, year, color, and the plate of the matching cars 
    and let the user select one. When there are less than 4 matches or when a car is selected from a list
    shown earlier, for each match, the make, model, year, color, and the plate of the matching car will
    be shown as well as the latest registration date, the expiry date, and the name of the person listed in
    the latest registration record.
    """
    try:
        # check if user is an officer
        c = database.cursor()
        c.execute('SELECT utype FROM users WHERE uid = ?', (user, ))
        user_type = c.fetchone()[0]

        # If user is an officer 
        if user_type == 'o':
            print(pm.car_own)
            c = database.cursor()

            make = str(input("Make: "))
            model = str(input("Model: "))
            year = int(input("Year: "))
            color = str(input("Color: "))
            plate = str(input("Plate: "))

            c.execute("""SELECT DISTINCT p.fname, p.lname FROM persons p JOIN registrations r ON (r.fname, r.lname) = 
            (p.fname, p.lname) JOIN vehicles v ON r.vin = v.vin WHERE v.make = ? OR v.model = ? OR v.year = ? OR v.color = ?
            OR r.plate = ?""", (make, model, year, color, plate))
            result = c.fetchall()

            if len(result) > 4:
                c.execute("""SELECT DISTINCT r.fname, r.lname, v.make, v.model, v.year, v.color, r.plate FROM persons p JOIN registrations r
                ON (r.fname, r.lname) = (p.fname, p.lname) JOIN vehicles v ON r.vin = v.vin WHERE v.make = ? OR v.model = ? OR
                v.year = ? OR v.color = ? OR r.plate = ?""", (make, model, year, color, plate))
                result = c.fetchall()
                for values in result:
                    print("\n-----------------------------------------")
                    print(f"Full Name: {values[0]} {values[1]}")
                    print("------------------------------------------")
                    print(f"Make: {values[2]}")
                    print(f"Model: {values[3]}")
                    print(f"Year: {values[4]}")
                    print(f"Color: {values[5]}")
                    print(f"Plate: {values[6]}")
            elif len(result) <= 4:
                c.execute("""SELECT DISTINCT r.fname, r.lname, v.make, v.model, v.year, v.color, r.plate, r.regdate, r.expiry FROM persons p JOIN registrations r
                ON (r.fname, r.lname) = (p.fname, p.lname) JOIN vehicles v ON r.vin = v.vin WHERE v.make = ? OR v.model = ? OR
                v.year = ? OR v.color = ? OR r.plate = ?""", (make, model, year, color, plate))
                result = c.fetchall()
                for values in result:
                    print("\n-----------------------------------------")
                    print(f"Full Name: {values[0]} {values[1]}")
                    print("------------------------------------------")
                    print(f"Make: {values[2]}")
                    print(f"Model: {values[3]}")
                    print(f"Year: {values[4]}")
                    print(f"Color: {values[5]}")
                    print(f"Plate: {values[6]}")
                    print(f'Registration Date: {values[7]}')
                    print(f"Expiry: {values[8]}")
            

            print(pm.all_done)
        else:
            print(pm.for_officers_only)
            sys.exit()
    except:
        print(pm.something_went_wrong)
        sys.exit() 
            

    


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


# Add your functions here
def bill_sale(database, user):
    '''The user should be able to record a bill of sale by providing the vin of a car, the name of the current owner, the name of the new owner, and a plate number for the new registration. '''
    regno = randrange(1001, 9867699)
    
    vin = str(input('VIN: '))
    c_fname = str(input("Current owner's first name': "))
    c_lname = str(input("Current owner's last name: "))
    c = database.cursor()
    c.execute(q.get_latest_owner,(vin,))
    name = c.fetchone()
    try:
    
        if name[0] == c_fname and name[1] == c_lname:
            
            n_fname = str(input("New owner's first name: "))
            n_lname = str(input("New owner's last name: "))
            plate = str(input('Plate number: '))
            todaysdate = regdate = datetime.today().strftime('%Y-%m-%d')
            a_year_after = datetime.today().replace(year= datetime.today().year +1).strftime('%Y-%m-%d')
        
            c.execute(q.update_current,(todaysdate,name[2]))
            c.execute(q.new_registrations,(regno,todaysdate,a_year_after,plate,vin,n_fname,n_lname))
        else :
            print(q.not_current_owner)  
        print(pm.all_done)
    except:
        print(pm.something_went_wrong)
        sys.exit()

def pro_payments(database, user):
    '''The user should be able to record a payment by entering a valid ticket number and an amount.'''
    tno = int(input("Enter a valid ticket number: "))
    amount = int(input("Enter an amount: "))
    pdate  = (datetime.today().strftime('%Y-%m-%d'))

    c = database.cursor()
    c.execute(q.get_fine,(str(tno),))
    fine_amount = c.fetchone()[0]
    c.execute(q.get_sum,(str(tno),))
    payment_sum = c.fetchone()[0]
    try:
        if payment_sum == None:
            payment_sum = 0
        if amount <=(fine_amount - payment_sum):
            c.execute(q.insert_payment,(tno,pdate,amount,))
        
        else:
            print("Amount should be less than fine amount.")
            sys.exit()
    except:
        print(pm.something_went_wrong)
        sys.exit()
    print(pm.all_done)

        
def get_abstract(database, user):
    
    
    fname = str(input("Enter driver first name: "))
    lname = str(input("Enter driver last name: "))
    try:
        _2yearsago =  datetime.today().replace(datetime.today().year - 2)
        c = database.cursor()
        c.execute(q.get_demerit,(fname,lname))
        nuum = c.fetchone()
        c.execute(q.get_demerit2,(fname,lname,_2yearsago))
        nuum2 = c.fetchone()    
        
        option = input("Do you want to order tickets(yes/no):  ")
        if option.upper() == "YES":
            get_regno = q.get_regno_ordered
            get_regnod = q.get_regno_ordered_dis
        else:
            get_regno = q.get_regno
            get_regnod = q.get_regno_dis
        c.execute(get_regno,(fname,lname))
        regno = c.fetchall()
        c.execute(get_regnod,(fname,lname))
        regnod = c.fetchall()
    except:
        print(pm.something_went_wrong)
    try:
        tickets = 0 
        tickets2 = 0
        ticket_desc = []
        ticket_desc2 = []
        for i in regnod:
            regno1 = str(i[0])
            c.execute(q.get_tickets,(regno1,))
            ticketnum = c.fetchone()[0]
            tickets += ticketnum
            c.execute(q.get_tickets2,(regno1,_2yearsago))
            ticketnum2 = c.fetchone()[0]
            tickets2 += ticketnum2
            c.execute(q.get_ticket_desc,(regno1,))
        for  i in regno:
            regno1 = str(i[0])
            t_desc = c.fetchone()
            c.execute(q.get_ticket_desc2,(regno1,_2yearsago))
            t_desc2 = c.fetchone()
            
            
            ticket_desc.append(t_desc)
            ticket_desc2.append(t_desc2)
        low_index=5
        high_index=9
        num_of_results = len(ticket_desc)
       # print(a,'>>>>>>>>>>>>>>>>>>')
        if num_of_results>5 :
            pm.printmsg(tickets, nuum,ticket_desc, tickets2, nuum2, ticket_desc2)
            answer = input("Do you want to see more(yes/no): ")
            
            while answer.upper() == "YES" and low_index< num_of_results :
                print("In lifetime")
                print(ticket_desc[low_index:high_index])
                print("In last 2 years")
                print(ticket_desc2[low_index:high_index])
                low_index +=5
                high_index += 5
                answer = input("Do you want to see more(yes/no): ")
                
        else:
            pm.printmsg(tickets, nuum,ticket_desc, tickets2, nuum2, ticket_desc2)
    except:
        print(pm.something_went_wrong)
        sys.exit()
    print(pm.all_done)
        

def main():
    """ Connects to database and other modules."""
    database = get_database()
    # If the user can log in
    status, active_user = login(database)
    if status:
        print(pm.logged_in)
        print("User in main: ", active_user, "\n------------------------------")
        

        print("List of Commands:")
        for command in pm.help_commands:
            # list all available commands
            print(command)
       
        command = str(input("\n----------\nCommand: ")).upper()
        
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
        
        elif command == "RENVEH":
            renew_registration(database, active_user)
        
        elif command == "PROBIL":
            bill_sale(database, active_user)
        
        elif command == "PROPAY":
            pro_payments(database, active_user)
        
        elif command == "DRIABS":
            get_abstract(database, active_user)

        elif command == "ISUTIC":
            issue_ticket(database, active_user)

        elif command == "CAROWN":
            find_car_owner(database, active_user)

        elif command == "HELP":
            for help_command in pm.help_commands:
                print(help_command)
    else:
        print("Not logged in.")    

    # # register birth
    # if active_user != "":
    # register_birth(database, active_user)


    database.commit()
    database.close()


if __name__ == '__main__':
    main()