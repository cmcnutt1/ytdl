import os
import re
import subprocess
import sys
import tkinter as tk
import requests
import youtube_dl as ytdl
import configparser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from mutagen.id3 import ID3, APIC, _util
from mutagen.mp3 import EasyMP3
from mutagen.easyid3 import EasyID3

#-------------------------------------------------------------------------------


def getSpotifyClientCreds():
  testing = True
  config = configparser.ConfigParser()
  configPath = os.getcwd()
  if(testing):
    configPath = configPath + '/config.ini'
  config.read(configPath)

  spotiCli = config['keys']['spotify_client_id']
  spotiSec = config['keys']['spotify_client_secret']
  
  return [spotiCli, spotiSec]

#-------------------------------------------------------------------------------

def getSongData(title):
  songQuery = cleanTitle(title)
  creds = getSpotifyClientCreds()
  clientCreds = SpotifyClientCredentials(creds[0], creds[1])
  sp = spotipy.Spotify(client_credentials_manager=clientCreds)
  result = sp.search(songQuery, limit=1)
  result = result['tracks']['items'][0]
  track = result['name']
  artist = result['album']['artists'][0]['name']
  album = result['album']['name']
  artLink = result['album']['images'][0]['url']
  print(track)
  print(artist)
  print(album)
  print(artLink)

  return [track, artist, album, artLink]

#-------------------------------------------------------------------------------

#co-opted from musictools package
def cleanTitle(title):
  words_filter = ('official','lyrics','audio','remixed','remix','video','full','version','music','mp3','hd','hq','uploaded','explicit')
  chars_filter = "&()[]{}-:_/=+\"\'"

  song_name = title.split()

  song_name = ' '.join(map(lambda c: " " if c in chars_filter else c, song_name))
  song_name = re.sub('|'.join(re.escape(key) for key in words_filter), "", song_name, flags=re.IGNORECASE)

  song_name = re.sub(' +', ' ', song_name)

  return song_name.strip()

# ------------------------------------------------------------------------------

def applyTags(songData):

  print('doing tag stuff')
  target = getAudioFile()
  tags = EasyID3(target)

  tags['title'] = songData[0]
  tags['artist'] = songData[1]
  tags['album'] = songData[2]

  tags.save()

  print(tags)

  addCoverArt(songData[3])

#-------------------------------------------------------------------------------
  
#also co-opted from musictools package
def addCoverArt(url):
  img = requests.get(url, stream=True)
  img = img.raw
  target = getAudioFile()
  audio = EasyMP3(target, ID3=ID3)

  try:
    audio.add_tags()
  except _util.error:
    pass

  audio.tags.add(
    APIC(
      encoding=3,
      mime='image/png',
      type=3,
      desc='Cover',
      data = img.read()
    )
  )

  print(audio.tags)

  audio.save(v2_version=4)

#-------------------------------------------------------------------------------

def getAudioFile():
  for f in os.listdir(os.getcwd()):
    if f.endswith('.mp3'):
      #audioFile = os.path.join(os.getcwd(), f)
      audioFile = f
  print(audioFile)
  return audioFile

#-------------------------------------------------------------------------------

def download(url, urlType):
  alterPath()
  print(os.environ['PATH'])
  downloadOptions = {
    'format': 'bestaudio/best',
    'postprocessors': [{
      'key': 'FFmpegExtractAudio',
      'preferredcodec': 'mp3',
      'preferredquality': '192'
    }]
  }

  with ytdl.YoutubeDL(downloadOptions) as ydl:
    ydl.download([url])
    vid_info = ydl.extract_info(url, download=False)
    title = vid_info['title']
    try:
      songData = getSongData(title)
      applyTags(songData)
    except:
      pass

  moveFiles()

def alterPath():
  currDir = os.getcwd()
  os.environ['PATH'] += os.pathsep + currDir + '\\ffmpeg' + os.pathsep + currDir + '\\ffprobe'

def moveFiles():
  subprocess.call("move *.mp3 %HOMEPATH%/Music/Downloads/Youtube", shell=True)

class Application(tk.Frame): 

  def my_hook(d):
    if d['status'] == 'finished':
      print('Done downloading. Starting conversion...')
      
  def say_hi(self):
    print("hello world")

  def buttons(self):
    self.QUIT = tk.Button(self)
    self.QUIT["text"] = "exit"
    self.QUIT["fg"] = "red"
    self.QUIT["command"] = self.quit

    self.QUIT.pack({"side": "bottom"})


    self.download = tk.Button(self, text='download', fg='green', bg='black', pady='5.2', command=lambda:download(self.textbox.get(),'song'))
    #self.download['text'] = 'download'
    #self.download['fg'] = 'green'
    #self.download['bg'] = 'black'
    #self.download['command'] = lambda: download('', 'song')

    self.download.place(relx = 0.5, rely=0.5)
    self.download.pack()

    self.textbox = tk.Entry(self, width=50)

    self.textbox.pack({'side': 'top'})

  def setFrame(self):
    self.Win = tk.Frame(self)
    self.Win['height'] = 100
    self.Win['width'] = 100
    self.Win['padx'] = 20
    self.Win['pady'] = 20

    self.Win.pack()


  def __init__(self, master=None):
    super().__init__(master)
    self.pack()
    self.buttons()
    self.setFrame()

root = tk.Tk()
app = Application(master=root)
app.mainloop()
