import socket
import sys

class Server:
    def __init__(self, robot_controller, host, port):
        self.robot_controller = robot_controller
        self.host = host
        self.port = port

    def listen(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_address = (self.host, self.port)
        sock.bind(server_address)

        sock.listen(1)

        print("Listening on port {}".format(self.port))

        try:
            while True:
                connection, client_address = sock.accept()
                try:
                    command = connection.recv(4096)
                    if command:
                        command = self._strip_command(command)
                        print("Received command: {}".format(command))
                        result = str(self._dispatch(command))
                        if result:
                            connection.sendall(result.encode("utf-8"))
                finally:
                    connection.close()
        except KeyboardInterrupt:
            sock.shutdown(socket.SHUT_RDWR)
            sock.close()

    def _strip_command(self, command):
        command = command.decode("utf-8")
        command = command.rstrip()
        return command

    def _dispatch(self, command):
        if command == "start":
            self.robot_controller.start()
            return "starting"
        elif command == "stop":
            self.robot_controller.stop()
            return "stopping"
        elif command == "getdist":
            return self.robot_controller.get_dist()
        elif command == "getmotors":
            return self.robot_controller.get_motors()
        else:
            return "unknown command"
