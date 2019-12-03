# WallFollower
Project from a class in Embedded Linux on University of Southern Denmark, using CamJam Edukit3

## How it works

The wall following robot works by running the [main](main.py) file which instantiates following classes: 
- A [MotorController](motor_controller.py) object used to steer the robot extending the CamJamKitRobot library by validating the given input. 
- A [Sonar](distance_sensor.py) object is instantiated with pins 17 and 18 used to get the distance to an object in its range. The Sonar class uses the [pigpio](http://abyz.me.uk/rpi/pigpio/python.html) library to communicate with the [pigpio daemon](http://abyz.me.uk/rpi/pigpio/pigpiod.html). 
- A [RobotController](robot_controller.py) object is then instantiated with that sonar and MotorController object, providing the start, stop, get_dist and get_motors functions.
- Lastly a [Server](server.py) object is instantiated,  running a TCP server on its local ip address: 192.168.99.11 with port 8080. The server listens for incoming commands in the form of start, stop, getdist or getmotors, which is then dispatched to the RobotController object, that responds accordingly.

The RobotController is running in its own thread, in order to not block the server thread, listening for commands. The robot works in two states, first one being stationary, rotating to the left, trying to find the wall, and become parallel to it. Second state makes the robot move forward trying to find the best correction to its movement, and adjust the motorspeed. The correction is based on two parameters, direction and deviation. Direction is calculated based on a distance measurement that is subtracted from a previous distance measurement taken with a 100 ms interval. The direction will tell whether it is approaching the wall or moving away, depending on if it is positive or negative. Deviation is calculated based on some initial manual target distance (the distance desired to be apart from the wall) minus the latest actual distance reading, telling the robot if it is too close, or too far away from the wall.    

## Scripts and systemd services
We have automated the startup process of the Pi with the following scripts and systemd services:
- The Pi connects automatically to an ad-hoc network called "pibot", using [connect-pibot.sh](scripts/connect-pibot.sh), which is executed at startup by [connect-pibot.service](scripts/connect-pibot.service).
- The pigpio daemon is started automatically by a systemd service provided by the pigpio author.
- The robot software is started by [wall-follower.service](scripts/wall-follower.service)

## To connect to server
When the robot has been turned on, you can connect to it by following these steps:
1. Possibly stop the network manager, which can be done with: sudo service network-manager stop
2. Connect to the pibot network. This can be done with an adapted version (changing the static ip address to something else) of [connect-pibot.sh](scripts/connect-pibot.sh).
3. You can now control the robot by sending commands over TCP, either getdist, getmotors, start or stop. You can either:
    1. Use socat: echo start | socat 192.168.99.11:8080 -
    2. or use [commander.sh](scripts/commander.sh) to easily start and stop the robot.  
