"""
Datos del sistema.
By: EssEnemiGz
"""
"""
Pendiente: Agregar porcentaje de batería.
"""

from sys import argv
from subprocess import run

def parseo(arg):
    """
    Pasear el comando directamente.
    arg es el comando que va a ser ejecutado, debe poner un : al final de cada palabra, sin espacios.
    """
    comando = arg.split(":")
    return comando

def command(commands): 
    """
    Ejecutar comandos.
    """
    output = run(parseo(commands), capture_output=True)
    return output.stdout.decode()

class main:
    def welcome(self):
        # Capturar el OS del usuario.
        F = open("/etc/os-release")
        e=[i.strip() for i in F.readlines()]
        OS = e[0][6:].replace('"','')

        # Bienvenida al usuario con su OS y su username.
        name = command("whoami")
        
        from random import randint
        rColor = randint(31, 36) # Color random para el nombre de usuario
        rColor = f"\033[1;{rColor}m"      
        print(command(f'cowsay:-f:tux:"Welcome back to {OS}, {rColor}{name}\033[0m"'))
    
    def IP(self):
        import socket

        socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Socket a usar.
        socket.connect( ("8.8.8.8", 88) ) # El socket se conecta al DNS de google por el puerto 88.
        print(f"\033[1;34m Private IP -> {socket.getsockname()[0]} \033[0m") # Muestra la IP pública.

objeto = main()

if len(argv) == 1:
    objeto.welcome()
    objeto.IP()

elif argv[1] in ["-p", "--public"] : 
    from requests import get

    ip = get("http://ipecho.me").content.decode('utf-8').strip()
    print(f"\033[1;31m Public IP -> {ip}\033[0m")

