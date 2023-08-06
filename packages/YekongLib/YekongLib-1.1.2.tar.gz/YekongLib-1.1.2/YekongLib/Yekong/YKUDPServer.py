import socket
import asyncio

# Define a class for the UDP server
class YKUDPServer:
    # Define a constructor that takes a data handler function, a port number and an optional address
    def __init__(self, data_handler, port, address="0.0.0.0"):
        # Check the input parameters for null values
        if data_handler is None:
            raise ValueError("data_handler cannot be null")
        if port is None or port < 0 or port > 65535:
            raise ValueError("port must be a valid integer between 0 and 65535")

        # Initialize a socket with the given port and address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((address, port))

        # Initialize the data handler with the given function
        self.data_handler = data_handler

    # Define a method to start listening for incoming data
    async def start(self):
        # Loop indefinitely
        while True:
            try:
                # Receive a datagram from any remote endpoint and get the data and the remote endpoint
                data, remote_endpoint = await self.loop.sock_recvfrom(self.sock, 1024)

                # Call the user-defined data handler function with the data and the remote endpoint
                self.data_handler(data, remote_endpoint, self.sock)
            except Exception as ex:
                # Handle any exceptions
                print(ex)

    # Define a method to stop listening and close the socket
    def stop(self):
        # Close the socket
        self.sock.close()

# Define a function to document the format of the data handler function
def data_handler_format():
    """
    The data handler function is a user-defined function that takes three parameters:

    - data: a bytes object that contains the received datagram
    - remote_endpoint: a tuple of (address, port) that represents the sender of the datagram
    - sock: a socket object that can be used to send back a response

    The data handler function can perform any desired operations on the received data,
    such as parsing, processing, logging, etc. It can also use the sock object to send back
    a response to the remote endpoint if needed.

    The data handler function does not need to return anything.
    """
