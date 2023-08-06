import socket
import threading
import sys
import getpass

from selis.computerinfo import ComputerInfo
from selis.command import commands
from selis.utils import *


class ChatClient:
    def __init__(self, ip, port, nickname):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.connection.connect((ip, port))
        except:
            print(f"\033[91m[-] Sever not found\033[0m")
            sys.exit()

        self.nickname = nickname
        self.send_client_info_to_server()
        self.is_running = True


    def send_client_info_to_server(self):
        client_computer = ComputerInfo()
        info = client_computer.get()
        msg = self.nickname + "/" + info

        self.send_message(msg)


    def process_admin_mode(self):
        password = getpass.getpass("\033[1m[*] Admin's Password: \n>> \033[0m")
        msg = "check-admin/" + self.nickname + "/" + password
        self.send_message(msg)


    def send_message(self, message):
        self.connection.send(message.encode())


    def receive_message(self):
        return self.connection.recv(1024).decode()


    def exit(self):
        self.is_running = False
        guide_to_exit()
        self.connection.close()


    def process_receiving_message(self):
        try:
            while True:
                response = self.receive_message()

                if response:
                    my_message = f">>> {self.nickname}:"

                    if my_message in response:
                        continue


                    if "admin/open-url" in response:
                        url = response.split(" ")[1]
                        open_url(url)

                    elif response == "system/exist_nickname":
                        print("\033[91m[!] This nickname already exists\033[0m")
                        self.exit()
                        break

                    elif response == "admin/close":
                        print("\033[91m[-] Server is not available\033[0m")
                        self.exit()
                        break

                    elif response == "admin/ban&kick":
                        print("\033[91m[-] Server is not available\033[0m")
                        self.exit()
                        break

                    elif response == "admin/close-server":
                        print("\033[91m[-] Admin closes the server\033[0m")
                        try:
                            self.exit()
                            break
                        except:
                            sys.exit()

                    else:
                        print(response)

        except:
            print("\033[91m[-] Connection is closed\033[0m")
            self.connection.close()
            sys.exit(0)


    def process_sending_message(self):
        try:
            while True:
                content = input().strip()

                if content == "" and self.is_running == True:
                    print("\033[91m[-] Typing something before sending\033[0m")
                    continue

                elif content == "/exit":
                    self.send_message(f"client/exit {self.nickname}")
                    self.connection.close()
                    break

                elif content == "/clear":
                    clear_screen()

                elif content == "/admin":
                    self.process_admin_mode()

                elif content.split()[0] in commands:
                    self.send_message(content)

                else:
                    print(f"\033[0m>>> (You): {content}")

                    content = f"\033[0m>>> {self.nickname}: {content}"
                    self.send_message(content)

        except:
            sys.exit()


    def start(self):
        recieve_threading = threading.Thread(target=self.process_receiving_message)
        recieve_threading.start()
        
        send_threading = threading.Thread(target=self.process_sending_message)
        send_threading.start()

        recieve_threading.join()
        send_threading.join()
