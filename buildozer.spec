[app]
title = OwO Selfbot
package.name = owoselfbot
package.domain = org.owobot

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 1.0.0

# PINNED VERSIONS TO FIX COMPILER CRASH
requirements = python3,kivy==2.2.0,discord.py-self==1.9.2,aiohttp==3.8.5,certifi,yarl,multidict,idna,charset-normalizer

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,ACCESS_NETWORK_STATE,WAKE_LOCK
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True

# BUILD 64-BIT ONLY TO PREVENT GITHUB ACTIONS OUT-OF-MEMORY CRASH
android.archs = arm64-v8a

p4a.branch = develop
p4a.bootstrap = sdl2

[buildozer]
log_level = 2
warn_on_root = 1
