import os   #to fetch songs and directories
from tkinter.filedialog import askdirectory     # for selecting song directory
import pygame   #for playing music
from mutagen.id3 import ID3     #for tagging the meta data to our songs
from tkinter import * #for UI


root = Tk()
root.minsize(400,400)


listofsongs = []
realnames = []


#To currently see which song is being played we need a label on our UI
#that updates as the song changes or updates. To do this we need to define  Label that gets it’s value from a StringVar().
v = StringVar()
songlabel = Label(root,textvariable = v, width = 35)

index = 0

#opening a directory, scanning all the songs in that directory, and then adds them to our listofsongs list.....


def directorychooser():

    directory = askdirectory()  #askdirectory() is a Tk function
    os.chdir(directory)

    #loop over all the files in the directory

    for files in os.listdir(directory):
        #only add files with mp3 extension
        if files.endswith(".mp3"):
            realdir = os.path.realpath(files)

            #load the meta data of that song into audio variable( A dictionary)
            audio = ID3(realdir)

            #TIT2 refers to the TITLE of the song. so lets append that to realnames
            realnames.append(audio['TIT2'].text[0])
            listofsongs.append(files)

    #inializing pygame
    pygame.mixer.init()

    #load the first song
    pygame.mixer.music.load(listofsongs[0])
    pygame.mixer.music.play()

directorychooser()

    #fumction to update our label as the song changes or updates
def updatelabel():
    global index
    global songname

    v.set(realnames[index]) #set StringVar to the real name


# functions to manipulate songs like next,previous,stop.......

def nextsong(event):
    #get index from gloabl
    global index
    #increament index
    index += 1
    #get the nect song from the listofsongs
    pygame.mixer.music.load(listofsongs[index])
    #play the next song
    pygame.mixer.music.play()
    #do not forget to update the Label
    updatelabel()

#similarly for the previous song
def prevsong(event):
    global index
    index -= 1
    pygame.mixer.music.load(listofsongs[index])
    pygame.mixer.music.play()
    updatelabel()

#stop the song!!!
def stopsong(event):
    # stop the current playing song
    pygame.mixer.music.stop()
    #set our label to empty
    v.set("")

def playsong(event):

    pygame.mixer.music.play()



# UI DESIGN


label = Label(root,text = "Music Player")
label.pack()


#listbox to store all songs

listbox = Listbox(root)
listbox.pack()

#inserting songs to the Listbox
# but the listbox will show them in reverse order
# so displaying the reverse of the list will help

realnames.reverse()

for items in realnames:
    listbox.insert(0,items)

realnames.reverse()

#BUTTONS

nextbutton = Button(root,text = "Next")
nextbutton.pack()

prevbutton = Button(root,text = "Previous")
prevbutton.pack()

playbutton = Button(root,text = "Play")
playbutton.pack()

stopbutton = Button(root,text = "Stop")
stopbutton.pack()



#binding buttons the functions

nextbutton.bind("<Button-1>",nextsong)
prevbutton.bind("<Button-1>",prevsong)
stopbutton.bind("<Button-1>",stopsong)
playbutton.bind("<Button-1>",playsong)

songlabel.pack()

root.mainloop()
