import socket
import sys

class Server:
    def __init__(self, robot_controller, host, port):
        self.robot_controller = robot_controller
        self.host = host
        self.port = port

    def listen(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        server_address = (host, port)
        print('starting up on {} port {}'.format(*server_address))
        sock.bind(server_address)

        sock.listen(1)

        while True:
            print('waiting for a connection')
            connection, client_address = sock.accept()
            try:
                while True:
                    command = connection.recv(4096)
                    if data:
                        print("Recevied command: {}".format(command))
                        result = self._dispatch(command)
                        if result:
                            connection.sendall(result)
            finally:
                connection.close()

    def _dispatch(self, command):
        if command == "start":
            robot_controller.start()
            return "starting"
        elif command == "stop":
            robot_controller.stop()
            return "stopping"
        elif command == "getdist":
            return robot_controller.get_dist()
        elif command == "getmotors":
            return robot_controller.get_motors()
        else:
            return "unknown command"
