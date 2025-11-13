[app]
title = TonS
package.name = tons
package.domain = org.tons

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 1.0.0

requirements = python3,kivy,requests

orientation = portrait
fullscreen = 0
android.permissions = INTERNET,ACCESS_NETWORK_STATE,CHANGE_NETWORK_STATE,BIND_VPN_SERVICE
android.api = 31
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
