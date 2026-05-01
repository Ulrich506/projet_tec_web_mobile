[app]
title = Secure Node
package.name = securenode
package.domain = org.eni

# Les fichiers à inclure
source.include_exts = py,png,jpg,kv,atlas

# TRÈS IMPORTANT : Ajoute cryptography ici
requirements = python3,kivy,cryptography,openssl

# Permissions pour le réseau et le maillage
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (Optionnel) Pour que le clavier ne cache pas l'interface
android.window_softinput_mode = resize