"""
Datos del sistema.
By: EssEnemiGz
Forked by: lae-laps
"""

import json
import time
from sys import argv
from requests import get
from subprocess import run
from random import randint


# log file
# Editar y poner unos valores razonables, como ~/.config/system-data o ~/.cache/system-data
log_file = "system-data.logs"
config_file = "config.json"

def log_error(error):
    with open(log_file, "a") as lf:
        lf.write(f"{error} \n")

# No está implementado, pero queda la función hecha para recojer datos de la configuración en formato json en el futuro
def get_config() -> dict:
    with open(config_file, "r") as cf:
        data = json.load(cf)
    return data

def command(commands): 
    output = run(commands.split(":"), capture_output=True)
    return output.stdout.decode()

class Interface:
    def welcome(self):
        try:
            file = open("/etc/os-release")
            e = [i.strip() for i in file.readlines()]
            os = e[0][6:].replace('"','')
        except Exception as e:
            os = "undetermined-os"
            log_error(f"[-] Error trying to get OS release line 23-26 -> {e}")

        try:
            name = command("whoami")
        except Exception as e:
            name = "username"
            log_error(f"[-] Error trying to read username - line 31 -> {e}")

        rColor = randint(31, 36) 
        rColor = f"\033[1;{rColor}m"      
        print(command(f'cowsay:-f:tux:"Welcome back to {os}, {rColor}{name}\033[0m"'))

    def show_local_ip(self):
        try:
            local_ip = localIp()
            local_ip.get()
            local_ip.print_formated()
        except Exception as e:
            log_error(f"[-] Error - could not retrieve local IP address - line 46-48 -> {e}")

    def show_battery_status(self):
        try:
            battery = Battery()
            capacity = battery.get_capacity()
            color = battery.get_color()
        except Exception as e:
            log_error(f"[-] Error trying to get battery capacity - line 51-53 -> {e}")
   
    def show_time(self):
        try:
            time = Time()
            time.print_formated()
        except Exception as e:
            log_error(f"[-] Error in printing time - line 58-59 -> {e}")
        
class localIp:
    def __init__(self):
        self.value = "127.0.0.1"

    def get(self):
        try:
            import socket
            socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
            socket.connect( ("8.8.8.8", 88) ) 
            self.value = socket.getsockname()
        except OSError as e:
            self.value = "invalid"
            log_error(f"[-] Error trying to get local ip address - lines 46-48 -> {e}")

    def print_formated(self):
        if self.value == "invalid":
            print("\033[1;31m Error:\033[0m La conexión está deshabilitada.")
        else:
            print(f"\033[1;34m Private IP -> {self.value[0]} \033[0m")

class publicIp:
    def __init__(self):
        self.value = ""
    
    def get(self):
        try:
            self.value = get("80.58.61.250").content.decode('utf-8').strip()
        except Exception as e:
            log_error(f"[-] Error - could not get public IP via no DNS method - line 83 -> {e}")
            try:
                self.value = get("http://ipecho.me").content.decode('utf-8').strip()
            except Exception as e:
                log_error(f"[-] Error - could not get public IP via DNS method - line 86 -> {e}")

    def print_formated(self):
        print(f"\033[1;31m Public IP -> {self.value}\033[0m")

class Battery:
    def __init__(self):
        self.capacity = 0

    def get_color(capacity):
        if int(capacity) >= 35 and int(capacity) < 65:
            return "\033[1;33m"
        elif int(capacity) >= 65:
            return "\033[1;32m"
        elif int(capacity) < 35:
            return "\033[1;31m"
    
    def get_capacity(argv):
        if argv == "Unknown" or argv == "Charging":
            return f"\033[1;32m Status -> Charging"
        elif argv == "Discharging":
            return f"\033[1;31m Status -> {argv}"

    try:
        ruta = command("find:/sys/class/power_supply").split()
        nuevaRuta = open(f"{ruta[1]}/status").read().strip()
    
        if nuevaRuta == "Discharging":
            print(f"\033[1;31m Status -> {nuevaRuta} \033[0m")
        else:
            print(f"\033[1;32m Status -> {nuevaRuta} \033[0m")

    except Exception as e:
        log_error(f"[-] Error trying to get battery percentage - line 85-86 -> {e}")

class Time:
    def __init__(self):
        self.now = time.strftime('%X')
    
    def print_formated(self):
        print(f"    \033[1;35m Hour: \033[0m \033[1;33m {self.now} \033[0m")


# Main

if __name__ == "__main__":

    if len(argv) == 1:
        interface = Interface()

        interface.welcome()
        interface.show_time()
        interface.show_local_ip()
        interface.show_battery_status()
        exit(0)

    elif argv[1] in ["-p", "--public"] : 

        public_ip = publicIp()
        public_ip.get()
        public_ip.print_formated()
        exit(0)
