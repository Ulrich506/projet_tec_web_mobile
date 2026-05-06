import socket
import threading

def ecouter_port(port):
    # Création du socket UDP
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('0.0.0.0', port))
    print(f"[*] PC-RECEPTEUR actif sur le port {port}")

    while True:
        data, addr = s.recvfrom(1024)
        message = data.decode('utf-8')
        print(f"\n[MESSAGE REÇU de {addr} sur port {port}]")
        print(f"Contenu : {message}")
        
        # --- OPTIONNEL : RÉPONSE AUTOMATIQUE ---
        # Si tu veux que le PC réponde au téléphone dès qu'il reçoit un message :
        # s.sendto("Message recu par le PC !".encode('utf-8'), addr)
        
        print("-" * 30)

def menu_envoi():
    """Fonction pour permettre au PC d'envoyer un message manuellement"""
    s_envoi = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        target_ip = input("\n[ENVOI] Entrez l'IP du téléphone : ")
        target_port = 5001 # Port par défaut
        msg = input("[ENVOI] Votre message : ")
        
        if msg and target_ip:
            try:
                s_envoi.sendto(msg.encode('utf-8'), (target_ip, target_port))
                print(f"[OK] Message envoyé à {target_ip}")
            except Exception as e:
                print(f"[ERREUR] Impossible d'envoyer : {e}")

if __name__ == "__main__":
    print("--- DEMARRAGE DU TERMINAL BI-DIRECTIONNEL TEC WEB MOBIL ---")
    
    # Écoute sur les ports 5001 et 5002 (pour la réception)
    threading.Thread(target=ecouter_port, args=(5001,), daemon=True).start()
    threading.Thread(target=ecouter_port, args=(5002,), daemon=True).start()
    
    # Lancement du menu d'envoi pour que le PC puisse aussi écrire
    menu_envoi()