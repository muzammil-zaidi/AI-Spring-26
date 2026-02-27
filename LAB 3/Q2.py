import time

class FloorCleaningRobot:
    def __init__(self):
        self.rooms = {
            1: False,
            2: False,
            3: False
        }
        self.position = 1

    def perceive(self):
        return self.rooms[self.position]

    def clean(self):
        self.rooms[self.position] = True
        print(f"Cleaned Room {self.position}")

    def move_right(self):
        if self.position < 3:
            self.position += 1
            print(f"Moved to Room {self.position}")

    def move_left(self):
        if self.position > 1:
            self.position -= 1
            print(f"Moved to Room {self.position}")

    def all_clean(self):
        return all(self.rooms.values())

    def run(self):
        print("Starting cleaning process...\n")

        while not self.all_clean():
            print(f"Robot is in Room {self.position}")

            if not self.perceive():
                self.clean()
            else:
                print(f"Room {self.position} is already clean")

            if self.position < 3:
                self.move_right()
            else:
                self.move_left()

            time.sleep(1)
            print("-" * 30)

        print("\nAll rooms are clean. Task completed!")

robot = FloorCleaningRobot()
robot.run()
