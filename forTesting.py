import sys
import program_messages as pm
help_commands = ["RegBir to Register a Birth", 
            "RegMar to Register a Marriage",
            "RenVeh to Renew a vehicle",
            "ProBil to Process a bill of sale",
            "ProPay to Process a payment",
            "DriAbs to Get a driver abstract",
            "IsuTic to Issue a ticket",
            "CarOwn to Find a car owner"]


print(sys.argv[1])
print(type(sys.argv[1]))
print(len(sys.argv))

if (len(sys.argv) > 1):
    pass
else:
    print("Please enter a command.\nType help to see list of commands.")

if sys.argv[1] == "help":
    print(':)')


# For the arguments
# Checks if there is an argument provided
    if len(sys.argv) > 1:
        # Checks if it's a valid argument
        if sys.argv[1] in pm.lst_of_commands:
            # If command is help, list all available commands
            if sys.argv[1] == "help":
                for help_command in ps.help_commands:
                    print(f'|- {help_command} ')
            # if quit, close database and application
            elif sys.argv[1] == "quit":
                # TODO: Quit the database
                print(pm.quit_message)
                sys.exit()
        else:
            print(pm.provide_valid_argument)
    else:
        print(pm.provide_argument)