# Find some kind of TTS functionality and assign it to tts
# On OSX and Linux, not implemented
# On Android we use the TTS feature included with Android.
# If no TTS is found, we use notts, which just echoes the message to the console
__version__ = '0.0.10'

from kivy.utils import Platform
from kivy.core.audio import SoundLoader #Without this TTS doesn't work!!

platform = Platform()  # ToDo aggiustare riconoscimento piattaforma
debug = False


def tts_android(message, language="EN"):
    if tts.isSpeaking():
        res = -1
    else:
        if language == "IT":
            tts.setLanguage(Locale.ITALY)
        elif language == "BR":
            tts.setLanguage(Locale.BRAZIL)
        else:
            tts.setLanguage(Locale.US)
        res = tts.speak(message, TextToSpeech.QUEUE_FLUSH, None)
    if debug:
        print "TTS android Result is {}".format(res)
    return res


def tts_speak_win(message, language="EN"):
    list_voices = tts.GetVoices()
    if language == "IT":
        tts.SetVoice(list_voices['ScanSoftSilvia_Dri40_16kHz'])
    elif language == "BR":
        tts.SetVoice(list_voices['eSpeak_3'])
    else:
        tts.SetVoice(list_voices['MS-Anna-1033-20-DSK'])
    if not tts.IsSpeaking():
        tts.Speak(message)
        res = 0
    else:
        res = -1
    if debug:
        print "TTS for windows Result is {}".format(res)
    return res


def tts_speak_notts(message, language="EN"):
    """
     Echoes the message to the console
    :param message:
    :return:
    """
    print 'FakeTTS: {} spoken in {}'.format(message, language)
    return 0

# Platform-specific searches
if platform == "android":
    from os import environ
    from jnius import autoclass
    if 'PYTHON_SERVICE_ARGUMENT' in environ:
        PythonService = autoclass('org.renpy.android.PythonService')
        activity = PythonService.mService
    else:
        PythonActivity = autoclass('org.renpy.android.PythonActivity')
        activity = PythonActivity.mActivity
    Locale = autoclass('java.util.Locale')
    TextToSpeech = autoclass('android.speech.tts.TextToSpeech')
    tts = TextToSpeech(activity, None)
    speak = tts_android
    isSpeaking = tts.isSpeaking
elif platform == "win":
    from pyTTS import pyTTS
    tts = pyTTS()
    tts.SetRate(-2)
    speak = tts_speak_win
    isSpeaking = tts.IsSpeaking
else:  # Default to no TTS
    speak = tts_speak_notts

