import threading
import time

class RobotController:
    def __init__(self, distance_sensor, motor_controller):
        self.distance_sensor = distance_sensor
        self.motor_controller = motor_controller

        self.thread = None
        self.running = False 

        self.speed = 0.35
        self.target_distance = 20

    def start(self):
        if not self.running and (self.thread == None or (not self.thread.isAlive())):
            self.running = True
            self.state = 1
            self.thread = threading.Thread(target=self._run)
            self.thread.start()
        return "starting"

    def _run(self):
        while self.running:
            if self.state == 1:
                dist = self.get_dist()
                self.motor_controller.set_values(-0.35, 0.35)
                while dist > 50:
                    time.sleep(0.15)
                    dist = self.get_dist()
                self.motor_controller.set_values(0, 0)
                self.state = 2
                print("STATE 2")
            elif self.state == 2:
                correction = self._get_correction()
                self.motor_controller.set_values(self.speed - correction, self.speed + correction)
        # When stopped
        self.motor_controller.set_values(0, 0)

    def _get_direction_and_distance(self):
        distance1 = self.get_dist()
        time.sleep(0.1)
        distance2 = self.get_dist()
        direction =  distance1 - distance2
        deviation = self.target_distance - distance2
        return direction, deviation

    def _get_correction(self):
        direction, deviation = self._get_direction_and_distance()
        if direction > 0 and deviation < 0:
            correction = 0
        elif direction < 0 and deviation < 0:
            correction = -0.1
        elif direction > 0 and deviation > 0:
            correction = direction * 0.15
        else:
            correction = 0
        return correction

    def stop(self):
        self.running = False
        return "stopping"

    def get_dist(self):
        return self.distance_sensor.get_distance()

    def get_motors(self):
        return self.motor_controller.get_values()
