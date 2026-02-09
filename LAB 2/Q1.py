class Light:
    def __init__(self, room_name):
        self.room_name = room_name
        self.status = "OFF"

    def turn_on(self):
        self.status = "ON"
        print(f"{self.room_name} light turned ON.")

    def turn_off(self):
        self.status = "OFF"
        print(f"{self.room_name} light turned OFF.")

    def display_status(self):
        print(f"{self.room_name} light is {self.status}.")


living_room_light = Light("Living Room")
bedroom_light = Light("Bedroom")

living_room_light.turn_on()
bedroom_light.turn_off()

living_room_light.display_status()
bedroom_light.display_status()
