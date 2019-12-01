import threading
import time

class RobotController:
    def __init__(self, distance_sensor, motor_controller):
        self.distance_sensor = distance_sensor
        self.motor_controller = motor_controller

        self.thread = None
        self.running = False 

        self.speed = 0.2
        self.target_distance = 13
        self.multiplier = 0.1

    def start(self):
        if not self.running and (self.thread == None or (not self.thread.isAlive())):
            self.running = True
            self.thread = threading.Thread(target=self._run)
            self.thread.start()
        return "starting"

    def _run(self):
        while self.running:
            distance = self.get_dist()
            diff = (self.target_distance - distance) * self.multiplier
            if diff > 0.03:
                diff = 0.03
            if diff < -0.03:
                diff = -0.03
            self.motor_controller.set_values(self.speed - diff, self.speed + diff)
            time.sleep(0.1)
        # When stopped
        self.motor_controller.set_values(0, 0)

    def stop(self):
        self.running = False
        return "stopping"

    def get_dist(self):
        return self.distance_sensor.get_distance()

    def get_motors(self):
        return self.motor_controller.get_values()
