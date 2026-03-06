import time

class DeliveryRobot:
    def __init__(self):
        self.position = 0
        self.goal = 15
        self.steps = 0
        self.path = [self.position]

    def decide_action(self):
        """
        Goal-based decision:
        Choose the action that reduces distance to the goal.
        """
        distance_forward = abs(self.goal - (self.position + 1))
        distance_backward = abs(self.goal - (self.position - 1))

        if distance_forward <= distance_backward:
            return +1
        else:
            return -1

    def move(self, action):
        self.position += action
        self.steps += 1
        self.path.append(self.position)

    def run(self):
        print("Starting delivery robot simulation...\n")

        while self.position != self.goal:
            print(f"Current Position: {self.position}")

            action = self.decide_action()

            if action == +1:
                print("Action: Move Forward (+1)")
            else:
                print("Action: Move Backward (-1)")

            self.move(action)
            time.sleep(0.5)

        print("\nGoal reached!")
        print(f"Final Position: {self.position}")
        print(f"Total Steps Taken: {self.steps}")
        print(f"Path Visited: {self.path}")

robot = DeliveryRobot()
robot.run()
