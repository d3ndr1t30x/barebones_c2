import socket

def listener_handler():
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host_ip = '127.0.0.1'
    host_port = 2222

    try:
        # Bind the socket to the IP address and port
        sock.bind((host_ip, host_port))
        print('[+] Awaiting connection from client...')

        # Listen for incoming connections
        sock.listen(1) # listen(1) specifies that only one connection is accepted at a time

        # Accept a connection
        remote_target, remote_ip = sock.accept()
        print(f'[+] Connection received from {remote_ip[0]}')

        while True:
            try:
                # Get input from the user to send to the client
                message = input('Message to send #> ')

                if message == 'exit':
                    remote_target.send(message.encode())
                    print ('[+] Closing connection')
                    remote_target.close()
                    break

                # Send message to the client
                remote_target.send(message.encode())

                # Receive the response from the client
                response = remote_target.recv(1024).decode()

                if response == 'exit':
                    print('[-] The client has terminated the session')
                    remote_target.close()
                    break

                print(response)
            except  KeyboardInterrupt:
                print('[+] Keyboard interrupt issued')
                remote_target.close()
                break

            except Exception as e:
                print(f'[!] Exception occured: {e}')
                remote_target.close()
                break

    except Exception as e:
        print(f'[!] Exception occured: {e}')
        remote_target.close()
        
    finally:
        sock.close()

if __name__ == '__main__':
    listener_handler


