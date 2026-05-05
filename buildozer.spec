[app]
title = Secure Node
package.name = securenode
package.domain = org.eni
source.dir = .
version = 0.1
source.include_exts = py,png,jpg,kv,atlas,ttf

# Dépendances
requirements = python3, kivy==2.3.0, kivymd==1.2.0, openssl, requests, urllib3

orientation = portrait
android.permissions = INTERNET, ACCESS_NETWORK_STATE, WAKE_LOCK

# --- LA CORRECTION EST ICI ---
# fullscreen = 0 permet à Android de garder les barres système 
# et aide Kivy à calculer la vraie taille de l'affichage.
fullscreen = 0

# Configuration Android
android.accept_sdk_license = True
android.api = 34
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.archs = arm64-v8a, armeabi-v7a

# --- RÉGLAGE CLAVIER ---
# 'resize' est le plus stable pour les interfaces de messagerie.
android.window_softinput_mode = resize

[buildozer]
log_level = 2
warn_on_root = 1