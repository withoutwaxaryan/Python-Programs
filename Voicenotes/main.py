from tkinter import *  # import everything from tkinter
# from PIL import Image, ImageTk  # to resize image
from pygame import mixer  # used for music
import tkinter.messagebox  # for pop ups
from tkinter import filedialog
from tkinter import ttk  # tkinter themes
from ttkthemes import themed_tk as tk
from pathlib import Path  # for directory related work
# mutagen --> for audio stuff
import time
import threading

global filename
global stopped
muted = False 
paused = False

# So this is what we are trying to create 
# RootWindow --> StatusBar, LeftFrame, RightFrame
# LeftFrame  --> Listbox ( playlist)
# RightFrame --> TopFrame, MiddleFrame, BottomFrame

# root = Tk()  # creates a window  --> opens only for a few seconds, therefore we use mainloop

root = tk.ThemedTk()  # we use this to add the new theme
root.get_themes()
root.set_theme("radiance")
mixer.init()  # initializing the mixer
root.geometry('700x300')  # TO Give a height and width to the ui
root.title("Voicenotes")
# root.iconbitmap(r"music-note.xbm")  # in Windows image should be of ico type, and for linux it should be of xbm type
# root.tk.call('wm', 'iconphoto', root._w, PhotoImage(file='music-note.png'))  #doesnt work


def pause_music():
    global paused
    global filename
    paused = True
    mixer.music.pause()
    file = Path(filename).stem
    text = " Pausing " + str(file)
    statusbar["text"] = text


def stop_music():
    global stopped
    global filename
    stopped = True 
    mixer.music.stop()
    file = Path(filename).stem
    text = " Stopping " + str(file)
    statusbar["text"] = text


def mute_music():
    global muted
    if muted:
        mixer.music.set_volume(0.7)
        scale.set(70)
        volumeBtn.configure(image=sound_photo)
        muted = False
    else:
        mixer.music.set_volume(0)
        volumeBtn.configure(image=mute_photo)
        muted = True


def set_vol(val):  # mixer volume is only between 0 and 1 , and val is taken by its own in string type. THerefore use the parameter but convert to int first
    volume = float(val)/100  # divide by 100 since we have the scale from 0 to 100
    mixer.music.set_volume(volume)


def about_us():
    tkinter.messagebox.showinfo('Hello World!', 'YEs i made this!')
    # showerror --> pop up showing error
    # showwarning --> pop up showing warning


def browse_file():
    global filename
    filename = filedialog.askopenfilename()
    add_to_playlist(filename)
    # print(filename)
    file = Path(filename).stem
    text = " File Selected : " + str(file)
    statusbar["text"] = text

playlist =[] # items added must contain full path + filename
# this is done since pygame needs the full path in play_music()

def add_to_playlist(file_name):
    index = 0
    file = Path(file_name).stem
    playlistBox.insert(0, file)
    playlist.insert(index, file_name)
    playlistBox.pack()
    index += 1


def del_song():
    selected_song = playlistBox.curselection()
    selected_song = int(selected_song[0])
    playlistBox.delete(selected_song)
    playlist.pop(selected_song)


def show_details(play_song):
    # global filename
    a = mixer.Sound(play_song)
    total_length = a.get_length()
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d} : {:02d}'.format(mins, secs)
    length['text'] = "Song Length  " + timeformat 
    # start_count(total_length) --> will cause the same function being run for a long time, and the other stuff wont work --> threading
    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):  # will need threading
    global paused
    while t and mixer.music.get_busy():  # mixer.music.get_busy returns false when music is stopped
        if paused:
            continue
        else:
            mins, secs = divmod(t, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d} : {:02d}'.format(mins, secs)
            time.sleep(1)
            t = t -1
            remainingtime['text'] = "Remaining Time " + timeformat


def play_music():
    global filename
    global paused
    global playlist
    # mixer.music.load('Falling in love.ogg')  # problem playing mp3 files, works perfectly with ogg
    if paused:
        mixer.music.unpause()
        file = Path(filename).stem
        statusbar["text"] = " Resumed " + str(file) 
        paused = False
    else:
        try:
            stop_music()  # done since if someone presses the play button for another song, we can destroy the previous thread. 
            time.sleep(1)
            selected_song = playlistBox.curselection() # outputs a tuple value
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            file = Path(play_it).stem
            text = " Playing " + str(file)
            statusbar["text"] = text
            show_details(play_it)
        except Exception as e:
            # print(e)
            tkinter.messagebox.showerror("No File added", "Please add music file to play")
            statusbar["text"] = "Error"


# def on_closing():
#     stop_music()
#     root.destroy() # still gives error though
#     #root.quit()


# Create a Menubar
menubar = Menu(root)
root.config(menu=menubar)

# Create Submenus
subMenu = Menu(menubar, tearoff=0)  # tearoff removes a dotted line which appears when the argument is not there
menubar.add_cascade(label="File", menu=subMenu)
subMenu.add_command(label="Open", command=browse_file)
subMenu.add_command(label="Exit", command=root.destroy)

subMenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=subMenu)
subMenu.add_command(label="About Us", command=about_us)

# Status Bar
statusbar = ttk.Label(root, text="Welcome to Voicenotes!", relief_=SUNKEN, anchor=W, font="Times 15 bold")  # W --> west, shifts writing to left
statusbar.pack(side=BOTTOM, fill=X)

# Divide space into left and right frames
leftFrame = Frame(root)
leftFrame.pack(side=LEFT, padx=10)

rightFrame = Frame(root)
rightFrame.pack()

# Creating listbox in leftframe
playlistBox = Listbox(leftFrame)
playlistBox.pack()

#Add, delete button for playlist
add_btn = ttk.Button(leftFrame, text="Add", command=browse_file)
add_btn.pack(side=LEFT, padx=10)
del_btn = ttk.Button(leftFrame, text="Delete", command=del_song)
del_btn.pack(side=LEFT,padx= 5)


# To show stuff in the window you need to 'pack' it.
# You can also use grid, but you cant have both pack and grid in the same file.
# Creating a Text Widget --> Label()
text = ttk.Label(rightFrame, text="For the voices inside my head")
text.pack(pady=10)  # you need to pack up stuff

length = ttk.Label(rightFrame, text="Song Length --:--")
length.pack(pady=5)

remainingtime = ttk.Label(rightFrame, text="Remaining Time --:--", relief=GROOVE)
remainingtime.pack(pady= 10)

# Adding a photo
# play_photo = PhotoImage(file='play-button.png')
# labelphoto = Label(root, image=photo)
# labelphoto.pack()


# Adding a Button 
# We need to add pack since its a layout manager
# we can also create frames which are like Pyqt's layouts for horizontal/vertical layouts
# We have Pack(Frame) Layout Manager & Grid Layout Manager
# pack stacks objects on top to bottom

# Text Button
# btn = Button(root, text=" Smack That", command=play_music_btn)
# btn.pack()


top_frame = Frame(rightFrame)
top_frame.pack()

middle_frame = Frame(rightFrame) #  creating a layout
middle_frame.pack(padx=10)

bottom_frame = Frame(rightFrame)
bottom_frame.pack(pady=18)

# Image Buttons
play_photo = PhotoImage(file='Resources/play-button.png')
playBtn = ttk.Button(middle_frame, image=play_photo, command=play_music)
playBtn.pack(side=LEFT)

pause_photo = PhotoImage(file='Resources/pause-button.png')
pauseBtn = ttk.Button(middle_frame, image=pause_photo, command=pause_music)
pauseBtn.pack(side=LEFT, padx=5)

stop_photo = PhotoImage(file='Resources/stop-button.png')
stopBtn = ttk.Button(middle_frame, image=stop_photo, command=stop_music)
stopBtn.pack(side=LEFT)

mute_photo = PhotoImage(file='Resources/mute.png')
sound_photo = PhotoImage(file='Resources/volume.png')
volumeBtn = ttk.Button(bottom_frame, image=sound_photo, command=mute_music)
volumeBtn.pack(side=LEFT)

# Scale Widget
scale = ttk.Scale(bottom_frame, from_=0, to=100, orient=HORIZONTAL, command=set_vol)
scale.set(70)
mixer.music.set_volume(0.7) # for running the music the first time with specific volume
scale.pack(pady=15)

# root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()  # putting the window in an infinite loop
