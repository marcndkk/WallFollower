from gpiozero import DistanceSensor

class Sonar:
    def __init__(self, echo_pin, trigger_pin):
        self.sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin)

    def get_distance(self):
        return self.sensor.distance * 100
