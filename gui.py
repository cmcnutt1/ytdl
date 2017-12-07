import os
import subprocess
import sys
import tkinter as tk
import youtube_dl as ytdl

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
  moveFiles()

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
