from server import Server
from robot_controller import RobotController
from distance_sensor import Sonar
from motor_controller import MotorController

def main():
    motor_controller = MotorController()
    sonar = Sonar(18, 17)
    controller = RobotController(sonar, motor_controller)
    server = Server(controller, "192.168.99.11", 8080)
    server.listen()

if __name__=="__main__":
    main()
