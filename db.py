<<<<<<< HEAD
# Adam J BuildADatabase
=======
# Adam J CSCE 4350 - BuildADatabase
>>>>>>> 3f138245a86f68741e55d94eea00e0608e4c87ba
import os
import sys
DB_FILE = "data.db"

class KeyValueStore:
    """
    Is a simple persistent key value store that uses an append only log file and the in memory index is stored as a list of the tuples
    """

    def __init__(self):
        # is the In memory storage of the list of tuples
        self.store = []
        self.load_data()

    def load_data(self):
        """
        It rebuilds the in memory index by replaying the append only log file 
        """
        if not os.path.exists(DB_FILE):
            return
        try:
            with open(DB_FILE, "r") as f:
                for line in f:
                    parts = line.strip().split(" ", 2)

                    if len(parts) == 3 and parts[0] == "SET":
                        key = parts[1]
                        value = parts[2]
                        self.set_memory(key, value)
        except Exception:
            pass

    def set_memory(self, key, value):
        """
        Updates the in memory store and if a key already exists it will overwrite it 
        """
        for i in range(len(self.store)):
            if self.store[i][0] == key:
                self.store[i] = (key, value)
                return

        # If a key doesn’t exist it will add it 
        self.store.append((key, value))

    def set(self, key, value):
        """
        Continues the SET command to disk and updates the memory
        """
        try:
            with open(DB_FILE, "a") as f:
                f.write(f"SET {key} {value}\n")
        except Exception:
            pass

        self.set_memory(key, value)

    def get(self, key):
        """
        Retrieves a value from the in memory store
        """
        for k, v in self.store:
            if k == key:
                return v
        return None


def main():
    """
    Is a command line interface that's able to read the commands from stdin
    """
    db = KeyValueStore()

    for line in sys.stdin:
        command = line.strip()

        if not command:
            continue

        parts = command.split(" ", 2)

        if parts[0] == "SET" and len(parts) == 3:
            db.set(parts[1], parts[2])

        elif parts[0] == "GET" and len(parts) == 2:
            result = db.get(parts[1])
            if result is not None:
                print(result, flush=True)

        elif parts[0] == "EXIT":
            break

if __name__ == "__main__":
    main()
