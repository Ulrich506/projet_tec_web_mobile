[app]

# (section) Informations de base
title = Secure Node
package.name = securenode
package.domain = org.eni

# (section) Fichiers source
# Assure-toi que ton fichier principal s'appelle bien main.py localement
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# (section) Configuration Python & Dépendances
# CRUCIAL : Ajoute pycryptodome ou cryptography + les recettes système
# On ajoute 'requests' et 'urllib3' si ton nœud communique via API, 
# sinon reste sur cryptography,openssl,pyffi
requirements = python3,kivy==2.3.0,cryptography,openssl,pyffi,setuptools

# (section) Android spécifique
# Indispensable pour le maillage et l'envoi de paquets UDP/TCP
android.permissions = INTERNET, ACCESS_NETWORK_STATE, CHANGE_NETWORK_STATE

# Cible les versions récentes d'Android demandées par GitHub
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25c

# (section) Interface
orientation = portrait
android.window_softinput_mode = resize

# (section) Buildozer et Python-for-Android
# Force l'utilisation d'une version stable pour éviter les erreurs Node.js/Build
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1