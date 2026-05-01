import socket
import threading
from cryptography.fernet import Fernet

# CONFIGURATION
KEY = b'PtiW1Y8fYyJrPg8M3fqIMeYZVzp_U-u691LGKDRjCLE='
cipher = Fernet(KEY)
MY_PORT = 5001
last_mobile_addr = None

def start_node():
    global last_mobile_addr
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 0.0.0.0 est crucial pour écouter le téléphone via le WiFi
    sock.bind(('0.0.0.0', MY_PORT))
    
    print(f"--- NOEUD PC PRÊT (Port {MY_PORT}) ---")

    def receive():
        global last_mobile_addr
        while True:
            try:
                data, addr = sock.recvfrom(1024)
                msg = cipher.decrypt(data).decode()
                # On mémorise l'IP du mobile pour pouvoir répondre
                if addr[0] != '127.0.0.1':
                    last_mobile_addr = addr
                print(f"\n[REÇU] {msg}")
                print("Message à envoyer > ", end="")
            except: pass

    threading.Thread(target=receive, daemon=True).start()

    while True:
        msg = input("Message à envoyer > ")
        if last_mobile_addr:
            token = cipher.encrypt(msg.encode())
            sock.sendto(token, (last_mobile_addr[0], 5005)) # Port 5005 pour l'APK
            print(f"-> Envoyé au mobile ({last_mobile_addr[0]})")
        else:
            print("! En attente d'un premier message du mobile...")

if __name__ == "__main__":
    start_node()