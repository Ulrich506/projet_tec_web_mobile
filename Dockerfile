# 1. Utiliser une image Python légère (idéale pour l'IoT)
FROM python:3.9-slim

# 2. Définir le dossier de travail dans le conteneur
WORKDIR /app

# 3. Copier le fichier des bibliothèques dans le conteneur
COPY requirements.txt .

# 4. LA COMMANDE : Installer les bibliothèques
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copier ton code Python (ton script de nœud) dans le conteneur
COPY node_script.py .

# 6. Lancer le script au démarrage du conteneur
CMD ["python", "node_script.py"]