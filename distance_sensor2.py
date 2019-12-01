from pigpio_ranger import ranger
import pigpio

class Sonar:
    def __init__(self, echo_pin, trigger_pin):
        self.pi = pigpio.pi()
        self.ranger = ranger(self.pi, trigger_pin, echo_pin)

    def get_distance(self):
        output = self.ranger.read()
        distance = output / 1000000.0 * 34030 
        return distance

    def stop(self):
        self.ranger.cancel()
        self.pi.stop()
