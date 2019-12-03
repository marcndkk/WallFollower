# WallFollower
Project from a class in Embedded Linux on University of Southern Denmark, using CamJam Edukit3

## How it works

The wall following robot works by running the [main](main.py) file which instantiates following classes: 
- A [MotorController](motor_controller.py) object used to steer the robot extending the CamJamKitRobot library by validating the given input. 
- A [Sonar](distance_sensor.py) object is instantiated with pins 17 and 18 used to get the distance to an object in its range. 
- A [RobotController](robot_controller.py) object is then instantiated with that sonar and MotorController object, providing the start, stop, get_dist and get_motors functions.
- Lastly a [Server](server.py) object is instantiated running on its local ip address: 192.168.99.11 with port 8080. The server listens for incoming commands in the form of start, stop, getdist or getmotors, which is then dispatched to the RobotController object, that responds accordingly.

The RobotController is running in its own thread, in order to not block the server thread, listening for commands. The robot works in two states, first one being stationary, rotating to the left, trying to find the wall, and become parallel to it. Second state makes the robot move forward trying to find the best correction to its movement, and adjust the motorspeed. The correction is based on two parameters, direction and deviation. Direction is calculated based on a distance measurement that is subtracted from a previous distance measurement taken with a 100 ms interval. The direction will tell whether it is approaching the wall or moving away, depending on if it is positive or negative. Deviation is calculated based on some initial manual target distance (the distance desired to be apart from the wall) minus the latest actual distance reading, telling the robot if it is too close, or too far away from the wall.    

## To connect to server
1. Run command: ... network_manager stop
2. execute bashscript [pibot.sh](pibot.sh)
3. echo start | socat tcp:192.168.99.11
