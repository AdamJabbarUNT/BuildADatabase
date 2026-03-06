# Adam J BuildADatabase

import os

# Name of the file where the database commands will be located 
DB_FILE = "data.db"

class KeyValueStore:
    def __init__(self):
        # Stores it as list that are tuples that are key and value
        self.store = [] 

        # Loads any existing data from the datafile whenever the program starts 
        self.load_data()

    def load_data(self):
        # Nothing will be loaded if the database file doesnt exist when the program starts 
        if not os.path.exists(DB_FILE):
            return

        # Opens the database file and replays all the stored SET commands 
        with open(DB_FILE, "r") as f:
            for line in f:
                #Splits the Line into command parts and makes it expect SET key value 
                parts = line.strip().split(" ", 2)

                # Checks if the line is a valid set command 
                if len(parts) == 3 and parts[0] == "SET":
                    key = parts[1]
                    value = parts[2]

                # Restores the key value pair in the memory 
                    self.set_memory(key, value)

    def set_memory(self, key, value):
        # Updates the value if the key already exists in the memory 
        for i in range(len(self.store)):
            if self.store[i][0] == key:
                self.store[i] = (key, value)
                return

        # If the key doesn't exist it will add a new key value pair 
        self.store.append((key, value))

    def set(self, key, value):
    # Adds the SET command to the database file and keeps a peristent log of all the operations
        with open(DB_FILE, "a") as f:
            f.write(f"SET {key} {value}\n")

        # Updates the in memory store as well 
        self.set_memory(key, value)

    def get(self, key):
        # Searches for the key in the in memory store 
        for k, v in self.store:
            if k == key:
                return v
                # Return Nothing if the key doesn't exist 
        return None


def main():
    # Creates the key value database instance 
    db = KeyValueStore()

    # Always reads the commands from the user 
    while True:
        try:
            command = input().strip()
        except EOFError:
            # Stops if there isnt any more input 
            break

        # Ignores any empty commands 
        if not command:
            continue
        # Splits the command into parts 
        parts = command.split(" ", 2)

        # Handles the SET command 
        if parts[0] == "SET" and len(parts) == 3:
            db.set(parts[1], parts[2])

        # Handles the GET command 
        elif parts[0] == "GET" and len(parts) == 2:
            result = db.get(parts[1])
        # Prints the stored value or puts NULL if its not found 
            if result:
                print(result)
            else:
                print("NULL")

        # Exits the program
        elif parts[0] == "EXIT":
            break
        # Handles any invalid commands 
        else:
            print("Invalid command")

# Runs the main function whenever the script is used 
if __name__ == "__main__":
    main()
