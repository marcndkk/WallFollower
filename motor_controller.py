from gpiozero import CamJamKitRobot

class MotorController:
    def __init__(self):
        self.robot = CamJamKitRobot()
        self.values = (0, 0)

    def get_values(self):
        return self.values

    def set_values(self, left, right):
        left = self._validate_value(left)
        right = self._validate_value(right)
        self.values = (left, right)
        self.robot.value = self.values

    def _validate_value(self, value):
        if value > 1:
            return 1
        elif value < -1:
            return -1
        else:
            return value
