Per Virtual Machine
===================

::

    user kivy
    pwd mao123

Buildozer
---------

Per Installare Buildozer
~~~~~~~~~~~~~~~~~~~~~~~~

Python-for-android compiled with: ./distribute.sh -m "sqlite3 openssl
pyopenssl lxml audiostream cymunk ffmpeg pil pyjnius twisted kivy"

Then go to dist/default, edit the blacklist.txt and remove all the
sqlite3 references.

Then build the launcher with:

::

    ./build.py --package org.kivy.pygame --name "Kivy Launcher" --version 1.1.0.0 --launcher --permission INTERNET --permission BLUETOOTH --permission WAKE_LOCK --icon templates/launcher-icon.png --presplash templates/launcher-presplash.jpg release

Lanciare Buildozer
~~~~~~~~~~~~~~~~~~

::

    buildozer distclean
    buildozer clean
    buildozer android debug deploy

PER WINDOWS
-----------

Usare Cython 0.20 !!!!

Codice funzionante
------------------

Debug
~~~~~

::

    from kivy.core.audio import SoundLoader
    sound = SoundLoader.load("C:\\Mao\\Progetti\\Mentor\\00_MentorApp_2015\\sounds\\sfs.ogg")

Pijunius
~~~~~~~~

::

    AudioManager am = (AudioManager) getSystemService(AUDIO_SERVICE);
    am.setStreamVolume(AudioManager.STREAM_NOTIFICATION, am.getStreamMaxVolume(AudioManager.STREAM_NOTIFICATION), AudioManager.FLAG_PLAY_SOUND);
