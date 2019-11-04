# Commands related
provide_argument = "Please enter a command. \nType help to see list of commands."
provide_valid_argument = "Please provide a valid argument. \nType help to see a list of available commands."
help_commands = ["RegBir to Register a Birth", 
            "RegMar to Register a Marriage",
            "RenVeh to Renew a vehicle",
            "ProBil to Process a bill of sale",
            "ProPay to Process a payment",
            "DriAbs to Get a driver abstract",
            "IsuTic to Issue a ticket",
            "CarOwn to Find a car owner",
            "Help to see available commands",
            "Quit to quit",]
lst_of_commands = ["REGBIR", "REGMAR", "RENVEH", "PROBIL",
                    "PROPAY", "DRIABS", "ISUTIC", "CAROWN",
                    "HELP", "QUIT"]
invalid_command = "Please type in a valid command."

# Database related
db_not_found = "Database not found. Make sure you typed it correctly."
provide_db_name = "Please provide a database name."


# General
quit_message = "Closing everything..bye"
something_went_wrong = "Something went wrong"
try_again = "Try again.."
all_done = "\n****************\nAll Done :)\n****************\n"


# Login
password_incorrect = "Password Incorrect."
uid_not_exist = "Uid does not exist in database."
logged_in = "------------------------------\nYou're logged in.\n------------------------------"

# birth
register_birth = "\n----------------------\nRegister a birth\n----------------------\n"


# Marriage
register_marriage = "\n----------------------\nRegister a Marriage\n----------------------\n"

# Registrations
renew_registration = "\n----------------------\nRenew Registration\n----------------------\n"
reg_num_not_in_db = "\n----------------------\nRegistration number not in database\n----------------------\n"


# Officers
for_officers_only = "Access Denied! Sorry, this feature is for officers only."

# carown
car_own = "\n----------------------\nFind owner of a car\n----------------------\n"


# arthur
process_bill = 'Processing bill of sale'
process_pay = "Processing payment"
driverabstract = "Getting driver abstract"
def printmsg(tickets, nuum,ticket_desc, tickets2, nuum2, ticket_desc2):
    print("In drivers lifetime")
    print("# of Tickets =",tickets)
    print("# of notices =", nuum[0])
    print("sum of points = ",nuum[1])
    print("The ticket number,violation date, violation description, fine,registration number,make,model")
    print(*ticket_desc, sep = '\n')
    
    print("In the last 2 years")
    print("# of Tickets =",tickets2)
    print("# of notices =", nuum2[0])
    print("sum of points = ",nuum2[1]) 
    print("The ticket number,violation date, violation description, fine,registration number,make,model")
    print(*ticket_desc2, sep = '\n')

print(lst_of_commands)
