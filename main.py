import tkinter as tk
from tkinter import ttk

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './functions')))

import database
from download_drive_file import main

class CollapsibleFrame(ttk.Frame):
    def __init__(self, parent, title, content, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.title = title
        self.is_expanded = False
        
        # Header Frame für Button
        self.header = ttk.Frame(self)
        self.header.pack(fill=tk.X, padx=5, pady=2)
        
        # Button mit fester Breite und zentriert
        self.toggle_button = ttk.Button(self.header, text=f"> {self.title}", command=self.toggle)
        self.toggle_button.pack(side=tk.TOP, padx=15, pady=2, fill=tk.X)
        
        # Content Frame, anfangs versteckt
        self.content = tk.Frame(self)
        self.content.pack_forget()
        
        # Inhalt des Balkens
        self.content_text = tk.Label(self.content, text="\n".join(content), justify=tk.LEFT, anchor="w")
        self.content_text.pack()
        
    def toggle(self):
        if self.is_expanded:
            self.content.pack_forget()
            self.toggle_button.config(text=f"> {self.title}")
        else:
            self.content.pack(fill=tk.X, padx=5, pady=2)
            self.toggle_button.config(text=f"v {self.title}")
        self.is_expanded = not self.is_expanded

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.prepare()
        
        self.title("Collapsible Frames")
        self.geometry("400x400")  # Fenstergröße
        
        # Define the data
        data = {
            "Google Drive": ["lorem 1", "lorem 2", "lorem 3"],
            "Local": ["lorem 4", "lorem 5", "lorem 6"],
            "Transcripted": ["lorem 7", "lorem 8", "lorem 9"],
            "Finished": ["lorem 10", "lorem 11", "lorem 12"]
        }
        
        # Erstellen der CollapsibleFrames
        for title, content in data.items():
            frame = CollapsibleFrame(self, title, content)
            frame.pack(fill=tk.X, padx=10, pady=5)
    
    def prepare(self):
        result = database.read_google()
        # print(result)
        missing_files_google = main(file_list=result, download_folder="Audios")
        print("Fehlende Dateien von Google Drive:", missing_files_google)
        database.add_google(data=missing_files_google)

if __name__ == "__main__":
    app = App()
    app.mainloop()