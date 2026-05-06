import socket
import threading

def ecouter_port(port):
    # Création du socket UDP (plus simple pour le Mesh)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('0.0.0.0', port))
    print(f"[NOM DU NOEUD] PC-RECEPTEUR actif sur le port {port}")

    while True:
        data, addr = s.recvfrom(1024)
        message = data.decode('utf-8')
        print(f"\\n[MESSAGE REÇU de {addr}]")
        print(f"Contenu : {message}")
        print("-" * 30)

# Lancement des deux ports en même temps grâce au threading
if __name__ == "__main__":
    print("--- DEMARRAGE DU TERMINAL DE RECEPTION TEC WEB MOBIL ---")
    threading.Thread(target=ecouter_port, args=(5001,)).start()
    threading.Thread(target=ecouter_port, args=(5002,)).start()