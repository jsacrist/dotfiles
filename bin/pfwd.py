#!/usr/bin/env python3
# This is a simple port-forward / proxy, written using only the default python
# based on: http://voorloopnul.com/blog/a-python-proxy-in-less-than-100-lines-of-code/
# Modified by j.sacris@gmail.com

import socket
import select
import time
import sys
import logging
import argparse

logging.basicConfig(format="[%(asctime)-8s][%(levelname)s]:\t%(message)s",
                    level=logging.DEBUG)

# Changing the buffer_size and delay, you can improve the speed and bandwidth.
# But when buffer get to high or delay go too down, you can break things
buffer_size = 4*1024
#refresh_delay = 1e-4
refresh_delay = 1e-5

class Forwarder:
    def __init__(self):
        self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        try:
            self.forward.connect((host, port))
            return self.forward
        except Exception as my_exception:
            logging.error("Forwarder error: %s" % str(my_exception),
                          exc_info=True)
            return False

class Forward_server:
    input_list = []
    channel = {}

    def __init__(self, from_port, to_host, to_port):
        self.from_port = int(from_port)
        self.to_host = to_host
        self.to_port = int(to_port)

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind(('', self.from_port))
        self.server.listen(200)
        logging.info("Forwarding    [*:*] ---> [%s:%d] ---> [%s:%d]" %
                     (socket.gethostname(), self.from_port,
                     self.to_host, self.to_port))

    def forward_loop(self):
        """
        """
        self.input_list.append(self.server)
        while (True):
            time.sleep(refresh_delay)
            ready_to_read, ready_to_write, in_error = \
                    select.select(self.input_list, [], [])

            for self.s in ready_to_read:
                if (self.s == self.server):
                    self.on_accept()
                    break
                try:
                    self.data = self.s.recv(buffer_size)
                    client_address = self.s.getpeername()
                    client_ip = client_address[0]
                    client_port = int(client_address[1])
                    if (len(self.data) == 0):
                        #client_address = self.s.getpeername()
                        #client_ip = client_address[0]
                        #client_port = int(client_address[1])
                        logging.info("Disconnect    [%s:%d] has disconnected" %
                                     (client_ip, client_port))
                        self.on_close()
                        break
                except Exception as my_except:
                    logging.info("Disconnect    Unexpected disconnection: %s" %
                                 my_except )
                    #logging.warning(self.s)
                    self.on_close()
                    ready_to_read.remove(self.s)
                    break

                if (len(self.data) != 0):
                    self.on_recv()


    def on_accept(self):
        forward = Forwarder().start(self.to_host, self.to_port)
        client_socket, client_address = self.server.accept()
        if (forward):
            client_ip = client_address[0]
            client_port = int(client_address[1])
            logging.info("Connection    [%s:%d] ---> [%s:%d] ---> [%s:%d]" % \
                         (client_ip, client_port,
                         socket.gethostname(), self.from_port,
                         self.to_host, self.to_port))
            self.input_list.append(client_socket)
            self.input_list.append(forward)
            self.channel[client_socket] = forward
            self.channel[forward] = client_socket
        else:
            logging.warning("Can't establish connection.")
            logging.info("Closing connection with client side: %s" % \
                    str(client_address))
            client_socket.close()

    def on_close(self):
        #remove objects from input_list
        self.input_list.remove(self.s)
        self.input_list.remove(self.channel[self.s])
        out = self.channel[self.s]

        # close the connection with client
        self.channel[out].close()  # equivalent to do self.s.close()

        # close the connection with remote server
        self.channel[self.s].close()

        # delete both objects from channel dictionary
        del self.channel[out]
        del self.channel[self.s]

    def on_recv(self):
        data = self.data
        # Logging the data could be done here
        self.channel[self.s].send(data)

#if __name__ == '__main__':
def main(arguments):
    parser = argparse.ArgumentParser(formatter_class = \
                                     argparse.RawDescriptionHelpFormatter)
    
    ## Parsing Options            
    parser.add_argument("-f", "--from-port",
                        type=str,
                        help="The port from which the forwarding takes place.")
    
    parser.add_argument("-a", "--to-address",
                        type=str,
                        default="localhost",
                        help="The address to which the forwarding takes place.")

    parser.add_argument("-t", "--to-port",
                        type=str,
                        help="The port to which the forwarding takes place.")
    
    args = parser.parse_args(arguments)

    if (args.from_port == None or args.to_port == None):
        logging.error("Must provide --from-port and --to-port")
        parser.print_help()
        exit(-1)

    server = Forward_server(args.from_port, args.to_address, args.to_port)
    try:
        server.forward_loop()
    except KeyboardInterrupt:
        logging.info("Ctrl C - Stopping server")
        sys.exit(1)
    except Exception as my_exception:
        logging.error("main() error: %s" % my_exception, exc_info=True)
        sys.exit(2)

################################################################################


if __name__ == "__main__":    
    main(sys.argv[1:])
