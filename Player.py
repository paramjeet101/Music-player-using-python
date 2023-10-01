import os
import time
from tkinter import *
from tkinter import filedialog
from pygame import mixer
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

root=Tk()
root.title("Python Music Player")
root.geometry("650x450")
root.config(bg="#333333")

#pygame intialized
mixer.init()

Playlist=Listbox(root,bg="black",fg="cyan",width=100)
Playlist.pack(pady=15,padx=15)

#global pause variable 
global paused
paused=False

    
#adding song
def add_song():
    song=filedialog.askopenfilename(title="Choose A song",filetypes=(("mp3 Files","*.mp3"),))
    
    #remove directory name and mp3 from song
    song=song.replace("/Users/trycatchair2/Downloads/","")
    song=song.replace(".mp3","")
    Playlist.insert(END,song)
                
#playing song
def play_song():
    song=Playlist.get(ACTIVE)
    song=f'/Users/trycatchair2/Downloads/{song}.mp3'
    
    mixer.music.load(song)
    mixer.music.play(loops=0)
    
    #call the time function to get the music length
    playtime()
    
    #scrollbar seting as mp3 timer
    slider_position=int(muted_song_length)
    slider.config(to=slider_position)

#stop playing current song
def stop_song():
    mixer.music.stop()
    Playlist.selection_clear(ACTIVE)
    
#deleting song from playlist
def delete_song():
    Playlist.delete(ANCHOR)
    mixer.music.stop()

#pause song
def pause_song(is_paused):
    global paused
    paused=is_paused
    if paused:
        mixer.music.unpause()
        paused=False
    else:
        mixer.music.pause()
        paused=True
    
def addmore_song():
    song=filedialog.askopenfilenames(title="Choose A song",filetypes=(("mp3 Files","*.mp3"),))
    
    for more in song:
        #remove directory name and mp3 from song
        more=more.replace("/Users/trycatchair2/Downloads/","")
        more=more.replace(".mp3","")
        Playlist.insert(END,more)

def deleteall_song():
    Playlist.delete(0,END)
    mixer.music.stop()
    
def prev_song():
    next_play=Playlist.curselection()
    next_play=next_play[0]-1
    song=Playlist.get(next_play)
    song=f'/Users/trycatchair2/Downloads/{song}.mp3'
    
    mixer.music.load(song)
    mixer.music.play(loops=0)
    
    #clear selected song 
    Playlist.selection_clear(0,END)
    
    #active the next song
    Playlist.activate(next_play)
    Playlist.selection_set(next_play,last=None)

def next_song():
    next_play=Playlist.curselection()
    next_play=next_play[0]+1
    song=Playlist.get(next_play)
    song=f'/Users/trycatchair2/Downloads/{song}.mp3'
    
    mixer.music.load(song)
    mixer.music.play(loops=0)
    
    #clear selected song 
    Playlist.selection_clear(0,END)
    
    #active the next song
    Playlist.activate(next_play)
    Playlist.selection_set(next_play,last=None)
    
#playtime
def playtime():
    current_time=mixer.music.get_pos() / 1000
    convert_current_time=time.strftime('%M:%S', time.gmtime(current_time))
    
    #getting length of song with mutagen
    
    #getting current song
    current_play=Playlist.curselection()
    song=Playlist.get(current_play)
    song=f'/Users/trycatchair2/Downloads/{song}.mp3'
    muted_song=MP3(song)
    global muted_song_length
    muted_song_length=muted_song.info.length
    convert_muted_song_length=time.strftime('%M:%S', time.gmtime(muted_song_length))
    
    slider_position=int(muted_song_length)
    current_time+=1
    slider.config(to=slider_position,value=current_time)
    
    timing.config(text=f'Time Elapsed : {convert_current_time} of {convert_muted_song_length}')
    timing.after(1000,playtime)
    slider.config(value=current_time)



    
    
timing=Label(root,text='',bd=1,relief=GROOVE)
timing.pack(fill=X,side=BOTTOM,ipady=2)

add_button=Button(root,text="Add file",height=2,command=add_song)
add_button.place(relx=0.17,rely=0.47)

addmore_button=Button(root,text="Add More file",height=2,command=addmore_song)
addmore_button.place(relx=0.33,rely=0.47)

delete_button=Button(root,text="Delete file",height=2,command=delete_song)
delete_button.place(relx=0.53,rely=0.47)

deleteall_button=Button(root,text="Delete All file",height=2,command=deleteall_song)
deleteall_button.place(relx=0.71,rely=0.47)

prev_button=Button(root,text="Prev",height=2,command=prev_song)
prev_button.place(relx=0.17,rely=0.65)

play_button=Button(root,text="Play",height=2,command=play_song)
play_button.place(relx=0.31,rely=0.65)

pause_button=Button(root,text="Pause",height=2,command=lambda: pause_song(paused))
pause_button.place(relx=0.45,rely=0.65)

stop_button=Button(root,text="Stop",height=2,command=stop_song)
stop_button.place(relx=0.59,rely=0.65)

next_button=Button(root,text="Next",height=2,command=next_song)
next_button.place(relx=0.75,rely=0.65)

slider=ttk.Scale(root,from_=0,to=100,orient=HORIZONTAL,value=0,length=400)
slider.place(relx=0.2,rely=0.85)

root.mainloop()