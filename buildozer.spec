[app]
# (Obligatoire) Titre de ton application
title = Secure Node

# (Obligatoire) Nom du package
package.name = securenode

# (Obligatoire) Domaine du package (L'ENI est bien spécifiée ici)
package.domain = org.eni

# (Obligatoire) Où se trouve le code source
source.dir = .

# (Obligatoire) Version de l'application
version = 0.1

# Fichiers à inclure : AJOUT de .ttf pour les polices de caractères
source.include_exts = py,png,jpg,kv,atlas,ttf

# --- DÉPENDANCES CRITIQUES ---
# AJOUT de 'requests' (si tu envoies des mails via API) 
# et 'hostpython3' pour la compilation
requirements = python3, kivy==2.3.0, kivymd==1.2.0, openssl, requests, urllib3

# Orientation et permissions
orientation = portrait
# AJOUT de READ_EXTERNAL_STORAGE si tu veux sauvegarder des logs
android.permissions = INTERNET, ACCESS_NETWORK_STATE, WAKE_LOCK

# --- Configuration Android ---
android.accept_sdk_license = True
android.api = 34
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

# Architecture : AJOUT de armeabi-v7a pour une compatibilité maximale (vieux téléphones)
android.archs = arm64-v8a, armeabi-v7a

# --- SERVICE & ICON ---
# Icône de l'app (pense à mettre un fichier icon.png dans ton dossier)
# icon.filename = %(source.dir)s/icon.png

# Réglage pour le clavier Android (Indispensable pour ton chat)
android.window_softinput_mode = resize

[buildozer]
log_level = 2
warn_on_root = 1