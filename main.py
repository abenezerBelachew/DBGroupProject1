import sqlite3
import sys
import program_messages as pm
from os import path



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
    cursor = database.cursor()
   
    # Just for test
    cursor.execute("SELECT name FROM sqlite_master WHERE type = 'table';")
    print(cursor.fetchall())
    # -------------------


if __name__ == '__main__':
    main()