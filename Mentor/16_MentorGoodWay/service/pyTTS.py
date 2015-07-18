#!/usr/bin/python
# -*- coding: cp1252 -*-

from win32com.client import WithEvents, Dispatch, constants
from win32com.client import gencache
import os.path, cPickle, re

#make sure the module is generated for static dispatch
#the following 2 lines were automatically generated using
# python win32com/client/makepy.py -i
# and selecting the Microsoft Speech Library
gencache.EnsureModule('{C866CA3A-32F7-11D2-9602-00C04F8EE628}', 0, 5, 0)

#the problem below should go away now that the EnsureModule call is above, fix this
#define constants by hand, using imported constants seems to crash when the module is first built
# [ToDo] refix This - Mao
tts_default = 0 #constants.SVSFDefault
tts_async = 1 # constants.SVSFlagsAsync
tts_purge_before_speak = 2# constants.SVSFPurgeBeforeSpeak
tts_is_filename = 4 #constants.SVSFIsFilename
tts_is_xml = 8 #constants.SVSFIsXML
tts_is_not_xml = 16 #constants.SVSFIsNotXML
tts_persist_xml = 32 # constants.SVSFPersistXML
tts_nlp_speak_punc = 64# constants.SVSFNLPSpeakPunc

class pyTTS(object):
  '''This class wraps the basic functions of the Micrsoft SAPI. It provides simple text-to-speech
  services with support for speech events. Some of the features included are speaking directly to
  audio out, speaking to a wav, speaking from a wav, changing voices, changing the rate of speech,
  and changing the volume of speech.

  Properties:

  'speech': The underlying MS SAPI COM object

  'events': A placeholder for even callbacks

  'file_stream': Underlying COM file stream for speaking to/from disk

  'valid_flags': List of valid flags for SAPI functions

  Managed Properties:

  'OnAudioLevel': Event handler for audio level changes

  'OnBookmark': Event handler for speech stream bookmarks

  'OnEndStream': Event handler for the end of a speech stream

  'OnEnginePrivate': Event handler for private engine events

  'OnPhoneme': Event handler for phonemes in a speech stream

  'OnSentence': Event handler for a sentence boundary in a speech stre

  'OnStartStream': Event handler for the start of a speech stream

  'OnViseme': Event handler for visemes in a speech stream

  'OnVoiceChange': Event handler for voice changes

  'OnWord': Event handler for a word boundary in a speech stream

  'Volume': The volume of the voice

  'Rate': The speech rate of the voice

  'Voice': The voice to use for speaking

  Inner classes:

  'VoiceEvents': Package class that holds data from SAPI callbacks in one place to be returned to a
  higher level application

  'VoiceManager': Class that acts as a switching network for all registered SAPI events
  '''

  class VoiceEvent:
    def __init__(self, **kwargs):
      self.__dict__.update(kwargs)

  class VoiceEventManager:
    def __init__(self):
      self.handlers = {}

    def ConnectHandler(self, name, func):
      if callable(func):
        self.handlers[name] = func

    def DisconnectHandler(self, name):
      try:
        del self.handlers[name]
      except KeyError:
        pass

    def OnAudioLevel(self, stream_number, stream_position, audio_level):
      try:
        name = 'OnAudioLevel'
        func = self.handlers[name]
      except KeyError:
        return

      func(pyTTS.VoiceEvent(StreamNumber = stream_number, StreamPosition = stream_position,
                      AudioLevel = audio_level, Name = name))

    def OnBookmark(self, stream_number, stream_position, bookmark, bookmark_id):
      try:
        name = 'OnBookmark'
        func = self.handlers[name]
      except KeyError:
        return

      func(pyTTS.VoiceEvent(StreamNumber = stream_number, StreamPosition = stream_position,
                      Bookmark = bookmark, BookmarkID = bookmark_id, Name = name))

    def OnEndStream(self, stream_number, stream_position):
      try:
        name = 'OnEndStream'
        func = self.handlers[name]
      except KeyError:
        return

      func(pyTTS.VoiceEvent(StreamNumber = stream_number, StreamPosition = stream_position, Name = name))

    def OnEnginePrivate(self, stream_number, stream_position, engine_data):
      try:
        name = 'OnEnginePrivate'
        func = self.handlers[name]
      except KeyError:
        return

      func(pyTTS.VoiceEvent(StreamNumber = stream_number, StreamPosition = stream_position,
                      EngineData = engine_data, Name = name))

    def OnPhoneme(self, stream_number, stream_position, duration, next_phone_id, feature,
                  current_phone_id):
      try:
        name = 'OnPhoneme'
        func = self.handlers[name]
      except KeyError:
        return

      func(pyTTS.VoiceEvent(StreamNumber = stream_number, StreamPosition = stream_position,
                      Duration = duration, NextPhonemeID = next_phone_id, Feature = feature,
                      CurrentPhonemeID = current_phone_id, Name = name))

    def OnSentence(self, stream_number, stream_position, character_position, length):
      try:
        name = 'OnSentence'
        func = self.handlers[name]
      except KeyError:
        return

      func(pyTTS.VoiceEvent(StreamNumber = stream_number, StreamPosition = stream_position,
                      CharacterPosition = character_position, Length = length,
                      Name = name))

    def OnStartStream(self, stream_number, stream_position):
      try:
        name = 'OnStartStream'
        func = self.handlers[name]
      except KeyError:
        return

      func(pyTTS.VoiceEvent(StreamNumber = stream_number, StreamPosition = stream_position, Name = name))

    def OnViseme(self, stream_number, stream_position, duration, next_viseme_id, feature,
                 current_viseme_id):
      try:
        name = 'OnViseme'
        func = self.handlers[name]
      except KeyError:
        return

      func(pyTTS.VoiceEvent(StreamNumber = stream_number, StreamPosition = stream_position,
                      Duration = duration, NextPhonemeID = next_phone_id, Feature = feature,
                      CurrentPhonemeID = current_phone_id, Name = name))

    def OnVoiceChange(self, stream_number, stream_position, voice_obj_token):
      try:
        name = 'OnVoiceChange'
        func = self.handlers[name]
      except KeyError:
        return

      func(pyTTS.VoiceEvent(StreamNumber = stream_number, StreamPosition = stream_position,
                      VoiceObjectToken = voice_obj_token, Name = name))

    def OnWord(self, stream_number, stream_position, character_position, length):
      try:
        name = 'OnWord'
        func = self.handlers[name]
      except KeyError:
        return

      func(pyTTS.VoiceEvent(StreamNumber = stream_number, StreamPosition = stream_position,
                      CharacterPosition = character_position, Length = length,
                      Name = name))

  def __init__(self):
    '''Initialize an instance of the class.'''
    self.speech = Dispatch('SAPI.SpVoice')
    self.events = WithEvents(self.speech, pyTTS.VoiceEventManager)

    self.valid_flags = [pow(2, x) for x in range(0, 7)]
    self.valid_flags.append(0)

    voice_list = self.speech.GetVoices()
    self.voices = dict([(os.path.basename(voice.Id), voice) for voice in voice_list])

    self.speech.EventInterests = 0

    self.last_speech = ''
    self.format = self.speech.AudioOutputStream.Format.Type

  def __del__(self):
    '''Destroy an instance of the class. Be sure to clean up the COM object references.'''
    del self.events
    del self.speech

  def CheckFlags(self, flags):
    '''Validate speech flags to ensure they are valid. Reduce the list of flags to a single sum
    that can be passed to the COM object.

    Params:

    'flags': A list of possible MS SAPI flags
    '''
    for flag in flags:
      if flag not in self.valid_flags:
        raise ValueError('Invalid Flag')

    return reduce(lambda x, y: x+y, flags, 0)

  def SetOutputFormat(self, rate, bits, channels):
    '''Change the output stream format.

    Params:

    'rate': Sampling rate in kHz (8, 11, 12, 16, 22, 24, 32, 44, 48)

    'bits': Bits per sample (8 or 16)

    'channels': Mono (1) or stereo (2)
    '''
    s = 'SAFT%dkHz%dBit%s' % (rate, bits, (None, 'Mono', 'Stereo')[channels])
    self.format = getattr(constants, s)
    obj = self.speech.AudioOutputStream
    obj.Format.Type = self.format
    self.speech.AllowAudioOutputFormatChangesOnNextSet = False
    self.speech.AudioOutputStream  = obj

  def Speak(self, text, *flags):
    '''Speak some text. Use the flags to configure special speech options.

    Params:

    'text': The text to speech, possibly with embedded XML commands

    'flags': List of TTS flags passed to the underlying COM object
    '''
    flagsum = self.CheckFlags(flags)
    self.speech.Speak(text, flagsum)

  def SpeakFromWave(self, file, *flags):
    '''Speak the contents of a WAV file. Use the flags to configure special speech options. Events
    are fired from the WAV if it was written to disk by the speech engine.

    Params:

    'text': The text to speech, possibly with embedded XML commands

    'flags': List of TTS flags passed to the underlying COM object
    '''
    flagsum = self.CheckFlags(flags)
    file_stream = Dispatch('SAPI.SpFileStream')
    file_stream.Open(file, constants.SSFMOpenForRead)
    self.speech.SpeakStream(file_stream, flagsum)
    file_stream.Close()

  def SpeakToWave(self, file, text, *flags):
    '''Speak to a WAV file. Use the flags the configure special speech options.

    Params:

    'file': The filename of the WAV file to create

    'text': The text to speech, possibly with embedded XML commands

    'flags': List of TTS flags passed to the underlying COM object
    '''
    flagsum = self.CheckFlags(flags)

    #store a reference to the original speach stream
    audio_stream = self.speech.AudioOutputStream

    #redirect the speech to the file
    file_stream = Dispatch('SAPI.SpFileStream')
    file_stream.Format.Type = self.format
    self.speech.AllowAudioOutputFormatChangesOnNextSet = False
    file_stream.Open(file, constants.SSFMCreateForWrite)
    self.speech.AudioOutputStream = file_stream
    self.speech.Speak(text, flagsum)
    file_stream.Close()

    #restore the reference to the original stream
    self.speech.AudioOutputStream = audio_stream

  def SpeakToMemory(self, text, *flags):
    '''Speak to a memory block. Use the flags the configure special speech options.

    Params:

    'text': The text to speech, possibly with embedded XML commands

    'flags': List of TTS flags passed to the underlying COM object

    Returns:

    'mem_stream': SpMemoryStream object containing the speech data
    '''
    flagsum = self.CheckFlags(flags)

    # stare a reference to the original speech stream
    audio_stream = self.speech.AudioOutputStream

    # redirect the speech to memory to speak
    mem_stream = Dispatch('SAPI.SpMemoryStream')
    mem_stream.Format.Type = self.format
    self.speech.AllowAudioOutputFormatChangesOnNextSet = False
    self.speech.AudioOutputStream = mem_stream
    self.speech.Speak(text, flagsum)

    # reset stream to original audio device
    self.speech.AudioOutputStream = audio_stream

    return mem_stream

  def SpeakFromMemory(self, mem_stream, *flags):
    '''Speak the contents of memory block. Use the flags to configure special speech options.

    Params:

    'mem_stream': SpMemoryStream object containing the speech data

    'flags': List of TTS flags passed to the underlying COM object
    '''
    flagsum = self.CheckFlags(flags)
    self.speech.SpeakStream(mem_stream, flagsum)

  def IsSpeaking(self):
    '''Determine if the engine is speaking right now or not.

    Return

    bool: Flag indicates if speaking (True) or not
    '''
    return self.speech.Status.RunningState == 2

  def GetVoices(self):
    '''Get a list of voice objects available on this system.

    Return:

    dict(id : obj): A dictionary of voice objects keyed by ID where ID is the basename of the
    path to the voicefile on the local machine

    Deprecated: Use GetVoiceNames and SetVoiceByName instead or their related managed property,
    Voice
    '''
    return self.voices

  def SetVoice(self, voice_obj):
    '''Set the current voice object to use.

    Params:

    'voice_obj': The voice object to use for any future speech operations.

    Deprecated: Use GetVoiceNames and SetVoiceByName instead or their related managed property,
    Voice
    '''
    self.speech.Voice = voice_obj

  def GetVoiceNames(self):
    '''Get a list of voice names available on this system.

    Return:

    list(string): A list of voice names
    '''
    return self.voices.keys()

  def GetVoice(self):
    '''Gets the name of the currently selected voice.'''
    return os.path.basename(self.speech.Voice.Id)

  def SetVoiceByName(self, voice_name):
    '''Set the current voice to use by name.

    Params:

    'voice_name': The name of the voice to use for any future speech operations.
    '''
    self.speech.Voice = self.voices[voice_name]

  def GetRate(self):
    '''Get the current rate of speech.

    Return:

    int: Rate of speech in range from [-10, 10] from slowest to fastest
    '''
    return self.speech.Rate

  def SetRate(self, rate):
    '''Set the current rate of speech.

    Params:

    'rate': Rate of speech in range from [-10, 10] from slowest to fastest
    '''
    if rate < -10 or rate > 10:
      raise ValueError('Speech rate must be in range [-10, 10]')

    self.speech.Rate = rate

  def GetVolume(self):
    '''Gets the current voice volume.

    Return:

    int: Volume value in range [0,100]
    '''
    return self.speech.Volume

  def SetVolume(self, vol):
    '''Sets the current voice volume.

    Params:

    'vol': The volume to set in range [0,100]
    '''
    if vol < 0 or vol > 100:
      raise ValueError('Volume must be in range [0, 100]')
    self.speech.Volume = vol

  def Pause(self):
    '''Pauses a speech stream to be resumed later.
    '''
    self.speech.Pause()

  def Resume(self):
    '''Resumes a previously paused stream.
    '''
    self.speech.Resume()

  def Skip(self, num_items, type_items="Sentence"):
    '''Skips a number of items in a speech stream.

    Params:

    'num_items': The number of items to skip (positive = forward, negative = backwards)

    'type_items': The type of items to skip (MSSAPI 5.1 only supports sentence skipping)
    '''
    self.speech.Skip(type_items, num_items)

  def Stop(self):
    '''Stop all speech.
    '''
    #fake out the engine by giving it nothing to speak, and telling it to purge before speaking
    self.speech.Speak('', tts_purge_before_speak)

  def Repeat(self, *flags):
    '''Repeat the last thing spoken to audio out only. Use the new flags for configuring the
    engine.

    Params:

    'flags': List of TTS flags passed to the underlying COM object
    '''
    self.speech.Speak(self.last_speech, flags)

  def SubscribeAudioLevel(self, func):
    if func is not None:
      self.events.ConnectHandler('OnAudioLevel', func)
      self.setInterests(constants.SVEAudioLevel, True)
    else:
      self.events.DisconnectHandler('OnAudioLevel')
      self.setInterests(constants.SVEAudioLevel, False)

  def SubscribeBookmark(self, func):
    if func is not None:
      self.events.ConnectHandler('OnBookmark', func)
      self.setInterests(constants.SVEBookmark, True)
    else:
      self.events.DisconnectHandler('OnBookmark')
      self.setInterests(constants.SVEBookmark, False)

  def SubscribeEndStream(self, func):
    if func is not None:
      self.events.ConnectHandler('OnEndStream', func)
      self.setInterests(constants.SVEEndInputStream, True)
    else:
      self.events.DisconnectHandler('OnEndStream')
      self.setInterests(constants.SVEEndInputStream, False)

  def SubscribeEnginePrivate(self, func):
    if func is not None:
      self.events.ConnectHandler('OnEnginePrivate', func)
      self.setInterests(constants.SVEPrivate, True)
    else:
      self.events.DisconnectHandler('OnEnginePrivate')
      self.setInterests(constants.SVEPrivate, False)

  def SubscribePhoneme(self, func):
    if func is not None:
      self.events.ConnectHandler('OnPhoneme', func)
      self.setInterests(constants.SVEPhoneme, True)
    else:
      self.events.DisconnectHandler('OnPhoneme')
      self.setInterests(constants.SVEPhoneme, False)

  def SubscribeSentence(self, func):
    if func is not None:
      self.events.ConnectHandler('OnSentence', func)
      self.setInterests(constants.SVESentenceBoundary, True)
    else:
      self.events.DisconnectHandler('OnSentence')
      self.setInterests(constants.SVESentenceBoundary, False)

  def SubscribeStartStream(self, func):
    if func is not None:
      self.events.ConnectHandler('OnStartStream', func)
      self.setInterests(constants.SVEStartInputStream, True)
    else:
      self.events.DisconnectHandler('OnStartStream')
      self.setInterests(constants.SVEStartInputStream, False)

  def SubscribeViseme(self, func):
    if func is not None:
      self.events.ConnectHandler('OnViseme', func)
      self.setInterests(constants.SVEViseme, True)
    else:
      self.events.DisconnectHandler('OnViseme')
      self.setInterests(constants.SVEViseme, False)

  def SubscribeVoiceChange(self, func):
    if func is not None:
      self.events.ConnectHandler('OnVoiceChange', func)
      self.setInterests(constants.SVEVoiceChange, True)
    else:
      self.events.DisconnectHandler('OnVoiceChange')
      self.setInterests(constants.SVEVoiceChange, False)

  def SubscribeWord(self, func):
    if func is not None:
      self.events.ConnectHandler('OnWord', func)
      self.setInterests(constants.SVEWordBoundary, True)
    else:
      self.events.DisconnectHandler('OnWord')
      self.setInterests(constants.SVEWordBoundary, False)

  def setInterests(self, event_id, state=True):
    '''Set the events we want to watch. This function should not be considered private.

    Params:

    'event_id': The ID of the event

    'state': Flag indicating if we want to start or stop watching
    '''
    i = self.speech.EventInterests

    if state:
      self.speech.EventInterests = i | event_id
    elif i & event_id:
      self.speech.EventInterests = i ^ event_id

  OnAudioLevel = property(fset=SubscribeAudioLevel)
  OnBookmark = property(fset=SubscribeBookmark)
  OnEndStream = property(fset=SubscribeEndStream)
  OnEnginePrivate = property(fset=SubscribeEnginePrivate)
  OnPhoneme = property(fset=SubscribePhoneme)
  OnSentence = property(fset=SubscribeSentence)
  OnStartStream = property(fset=SubscribeStartStream)
  OnViseme = property(fset=SubscribeViseme)
  OnVoiceChange = property(fset=SubscribeVoiceChange)
  OnWord = property(fset=SubscribeWord)

  Volume = property(fget=GetVolume, fset=SetVolume)
  Rate = property(fget=GetRate, fset=SetRate)
  Voice = property(fget=GetVoice, fset=SetVoiceByName)

class Pronounce(object):
  tts_phonetic = 0
  tts_misspelled = 1

  class Translator(dict):
    '''Class the replaces words with phonetic representations or misspellings in order to correct
    for pronunciation. This class is based on the Xlator class by Xavier Defrang.'''
    def __init__(self, d):
      dict.__init__(self, d)
      self.regex = self.makeRegex()

    def makeRegex(self):
      return re.compile(r'\b'+r'\b|\b'.join(map(re.escape, self.keys()))+r'\b')

    def __call__(self, match):
      try:
        pron, type = self[match.group(0)]
      except:
        return

      if type == Pronounce.tts_phonetic:
        return '<pron sym="'+pron+'" />'
      else:
        return pron

    def Translate(self, text):
      return self.regex.sub(self, text.lower())

  '''Class that allows user specified corrections to text-to-speech pronunciations.'''
  def __init__(self, filename=None):
    '''Initialize an instance of the class. Load a dictionary immediately if one is given.

    Params:

    'filename': Name of the dictionary file to load
    '''
    if filename is None:
      self.dictionary = {}
      self.trans = None
    else:
      self.LoadDictionary(filename)

  def New(self):
    '''Start a new dictionary.'''
    self.dictionary = {}

  def Open(self, filename):
    '''Load a dictionary from disk.

    Params:

    'filename': Name of the dictionary to load
    '''
    f = open(filename, 'r')
    self.dictionary = cPickle.load(f)
    f.close()
    self.trans = Pronounce.Translator(self.dictionary)

  def Save(self, filename):
    '''Save a dictionary to disk.

    Params:

    'filename': Name of the dictionary to save
    '''
    f = open(filename, 'w')
    cPickle.dump(self.dictionary, f, True)
    f.close()

  def AddMisspelled(self, word, pron):
    '''Add a phonetic pronunciation to the dictionary. See the SAPI documentation for allowed
    phonetic symbols and stress marks.

    Params:

    'word': The correctly spelled word

    'pron': The pronunciation given by mispelling the correct word

    Return:

    bool: Flag indicating if word was already in the dictionary
    '''
    r = self.dictionary.has_key(word.lower())
    self.dictionary[word.lower()] = pron, Pronounce.tts_misspelled
    self.trans = Pronounce.Translator(self.dictionary)
    return r

  def AddPhonetic(self, word, pron):
    '''Add a phonetic pronunciation to the dictionary. See the SAPI documentation for allowed
    phonetic symbols and stress marks.

    Params:

    'word': The correctly spelled word

    'pron': The phonetic pronunciation of the word consisting of internationally recognized phenomes

    Return:

    bool: Flag indicating if word was already in the dictionary
    '''
    r = self.dictionary.has_key(word.lower())
    self.dictionary[word.lower()] = pron, Pronounce.tts_phonetic
    self.trans = Pronounce.Translator(self.dictionary)
    return r

  def RemoveWord(self, word):
    '''Remove a word from the dictionary.

    Params:

    'word': The word to remove
    '''
    try:
      del self.dictionary[word]
    except KeyError:
      pass

  def ListWords(self):
    '''Return a list of all the words in the dictionary.

    Return:

    list: List of all words in the dictionary
    '''
    return self.dictionary.keys()

  def GetPronunciation(self, word):
    '''Return the pronunciation text and type associated with the given word.

    Return:

    tuple(int, string): A tuple containing the type of pronunciation and its string.
    '''
    try:
      return self.dictionary[word]
    except KeyError:
      return None

  def Correct(self, text):
    '''Parse a text string and correct it for pronunciation according to the rules of the currently
    loaded dictionary.

    Params:

    'text': The text string to correct for pronunciation
    '''
    if self.trans is None:
      return text
    else:
      return self.trans.Translate(text)

  def CorrectNow(cls, word, pron, type=0):
    t = cls.Translator({word.lower() : (pron.lower(), type)})
    return t.Translate(word)

  CorrectNow = classmethod(CorrectNow)

if __name__ == '__main__':
  #tts = pyTTS()
  #p = Pronounce()
  #p.AddPhonetic('Alt', 'ao l t 1')
  #p.AddMisspelled('Ctrl', 'Control')
  #text = 'The alt key is the lamest ever. But the Ctrl key is the coolest!.'
  #print text
  #tts.Speak(text, tts_is_xml)
  pass

