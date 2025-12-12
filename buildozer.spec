[app]

# (str) Title of your application
title = Osu Rate Changer Mobile

# (str) Package name
package.name = osuratechanger

# (str) Package domain
package.domain = org.osurate

# (str) Source code folder
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas,mp3,ogg,osu

# (list) Directories to exclude
source.exclude_dirs = tests, bin, venv, __pycache__

# (str) Application version
version = 1.0

# (list) Application requirements
# Kivy (interfaz), Pydub (audio), ffpyplayer (para reproducir/convertir audio en Android)
requirements = python3,kivy,pydub,ffpyplayer

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Supported orientations
orientation = portrait

# (list) Permissions — necesarios para leer/escribir archivos .osu y .mp3 en Android
android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,INTERNET

# (str) Android entrypoint (archivo principal)
source.main = main.py

# (int) Target Android API — versión recomendada actual (2025)
android.api = 35

# (int) Minimum API your APK supports
android.minapi = 21

# (str) Android SDK version
android.sdk = 35

# (str) Android NDK PATH
android.ndk_path = /home/teran/.buildozer/android/platform/android-ndk

# (str) Android NDK version
android.ndk = 25b

# (bool) Usa almacenamiento público (necesario para acceder a archivos externos)
android.private_storage = False

# (bool) Activa compatibilidad OpenGL antigua (evita bugs en algunos dispositivos)
android.enable_legacy_gl = True

# (list) Arquitecturas Android
android.archs = arm64-v8a, armeabi-v7a

# (bool) Permitir backup automático (útil si luego haces versión de producción)
android.allow_backup = True

# (str) Tipo de salida en debug
android.debug_artifact = apk

# (str) Tipo de salida en release
#android.release_artifact = aab

# (bool) Mantener pantalla encendida mientras se ejecuta la app
android.wakelock = True

# (str) Python-for-Android branch (mantén estable)
p4a.branch = master

# (str) Bootstrap recomendado para apps Kivy
p4a.bootstrap = sdl2


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
