[app]

# (str) Title of your application
title = The Farmer Was Replaced

# (str) Package name
package.name = farmerdrone

# (str) Package domain (needed for android/ios packaging)
package.domain = org.farmerdrone

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf,json,xml

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.jpg

# (str) Application versioning (method 1)
version = 1.0.0

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
# Using python-for-android (p4a) recipe names - these will be built from source for Android
# Don't pin versions - use p4a default recipe versions
requirements = python3,kivy,pyjnius,android,openssl,certifi,charset_normalizer

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (str) Presplash of the application
# presplash.filename = %(source.dir)s/assets/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/assets/icon.png

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = landscape

# (list) List of service to declare
# services = NAME:ENTRYPOINT_TO_PY,NAME2:ENTRYPOINT2_TO_PY

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (string) Presplash background color (for android toolchain)
# presplash_color = #FFFFFF

# (string) Presplash animation using Lottie format
# presplash_lottie = "path/to/lottie/file.json"

# (str) Android arch to build for, choices: arm64-v8a, armeabi-v7a, x86, x86_64
# In past, was `android.arch` but we now use `android.archs`
android.archs = arm64-v8a, armeabi-v7a

# (int) Android API to use. Should be at least 21 for modern apps
android.api = 31

# (int) Minimum API required. 21 = Android 5.0
android.minapi = 21

# (int) Android SDK version to use
# android.sdk = 20

# (str) Android NDK version to use
# android.ndk = 25b

# (int) Android NDK API to use. This is the minimum API your app will support, it should usually match android.minapi
# android.ndk_api = 21

# (bool) Use --private data storage (True) or dir public (False)
# android.private_storage = True

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
# android.ndk_path =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid long downloads on a slow connection
# android.skip_update = False

# (str) Android entry point, default is ok for Kivy-based app
# android.entrypoint = org.kivy.android.PythonActivity

# (str) Android app theme, default is ok for Kivy-based app
# android.apptheme = "@android:style/Theme.NoTitleBar.Fullscreen"

# (list) Permissions
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible
# android.targetapi = 31

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process. Allows wildcards matching, for example:
# OUYA-ODK/libs/*.jar
# android.add_jars = foo.jar,bar.jar,path/to/more/*.jar

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
# android.add_src =

# (list) Android AAR archives to add
# android.add_aars =

# (list) Put these files or directories in the apk's assets directory
# android.add_assets =

# (list) Gradle dependencies to add
# android.gradle_dependencies =

# (bool) Enable AndroidX support
android.enable_androidx = True

# (str) Kotlin version to use
android.kotlin_version = 1.6.10

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid long downloads on a slow connection
# android.skip_update = False

# (bool) If True, then automatically accept SDK licenses
android.accept_sdk_license = True

# (str) Android entry point, default is ok for Kivy-based app
# android.entrypoint = org.kivy.android.PythonActivity

# (list) List of Java .jar files to add to the libs so that pyjnius can access
# their classes. Don't add jars that you do not need, since extra jars can slow
# down the build process. Allows wildcards matching, for example:
# OUYA-ODK/libs/*.jar
# android.add_jars = foo.jar,bar.jar,path/to/more/*.jar

# (list) List of Java files to add to the android project (can be java or a
# directory containing the files)
# android.add_src =

# (list) Android AAR archives to add
# android.add_aars =

# (list) Put these files or directories in the apk's assets directory
# android.add_assets =

# (list) Gradle dependencies to add
# android.gradle_dependencies =

#
# iOS specific
#

# (str) Path to a custom xcodebuild file to use (if using `build_ios` tool)
# ios.xcodebuild =

# (str) Name of the certificate to use for signing the debug version
# ios.codesign.debug = "iPhone Developer: <lastname> <firstname> (<hexstring>)"

# (str) Name of the certificate to use for signing the release version
# ios.codesign.release = "iPhone Distribution: <lastname> <firstname> (<hexstring>)"

# (str) Path to a provisioning profile to use
# ios.provisioning.profile =

# (str) URL of the app on the app store
# ios.appstore.url =

# (str) Bundle identifier
# ios.bundle_id =

# (int) Minimum iOS version
# ios.min_version = 13.0

# (str) Development team
# ios.development_team =

# (bool) Use the Python venv to build the iOS app
# ios.use_venv = False

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .ipa) storage
# bin_dir = ./bin

# (str) Python version to use for the build (must be available in your PATH)
# python.version = 3.10

# (list) Profiles to manage specific build options
# profiles =

# (int) Number of processes to use for the build (default: number of CPU cores)
# jobs = 4

# (bool) Enable the new build system (default: True)
# build.use_new = True

# (list) Source files to include for debugging (debug builds)
# debug.include_patterns =

# (list) Source files to exclude for debugging (debug builds)
# debug.exclude_patterns =

# (list) Source files to include for release (release builds)
# release.include_patterns =

# (list) Source files to exclude for release (release builds)
# release.exclude_patterns =

# (str) ANT to use
# ant = ant

# (int) Verbosity of ANT
# ant.verbose = 1

# (str) Force the build to use a specific Python version
# force_python_version = 3.10

# (str) Path to a custom recipe directory
# custom_recipes_dir =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid long downloads on a slow connection
# skip_update = False

# (str) Python version to use for the build (must be available in your PATH)
# python.version = 3.10

# (str) Path to a custom recipe directory
# custom_recipes_dir =

# (bool) If True, then skip trying to update the Android sdk
# This can be useful to avoid long downloads on a slow connection
# skip_update = False