import tkinter as tk
from tkinter import ttk
import pygame
import os
import fnmatch

# Create the main application window
canvas = tk.Tk()
canvas.title("Music Player")
canvas.geometry("570x580")
canvas.config(bg="#303030")

# Define the root path where the music files are located
rootpath = r"C:\Users\U-ser\Desktop\Python\Music App - Copy\Songs"
pattern = "*.mp3"

# Initialize Pygame and Pygame mixer for playing audio
pygame.init()
pygame.mixer.init()

# Define image paths for various control buttons and icons
prev_img = tk.PhotoImage(file="prev_img.png")
next_img = tk.PhotoImage(file="next_img.png")
pause_img = tk.PhotoImage(file="pause_img.png")
play_img = tk.PhotoImage(file="play_img.png")
volume_icon_img = tk.PhotoImage(file="Volumee.png")
search_icon_img = tk.PhotoImage(file="search.png")
music_icon_img = tk.PhotoImage(file="music.png")

paused = False  # Global variable to track if the music is paused

selected_song = None

# Function to handle the selection of a song in the listbox
def select(event=None):
    global selected_song
    displayed_song_name = listBox.get("anchor")
    if displayed_song_name:
        selected_song = full_song_names[displayed_song_name]  # Get the full filename with .mp3 extension
        label.config(text=displayed_song_name)  # Display the selected song name without the .mp3 extension
        pygame.mixer.music.load(os.path.join(rootpath, selected_song))
        pygame.mixer.music.play()
        playButton.config(image=pause_img, command=pause_resume_toggle)
        update_music_length()
        update_progress()

# Function to play the next song in the list
def play_next():
    global paused, selected_song
    current_index = (listBox.curselection()[0] + 1) % listBox.size()
    selected_song_name = listBox.get(current_index)  # Get the song name from the listbox
    selected_song = full_song_names[selected_song_name]  # Get the full filename with .mp3 extension
    listBox.selection_clear(0, "end")
    listBox.selection_set(current_index)
    label.config(text=selected_song_name)
    pygame.mixer.music.load(os.path.join(rootpath, selected_song))
    pygame.mixer.music.play()
    paused = False  # Reset paused status
    playButton.config(image=pause_img, command=pause_resume_toggle)  # Set button to pause
    update_music_length()  # Reset music length
    update_progress()  # Reset progress bar

# Function to play the previous song in the list
def play_prev():
    global paused, selected_song
    current_index = (listBox.curselection()[0] - 1) % listBox.size()
    selected_song_name = listBox.get(current_index)  # Get the song name from the listbox
    selected_song = full_song_names[selected_song_name]  # Get the full filename with .mp3 extension
    listBox.selection_clear(0, "end")
    listBox.selection_set(current_index)
    label.config(text=selected_song_name)
    pygame.mixer.music.load(os.path.join(rootpath, selected_song))
    pygame.mixer.music.play()
    paused = False  # Reset paused status
    playButton.config(image=pause_img, command=pause_resume_toggle)  # Set button to pause
    update_music_length()  # Reset music length
    update_progress()  # Reset progress bar


# Function to toggle between pause and resume of the music
def pause_resume_toggle():
    global paused
    if paused:  # If music is paused, resume it
        pygame.mixer.music.unpause()
        paused = False
        playButton.config(image=pause_img, command=pause_resume_toggle)
    else:  # If music is playing, pause it
        pygame.mixer.music.pause()
        paused = True
        playButton.config(image=play_img, command=pause_resume_toggle)
    update_progress()  # Update progress when pausing or resuming

# Function to update the displayed music length       
def update_music_length():
    length = pygame.mixer.Sound(rootpath + "\\" + selected_song).get_length()
    mins, secs = divmod(length, 60)
    time_format = '{:02d}:{:02d}'.format(int(mins), int(secs))
    music_length_label.config(text=time_format)
    progress_bar["maximum"] = length
    progress_bar.pack(pady=10)

# Function to update the progress of the currently playing song
def update_progress():
    global paused
    if not paused and pygame.mixer.music.get_busy():  # Check if music is not paused and playing
        current_time = pygame.mixer.music.get_pos() * 0.001  # Convert milliseconds to seconds
        progress_bar.config(value=current_time)
        mins, secs = divmod(current_time, 60)
        time_format = '{:02d}:{:02d}'.format(int(mins), int(secs))
        current_time_label.config(text=time_format)
    elif not pygame.mixer.music.get_busy():  # If music has stopped playing
        handle_song_end(None)  # Start playing the next song
    else:  # If music is paused
        current_time = pygame.mixer.music.get_pos() * 0.001
        progress_bar.config(value=current_time)  # Update progress even when paused
    canvas.after(1000, update_progress)  # Update every second

# Function to set the volume of the music   
def set_volume(volume):
    volume_level = int(volume) / 100  # Convert the scale value to a float between 0.0 and 1.0
    pygame.mixer.music.set_volume(volume_level)

# Function to handle the end of a song and play the next song
def handle_song_end(event):
    global paused, selected_song
    if not paused:
        next_song_index = (listBox.curselection()[0] + 1) % listBox.size()  # Select the next song
        listBox.selection_clear(0, "end")
        listBox.selection_set(next_song_index)

        selected_song = listBox.get(next_song_index)
        label.config(text=selected_song)
        pygame.mixer.music.load(os.path.join(rootpath, full_song_names[selected_song]))
        pygame.mixer.music.play()

        # Update the music length and progress bar for the new song
        length = pygame.mixer.Sound(os.path.join(rootpath, full_song_names[selected_song])).get_length()
        mins, secs = divmod(length, 60)
        time_format = '{:02d}:{:02d}'.format(int(mins), int(secs))
        music_length_label.config(text=time_format)
        progress_bar["maximum"] = length
        progress_bar["value"] = 0  # Reset the progress bar to the beginning
        update_progress()

# Dictionary to store the original indices of songs
original_indices = {}

# Function to search for songs based on user input
def search():
    query = search_var.get().lower()
    listBox.delete(0, "end")  # Clear the listbox
    for song_name, full_name in full_song_names.items():
        if query in song_name.lower():
            listBox.insert("end", song_name)
    # Reset the original indices of songs
    original_indices.clear()
    for index, song_name in enumerate(listBox.get(0, "end")):
        original_indices[song_name] = index
        
# Function to handle focus events on the search entry
def on_entry_focus(event):
    if search_var.get() == search_shadow_text:
        search_entry.delete(0, "end")
        search_entry.config(foreground="black")  
# Function to handle when focus is lost on the search entry
def on_entry_lost_focus(event):
    if not search_var.get():
        search_var.set(search_shadow_text)
        search_entry.config(foreground="grey") 
         
# Create a blank frame above the title frame to create a gap
blank_frame_above_title = tk.Frame(canvas, bg="#303030", height=10)
blank_frame_above_title.pack()        

# Create the title label with the music icon
title_frame = tk.Frame(canvas, bg="#303030")
title_frame.place(relx=0.5, rely=0.1, anchor="center")  # Adjust rely to leave some gap

music_icon_label = tk.Label(title_frame, image=music_icon_img, bg="#303030")
music_icon_label.pack(side="left")

title_label = tk.Label(title_frame, text="Music Player", bg="#303030", fg="white", font=("Helvetica", 20, "bold"))
title_label.pack(side="left")

search_frame = tk.Frame(canvas, bg="#303030")
search_frame.place(relx=0.5, rely=0.2, anchor="center")  # Adjust rely to leave some gap

# Create shadow text for the search box
search_shadow_text = "Search a Song Here"
search_var = tk.StringVar()
search_var.set(search_shadow_text)

# Create the search entry
search_entry = ttk.Entry(search_frame, textvariable=search_var, width=56, font=("Helvetica", 12), foreground="grey")
search_entry.grid(row=0, column=0, padx=(0, 5))
search_entry.bind("<FocusIn>", on_entry_focus)
search_entry.bind("<FocusOut>", on_entry_lost_focus)

search_button = tk.Button(search_frame, image=search_icon_img, bg="#303030", borderwidth=1, command=search)
search_button.grid(row=0, column=1)

# Function to center widgets horizontally
def center_horizontal(widget):
    widget.pack_configure(anchor="center", padx=5)

# Center the title frame
center_horizontal(title_frame)
# Center the search frame
center_horizontal(search_frame)

listbox_font = ("Helvetica", 12, "bold")
listBox = tk.Listbox(canvas, fg="white", bg="#303030", borderwidth=5, selectbackground="#D3D3D3", selectforeground="#000000", selectborderwidth=0, activestyle='none', width=100, font=listbox_font)
listBox.pack(padx=15, pady=(0, 15))

label = tk.Label(canvas, text="All Songs", bg="#303030", fg="white", font=("MonoLisa", 20, "bold"))
label.pack(pady=(5, 15))

progress_bar = ttk.Progressbar(canvas, orient="horizontal", length=450, mode="determinate", value=0)
progress_bar.pack(pady=10)

time_frame = tk.Frame(canvas, bg="#303030")
time_frame.pack(pady=5)

current_time_label = tk.Label(time_frame, text="00:00", bg="#303030", fg="white")
# Place the current time label at the start of the progress bar
current_time_label.pack(side="left")

# Create a frame to add space between the labels
space_frame = tk.Frame(time_frame, bg="#303030")
space_frame.pack(side="left", padx=195)

music_length_label = tk.Label(time_frame, text="00:00", bg="#303030", fg="white")
# Place the music length label at the end of the progress bar
music_length_label.pack(side="right")

control_frame = tk.Frame(canvas, bg="#303030")
control_frame.pack(pady=2)

prevButton = tk.Button(control_frame, text="Prev", image=prev_img, bg="#303030", borderwidth=0, command=play_prev)
prevButton.pack(side="left")

playButton = tk.Button(control_frame, text="Play", image=play_img, bg="#303030", borderwidth=0, command=select)
playButton.pack(side="left")

nextButton = tk.Button(control_frame, text="Next", image=next_img, bg="#303030", borderwidth=0, command=play_next)
nextButton.pack(side="left")

# Create a Label to display the volume icon
volume_icon_label = tk.Label(control_frame, image=volume_icon_img, bg="#303030")
volume_icon_label.pack(side="left")

# Create a Scale widget for volume control
volume_scale = tk.Scale(control_frame, from_=0, to=100, orient="vertical", command=set_volume)
volume_scale.set(50)  # Set the initial volume to 50
volume_scale.pack(side="left")
volume_scale.pack_forget()  # Hide the volume control slider initially
volume_scale.config(length=50, sliderlength=10, showvalue=2)  # Adjust the length and appearance of the volume slider

# Function to show the volume control when the mouse hovers over the icon
def show_volume_control(event):
    volume_scale.pack()  # Show the volume control slider
    volume_scale.place(in_=volume_icon_label, relx=1, rely=0, anchor='ne')

# Function to keep the volume control visible when the mouse is on the volume control
def keep_volume_control(event):
    volume_scale.place(in_=volume_icon_label, relx=1, rely=0, anchor='ne')

# Function to hide the volume control when the mouse leaves the icon
def hide_volume_control(event):
    volume_scale.pack_forget()  # Hide the volume control slider
    volume_scale.place_forget()

# Bind the show, keep, and hide functions to the icon label and volume control
volume_icon_label.bind("<Enter>", show_volume_control)
volume_icon_label.bind("<Leave>", hide_volume_control)
volume_scale.bind("<Enter>", keep_volume_control)
volume_scale.bind("<Leave>", hide_volume_control)
# Bind <<ListboxSelect>> event to the select function to play the selected song
listBox.bind('<<ListboxSelect>>', select)

pygame.mixer.music.set_endevent(pygame.USEREVENT)
canvas.bind(pygame.USEREVENT, handle_song_end)

full_song_names = {}

# Extract and insert filenames without the .mp3 extension into the listbox
for root, dirs, files in os.walk(rootpath):
    for filename in fnmatch.filter(files, pattern):
        # Remove the .mp3 extension from the filename for display
        song_name = filename.replace(".mp3", "")
        listBox.insert("end", song_name)
        # Store the full filename with the .mp3 extension in the dictionary
        full_song_names[song_name] = filename


canvas.mainloop()
