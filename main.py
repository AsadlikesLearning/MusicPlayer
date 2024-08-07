import tkinter
import customtkinter
import pygame

from PIL import Image, ImageTk

customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")


class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Asad's Music Player")
        self.root.geometry('400x580')

        pygame.mixer.init()

        self.current_song_index = 0
        self.is_playing = False
        self.is_paused = False

        self.songs = ['music/The search.wav', 'music/city.wav', 'music/Husan.wav']
        self.covers = ['img/nf.jpg', 'img/city.jpg','img/Husan.jpg']

        self.create_widgets()

    def create_widgets(self):
        # Album cover and song name
        self.cover_label = tkinter.Label(self.root)
        self.cover_label.place(relx=0.5, rely=0.3, anchor=tkinter.CENTER)

        self.song_name_label = customtkinter.CTkLabel(self.root, text="", font=("Helvetica", 14))
        self.song_name_label.place(relx=0.5, rely=0.6, anchor=tkinter.CENTER)

        # Buttons
        self.play_button = customtkinter.CTkButton(self.root, text="Play", command=self.toggle_play)
        self.play_button.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        self.skip_f = customtkinter.CTkButton(self.root, text=">", command=self.skip_forward, width=40)
        self.skip_f.place(relx=0.7, rely=0.7, anchor=tkinter.CENTER)

        self.skip_b = customtkinter.CTkButton(self.root, text="<", command=self.skip_back, width=40)
        self.skip_b.place(relx=0.3, rely=0.7, anchor=tkinter.CENTER)

        # Volume slider
        self.volume_slider = customtkinter.CTkSlider(self.root, from_=0, to=1, command=self.set_volume, width=210)
        self.volume_slider.set(0.5)
        self.volume_slider.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

        # Progress bar
        self.progress_bar = customtkinter.CTkProgressBar(self.root, width=250)
        self.progress_bar.place(relx=0.5, rely=0.87, anchor=tkinter.CENTER)
        self.progress_bar.set(0)

        # Time labels
        self.current_time_label = customtkinter.CTkLabel(self.root, text="0:00")
        self.current_time_label.place(relx=0.2, rely=0.92, anchor=tkinter.CENTER)

        self.total_time_label = customtkinter.CTkLabel(self.root, text="0:00")
        self.total_time_label.place(relx=0.8, rely=0.92, anchor=tkinter.CENTER)

    def get_album_cover(self):
        image = Image.open(self.covers[self.current_song_index])
        image = image.resize((250, 250), Image.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        self.cover_label.config(image=photo)
        self.cover_label.image = photo

        song_name = self.songs[self.current_song_index].split('/')[-1][:-4]
        self.song_name_label.configure(text=song_name)

    def toggle_play(self):
        if self.is_playing:
            if self.is_paused:
                pygame.mixer.music.unpause()
                self.is_paused = False
                self.play_button.configure(text="Pause")
            else:
                pygame.mixer.music.pause()
                self.is_paused = True
                self.play_button.configure(text="Resume")
        else:
            self.play_music()

    def play_music(self):
        pygame.mixer.music.load(self.songs[self.current_song_index])
        pygame.mixer.music.play()
        self.is_playing = True
        self.is_paused = False
        self.play_button.configure(text="Pause")
        self.get_album_cover()
        self.update_progress()

    def skip_forward(self):
        self.current_song_index = (self.current_song_index + 1) % len(self.songs)
        self.play_music()

    def skip_back(self):
        self.current_song_index = (self.current_song_index - 1) % len(self.songs)
        self.play_music()

    def set_volume(self, value):
        pygame.mixer.music.set_volume(float(value))

    def update_progress(self):
        if self.is_playing and not self.is_paused:
            current_time = pygame.mixer.music.get_pos() / 1000
            song = pygame.mixer.Sound(self.songs[self.current_song_index])
            total_length = song.get_length()

            # Update progress bar
            progress = current_time / total_length if total_length > 0 else 0
            self.progress_bar.set(progress)

            # Update time labels
            self.current_time_label.configure(text=self.format_time(current_time))
            self.total_time_label.configure(text=self.format_time(total_length))

            if current_time >= total_length:
                self.skip_forward()
            else:
                self.root.after(1000, self.update_progress)

    @staticmethod
    def format_time(seconds):
        minutes, seconds = divmod(int(seconds), 60)
        return f"{minutes}:{seconds:02d}"


if __name__ == "__main__":
    root = customtkinter.CTk()
    app = MusicPlayer(root)
    root.mainloop()