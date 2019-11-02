import sqlite3
import sys
from random import randrange
from datetime import datetime
import program_messages as pm
import getpass
help_commands = ["RegBir to Register a Birth", 
            "RegMar to Register a Marriage",
            "RenVeh to Renew a vehicle",
            "ProBil to Process a bill of sale",
            "ProPay to Process a payment",
            "DriAbs to Get a driver abstract",
            "IsuTic to Issue a ticket",
            "CarOwn to Find a car owner"]


# print(sys.argv[1])
# print(type(sys.argv[1]))
# print(len(sys.argv))

# if (len(sys.argv) > 1):
#     pass
# else:
#     print("Please enter a command.\nType help to see list of commands.")

# if sys.argv[1] == "help":
#     print(':)')


# For the arguments
# Checks if there is an argument provided
    # if len(sys.argv) > 1:
    #     # Checks if it's a valid argument
    #     if sys.argv[1] in pm.lst_of_commands:
    #         # If command is help, list all available commands
    #         if sys.argv[1] == "help":
    #             for help_command in ps.help_commands:
    #                 print(f'|- {help_command} ')
    #         # if quit, close database and application
    #         elif sys.argv[1] == "quit":
    #             # TODO: Quit the database
    #             print(pm.quit_message)
    #             sys.exit()
    #     else:
    #         print(pm.provide_valid_argument)
    # else:
    #     print(pm.provide_argument)

db = sqlite3.connect("testDb.db")
c = db.cursor()


# 1) Contents of all columns for row that match a certain value in 1 column
credential = {}
c.execute("SELECT uid, pwd FROM users;")
all_rows = c.fetchall()
c.execute("SELECT city FROM users WHERE uid =?", ('user1', ))
city  = c.fetchone()[0]
print(city)
print(type((city)), end = "\n\n\n")


for row in all_rows: 
    print(row[0], row[1])
    # print(f"UN: {row[0]} PW:{row[1]}")
    # credential[row[0]] = row[1]

# for uname, pw in credential.items():
#     print(uname, " ", pw)


c.execute("SELECT p.phone, p.address, b.m_fname, b.m_lname FROM persons p JOIN births b ON (p.fname, p.lname) = (b.m_fname, b.m_lname) WHERE m_fname = ? AND m_lname = ?", ("Linda", "Smith",))
pho_add = c.fetchone()
print(type(pho_add[0]))
# for pa in pho_add:
#     print(pa)
#     print(f"phone: {pa[0]}|||||||||address: {pa[1]}|||||||||m_fname: {pa[2]}|||||||||m_lname: {pa[3]}")

# print(datetime.today().strftime('%Y-%m-%d'))
# print(type(datetime.today().strftime('%Y-%m-%d')))


# print(type(randrange(1001, 9899)))

# def p():
#     return (True, "user")

# def q():
#     print(p()[1])
#     if p()[0]:
#         print("P true")

# q()

# password = getpass.getpass(prompt="Password: ")
# print(password)
# print(type(password)
c.execute('SELECT fname, lname FROM persons WHERE fname = "Davoo" AND lname = "Rafii"')
result = c.fetchall()
print(len(result) == 0)

