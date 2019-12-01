import threading
import time

class RobotController:
    def __init__(self, distance_sensor, motor_controller):
        self.distance_sensor = distance_sensor
        self.motor_controller = motor_controller

        self.thread = None
        self.running = False 

        self.speed = 0.30
        self.target_distance = 14

    def start(self):
        if not self.running and (self.thread == None or (not self.thread.isAlive())):
            self.running = True
            self.thread = threading.Thread(target=self._run)
            self.thread.start()
        return "starting"

    def _run(self):
        while self.running:
            distance = self.get_dist()
            correction = self._get_correction()
            self.motor_controller.set_values(self.speed - correction, self.speed + correction)
        # When stopped
        self.motor_controller.set_values(0, 0)

    def _get_correction(self):
        distance1 = self.get_dist()
        time.sleep(0.1)
        distance2 = self.get_dist()
        print(distance2)
        direction = distance1 - distance2
        diff = self.target_distance - distance2
        if direction > -0.1 and direction < 0.1:
            correction = 0
        elif ((diff > 0) and (direction > 0)) or ((diff < 0) and (direction < 0)):
            correction = 0.5 * direction / 10
        elif (diff < 0):
            correction = 0.2 * diff / 100
        else:
            correction = 0.5 * diff / 10
        return correction

    def stop(self):
        self.running = False
        return "stopping"

    def get_dist(self):
        distances = []
        for i in range(0,3):
            distances.append(self.distance_sensor.get_distance())
            time.sleep(0.01)
        mean = sum(distances)/len(distances)
        return mean

    def get_motors(self):
        return self.motor_controller.get_values()
