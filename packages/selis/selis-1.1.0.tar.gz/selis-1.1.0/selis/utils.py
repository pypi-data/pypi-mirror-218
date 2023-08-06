import datetime
import webbrowser
import os


def get_nickname(content):
    nickname = ""
    content = content.split(" ")
    for i in range(len(content)):
        if i > 0:
            nickname = nickname + content[i] + " "

    return nickname.strip()


def get_current_date():
    return datetime.date.today()


def get_current_time():
    now = datetime.datetime.now()
    return now.strftime("%p %H:%M:%S")


def convert_to_string(list_type):
    string = ""
    for i in list_type:
        string = string + i + " "
        
    return string.strip()


def print_connection_computer_info(machine, node, platform, processor, release, system, version):
    print(f"\033[93m |_[+] Current user: {node}")  
    print(f"\033[93m |_[+] Platform: {platform}")  
    print(f"\033[93m |_[+] OS info: (system='{system}', CPU: '{processor}', release='{release}', version='{version}', machine='{machine}')")


def open_url(url):
    webbrowser.open(url)


def clear_screen():
    os.system("clear")


def guide_to_exit():
    print("\033[0m[+] Press 'Enter' to exit")


def convert_color(string, style):
    colors = {
    "WARNING": '\033[93m',
    "FAIL": '\033[91m',
    "ENDC": '\033[0m',
    "BOLD": '\033[1m',
    }

    return colors[style] + string
