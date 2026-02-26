import time

class SmartStreetLightAgent:
    def __init__(self):
        self.running = True

    def perceive_and_act(self):
        while self.running:
            light_intensity = input("Enter light intensity (Bright/Dim or Exit): ").strip().lower()

            if light_intensity == "exit":
                print("Stopping smart street light system.")
                self.running = False
                break

            motion = input("Is motion detected? (Yes/No): ").strip().lower()

            if light_intensity == "bright":
                light_status = "OFF"
            elif light_intensity == "dim" and motion == "yes":
                light_status = "ON"
            else:
                light_status = "OFF"

            print(f"Street Light Status: {light_status}")
            print("-" * 30)

            time.sleep(2)

agent = SmartStreetLightAgent()
agent.perceive_and_act()
