[app]
title = Secure Node
package.name = securenode
package.domain = org.eni
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Cette ligne est la clé pour ton maillage sécurisé
requirements = python3,kivy==2.3.0,cryptography,openssl,pyffi,setuptools

# Permissions indispensables pour tes nœuds
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# Paramètres de build stables
android.api = 33
android.minapi = 21
android.ndk = 25c
android.archs = armeabi-v7a, arm64-v8a

[buildozer]
log_level = 2
#warn_on_root = 1