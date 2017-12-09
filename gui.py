import os
import re
import subprocess
import sys
import tkinter as tk
import youtube_dl as ytdl
import configparser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#Spotify credential stuff globals
global SPOTICLI, SPOTISEC

def getSpotifyClientCreds():
  config = configparser.ConfigParser()
  configPath = os.getcwd()
  configPath = configPath + '/config.ini'
  config.read(configPath)

  SPOTICLI = config['keys']['spotify_client_id']
  SPOTISEC = config['keys']['spotify_client_secret']


def getSongData(title):
  songQuery = cleanTitle(title)

#co-opted from musictools package
def cleanTitle(title):
  words_filter = ('official','lyrics','audio','remixed','remix','video','full','version','music','mp3','hd','hq','uploaded','explicit')
  chars_filter = "()[]{}-:_/=+\"\'"

  song_name = title.split()

  song_name = ''.join(map(lambda c: " " if c in chars_filter else c, song_name))
  song_name = re.sub('|'.join(re.escape(key) for key in words_filter), "", song_name, flags=re.IGNORECASE)

  song_name = re.sub(' +', ' ', song_name)

  print(song_name)
  return song_name.strip()

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
    #ydl.download([url])
    vid_info = ydl.extract_info(url, download=False)
    title = vid_info['title']
    print(title)
    clean_title = cleanTitle(title)
    print(clean_title)
    #getSongData(cleanTitle(ydl.extract_info(url, download=False)))
  #moveFiles()

def alterPath():
  currDir = os.getcwd()
  os.environ['PATH'] += os.pathsep + currDir + '\\ffmpeg' + os.pathsep + currDir + '\\ffprobe'

def moveFiles():
  subprocess.call("move *.mp3 %HOMEPATH%/Music/Downloads", shell=True)

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
logInToSpotify()
