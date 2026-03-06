import os

DB_FILE = "data.db"

class KeyValueStore:
    def __init__(self):
        self.store = []
        self.load_data()

    def load_data(self):
        if not os.path.exists(DB_FILE):
            return

        with open(DB_FILE, "r") as f:
            for line in f:
                parts = line.strip().split(" ", 2)

                if len(parts) == 3 and parts[0] == "SET":
                    key = parts[1]
                    value = parts[2]
                    self.set_memory(key, value)

    def set_memory(self, key, value):
        for i in range(len(self.store)):
            if self.store[i][0] == key:
                self.store[i] = (key, value)
                return

        self.store.append((key, value))

    def set(self, key, value):
        with open(DB_FILE, "a") as f:
            f.write(f"SET {key} {value}\n")

        self.set_memory(key, value)

    def get(self, key):
        for k, v in self.store:
            if k == key:
                return v
        return None


def main():
    db = KeyValueStore()

    while True:
        try:
            command = input().strip()
        except EOFError:
            break

        if not command:
            continue

        parts = command.split(" ", 2)

        if parts[0] == "SET" and len(parts) == 3:
            db.set(parts[1], parts[2])

        elif parts[0] == "GET" and len(parts) == 2:
            result = db.get(parts[1])
            if result:
                print(result)
            else:
                print("NULL")

        elif parts[0] == "EXIT":
            break

        else:
            print("Invalid command")


if __name__ == "__main__":
    main()