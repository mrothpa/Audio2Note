import tkinter as tk
from tkinter import ttk

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), './functions')))

import database
from download_drive_file import main
import transcribe
import summarize
import notion

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
        
        self.files = self.prepare()
        # print(self.files)
        
        self.title("Collapsible Frames")
        self.geometry("400x400")  # Fenstergröße
        
        # Erstellen der CollapsibleFrames
        for title, content in self.files.items():
            frame = CollapsibleFrame(self, title, content)
            frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Erstellen der Buttons
        button_frame = tk.Frame(self)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        button_frame.grid_rowconfigure(0, weight=1)
        button_frame.grid_columnconfigure([0, 1, 2, 3], weight=1)
        
        buttons = [
            ("Download", self.download, "yellow"),
            ("Transcribe", self.transcribe, "red"),
            ("Upload", self.upload, "blue"),
            ("All", self.all, "green")
        ]
        
        for text, func, color in buttons:
            button = tk.Button(button_frame, text=text, command=func, bg=color, fg="white", font=("Arial", 10, "bold"), width=9, height=2, relief="raised", borderwidth=2)
            button.pack(side=tk.LEFT, padx=5, pady=5)
    
    def prepare(self):
        result = database.read_google()
        # print(result)
        missing_files_google = main(file_list=result)
        # print("Fehlende Dateien von Google Drive:", missing_files_google)
        database.add_google(data=missing_files_google)
        
        result_sort = database.sort_data()
        # print(f"Result Sorted: {result_sort}")
        return result_sort
    
    def download(self):
        result = database.read_google()
        download_files = database.filter_download()
        missing_files = main(file_list=result, download_folder="Audios", download=True, download_file_list=download_files)
        database.update_download_files(download_files)

    def transcribe(self):
        transcribe_files = database.filter_transcribe()
        # print(transcribe_files)
        for name, id_ in transcribe_files.items():
            print(f"Name des Audions: {name}")
            text = transcribe.transcribe(name)
            corrected_text = summarize.correct_text(text)
            summarized_text = summarize.summarize_text(corrected_text)
            print(f"Text: {text}")
            print(f"Summary: {summarized_text}")
            database.update_transcribe(id_, text, summarized_text)
            print()

    def upload(self):
        upload_files = database.filter_upload()
        for name, id_ in upload_files.items():
            print(f"Name des AUdios: {name}")
            result = database.read_upload(id_)
            # print(f"Result: {result}")
            name_result, id_result, translation, summary = result
            
            notion.add_page(name=name_result, id_=id_result, translation=translation, summary=summary)
            database.update_upload(id_)
            

    def all(self):
        self.download()
        self.transcribe()
        self.upload()

if __name__ == "__main__":
    app = App()
    app.mainloop()