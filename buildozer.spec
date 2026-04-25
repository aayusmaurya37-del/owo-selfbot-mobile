[app]
title = OwO Selfbot
package.name = owoselfbot
package.domain = org.owobot

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 1.0

# Minimal requirements that WILL compile
requirements = python3,kivy==2.1.0,requests

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,ACCESS_NETWORK_STATE,WAKE_LOCK

# Use older, more stable versions
android.api = 31
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a

# Use older p4a that works better
p4a.branch = master
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
