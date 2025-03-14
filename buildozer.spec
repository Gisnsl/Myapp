[app]

# (str) Title of your application
title = SRAFYE

# (str) Package name
package.name = SARF

# (str) Package domain (needed for android/ios packaging)
package.domain = com.srafye.byahmed

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (leave empty to include all files)
source.include_exts = py,png,jpg,kv,atlas,ttf,otf,xml,json,css,html,webp

# (str) Application versioning
version = 0.1

# (list) Application requirements
requirements = python3,kivy,flask,requests,android.runnable,jnius,threading,json

# (list) Supported orientations
orientation = portrait

# (bool) Fullscreen mode
fullscreen = 1

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API
android.api = 34

# (int) Minimum Android API supported (Android 4.1)
android.minapi = 16

# (list) The Android architectures to build for
android.archs = armeabi-v7a, arm64-v8a, x86, x86_64


# (bool) Enable AndroidX support
android.enable_androidx = True

# (bool) Allow Android auto backup
android.allow_backup = True

# (str) The format used to package the app (apk or aab)
android.release_artifact = apk
android.debug_artifact = apk
