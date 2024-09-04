import tkinter as tk
from tkinter import filedialog, messagebox
from queue import Queue
import customtkinter as ctk
import cv2
import os
from PIL import Image, ImageTk
import threading
import yt_dlp  # Import yt-dlp

class VideoConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Red Halo Converter")
        self.root.geometry("900x900")
        self.root.resizable(True, True)
        self.root.iconbitmap("F:/Projects/Video Converter/myicon.ico")

        # Load logo image
        self.logo_image = Image.open("F:/Projects/Video Converter/logo.png")
        self.logo = ImageTk.PhotoImage(self.logo_image)

        # Main frame
        self.frame = ctk.CTkFrame(root, width=900, height=900, corner_radius=10, fg_color="#333333")
        self.frame.pack(fill="both", expand=True)

        # Tabview
        self.tabview = ctk.CTkTabview(self.frame, width=900, height=900, corner_radius=10)
        self.tabview.pack(fill="both", expand=True)

        # Tabs
        self.home_tab = self.tabview.add("Home")
        self.video_tab = self.tabview.add("Video Conversion")
        self.youtube_tab = self.tabview.add("YouTube Downloader")

        # Task queue
        self.task_queue = Queue()

        # Setup Tabs
        self.setup_home_tab()
        self.setup_video_tab()
        self.setup_youtube_tab()

    def setup_home_tab(self):
        self.home_tab.grid_columnconfigure(0, weight=1)
        self.home_tab.grid_rowconfigure(0, weight=1)
        self.home_tab.grid_rowconfigure(1, weight=1)
        self.home_tab.grid_rowconfigure(2, weight=1)

        # Add logo
        logo_label = tk.Label(self.home_tab, image=self.logo, bg="#333333")
        logo_label.grid(row=0, column=0, columnspan=1, pady=30)

        title_label = ctk.CTkLabel(self.home_tab, text="Red Halo Converter", font=("Arial", 30, "bold"), text_color="#FFFFFF")
        title_label.grid(row=1, column=0, pady=40, padx=20, sticky='n')

        video_button = ctk.CTkButton(self.home_tab, text="Video Converter", command=self.open_video_converter, 
                                    fg_color="#E53935", hover_color="#D32F2F", text_color="#FFFFFF", font=("Arial", 18, "bold"))
        video_button.grid(row=2, column=0, pady=20, padx=20, ipadx=10, ipady=10)

        youtube_button = ctk.CTkButton(self.home_tab, text="YouTube Downloader", command=self.open_youtube_downloader, 
                                      fg_color="#E53935", hover_color="#D32F2F", text_color="#FFFFFF", font=("Arial", 18, "bold"))
        youtube_button.grid(row=3, column=0, pady=20, padx=20, ipadx=10, ipady=10)

    def setup_video_tab(self):
        # Configure grid for responsive layout
        for i in range(10):
            self.video_tab.grid_rowconfigure(i, weight=1)
        self.video_tab.grid_columnconfigure(0, weight=1)
        self.video_tab.grid_columnconfigure(1, weight=2)
        self.video_tab.grid_columnconfigure(2, weight=1)

        # Add logo
        logo_label = tk.Label(self.video_tab, image=self.logo, bg="#333333")
        logo_label.grid(row=0, column=0, columnspan=3, pady=30)

        title_label = ctk.CTkLabel(self.video_tab, text="Video Converter", font=("Arial", 30, "bold"), text_color="#FFFFFF")
        title_label.grid(row=1, column=0, columnspan=3, pady=20)

        # Input file
        self._create_file_selector(self.video_tab, "Input File:", 2, self.select_input_file, "input_file_label")

        # Output folder
        self._create_file_selector(self.video_tab, "Output Folder:", 3, self.select_output_folder, "output_folder_label")

        # Output file name
        output_file_name_label = ctk.CTkLabel(self.video_tab, text="Output File Name:", font=("Arial", 20), text_color="#FFFFFF")
        output_file_name_label.grid(row=4, column=0, padx=20, pady=15, sticky='e')
        self.output_file_name_entry = ctk.CTkEntry(self.video_tab, font=("Arial", 20), fg_color="#FFFFFF", text_color="#000000", width=400, height=40)
        self.output_file_name_entry.grid(row=4, column=1, padx=20, pady=15, sticky='ew')

        # Format selection
        format_label = ctk.CTkLabel(self.video_tab, text="Format:", font=("Arial", 20), text_color="#FFFFFF")
        format_label.grid(row=5, column=0, padx=10, pady=15, sticky='e')
        self.format_var = tk.StringVar(value='avi')
        format_menu = ctk.CTkOptionMenu(self.video_tab, variable=self.format_var, values=['avi', 'mp4', 'mov'], 
                                        button_color="#E53935", button_hover_color="#D32F2F", 
                                        fg_color="#FFFFFF", text_color="#000000", font=("Arial", 20))
        format_menu.grid(row=5, column=1, padx=10, pady=15, sticky='ew')

        # Convert button
        self.create_rounded_button(self.video_tab, "Convert", self.add_conversion_task, row=6, column=1, font=("Arial", 20, "bold"), button_height=50, button_width=200)

        # Status label and spinner
        self.status_label = ctk.CTkLabel(self.video_tab, text="", font=("Arial", 20), text_color="#FFFFFF")
        self.status_label.grid(row=7, column=0, columnspan=3, pady=15, sticky='n')

        # Spinner
        self.spinner = ctk.CTkProgressBar(self.video_tab, mode='indeterminate', height=30)
        self.spinner.grid(row=8, column=0, columnspan=3, pady=15, sticky='n')
        self.spinner.grid_forget()

        # Add Back button
        back_button = ctk.CTkButton(self.video_tab, text="Back", command=self.show_home_screen, 
                                    fg_color="#E53935", hover_color="#D32F2F", text_color="#FFFFFF", font=("Arial", 20, "bold"), width=200, height=50)
        back_button.grid(row=9, column=0, padx=20, pady=20, sticky='w')

        # Task list
        self.task_list = ctk.CTkLabel(self.video_tab, text="", font=("Arial", 16), text_color="#FFFFFF", justify="left")
        self.task_list.grid(row=10, column=0, columnspan=3, pady=15, sticky='n')

    def setup_youtube_tab(self):
        # Configure grid for responsive layout
        for i in range(8):
            self.youtube_tab.grid_rowconfigure(i, weight=1)
        self.youtube_tab.grid_columnconfigure(0, weight=1)
        self.youtube_tab.grid_columnconfigure(1, weight=2)
        self.youtube_tab.grid_columnconfigure(2, weight=1)

        # Add logo
        logo_label = tk.Label(self.youtube_tab, image=self.logo, bg="#333333")
        logo_label.grid(row=0, column=0, columnspan=3, pady=30)

        title_label = ctk.CTkLabel(self.youtube_tab, text="YouTube Downloader", font=("Arial", 30, "bold"), text_color="#FFFFFF")
        title_label.grid(row=1, column=0, columnspan=3, pady=20)

        # YouTube URL
        url_label = ctk.CTkLabel(self.youtube_tab, text="YouTube URL:", font=("Arial", 20), text_color="#FFFFFF")
        url_label.grid(row=2, column=0, padx=20, pady=15, sticky='e')
        self.youtube_url_entry = ctk.CTkEntry(self.youtube_tab, font=("Arial", 20), fg_color="#FFFFFF", text_color="#000000", width=400, height=40)
        self.youtube_url_entry.grid(row=2, column=1, padx=20, pady=15, sticky='ew')

        # Download location
        location_label = ctk.CTkLabel(self.youtube_tab, text="Download Location:", font=("Arial", 20), text_color="#FFFFFF")
        location_label.grid(row=3, column=0, padx=20, pady=15, sticky='e')
        self.download_location_entry = ctk.CTkEntry(self.youtube_tab, font=("Arial", 20), fg_color="#FFFFFF", text_color="#000000", width=400, height=40)
        self.download_location_entry.grid(row=3, column=1, padx=20, pady=15, sticky='ew')
        location_button = ctk.CTkButton(self.youtube_tab, text="Browse", command=self.select_download_location, 
                                       fg_color="#E53935", hover_color="#D32F2F", text_color="#FFFFFF", font=("Arial", 20, "bold"))
        location_button.grid(row=3, column=2, padx=20, pady=15)

        # Format selection (Video/Audio)
        format_label = ctk.CTkLabel(self.youtube_tab, text="Format:", font=("Arial", 20), text_color="#FFFFFF")
        format_label.grid(row=4, column=0, padx=10, pady=15, sticky='e')
        self.format_var = tk.StringVar(value='video')
        format_menu = ctk.CTkOptionMenu(self.youtube_tab, variable=self.format_var, values=['video', 'audio'], 
                                        button_color="#E53935", button_hover_color="#D32F2F", 
                                        fg_color="#FFFFFF", text_color="#000000", font=("Arial", 20))
        format_menu.grid(row=4, column=1, padx=10, pady=15, sticky='ew')

        # Download button
        self.create_rounded_button(self.youtube_tab, "Download", self.download_video, row=5, column=1, font=("Arial", 20, "bold"), button_height=50, button_width=200)

        # Status label and spinner
        self.youtube_status_label = ctk.CTkLabel(self.youtube_tab, text="", font=("Arial", 20), text_color="#FFFFFF")
        self.youtube_status_label.grid(row=6, column=0, columnspan=3, pady=15, sticky='n')

        # Spinner
        self.youtube_spinner = ctk.CTkProgressBar(self.youtube_tab, mode='indeterminate', height=30)
        self.youtube_spinner.grid(row=7, column=0, columnspan=3, pady=15, sticky='n')
        self.youtube_spinner.grid_forget()

        # Add Back button
        back_button = ctk.CTkButton(self.youtube_tab, text="Back", command=self.show_home_screen, 
                                    fg_color="#E53935", hover_color="#D32F2F", text_color="#FFFFFF", font=("Arial", 20, "bold"), width=200, height=50)
        back_button.grid(row=8, column=0, padx=20, pady=20, sticky='w')

    def _create_file_selector(self, parent, label_text, row, command, var_name):
        label = ctk.CTkLabel(parent, text=label_text, font=("Arial", 20), text_color="#FFFFFF")
        label.grid(row=row, column=0, padx=20, pady=15, sticky='e')
        entry = ctk.CTkEntry(parent, font=("Arial", 20), fg_color="#FFFFFF", text_color="#000000", width=400, height=40)
        entry.grid(row=row, column=1, padx=20, pady=15, sticky='ew')
        button = ctk.CTkButton(parent, text="Browse", command=command, 
                              fg_color="#E53935", hover_color="#D32F2F", text_color="#FFFFFF", font=("Arial", 20, "bold"))
        button.grid(row=row, column=2, padx=20, pady=15)

    def create_rounded_button(self, parent, text, command, row, column, font=("Arial", 20, "bold"), button_height=50, button_width=200):
        button = ctk.CTkButton(parent, text=text, command=command, font=font, 
                              fg_color="#E53935", hover_color="#D32F2F", text_color="#FFFFFF", 
                              width=button_width, height=button_height)
        button.grid(row=row, column=column, padx=20, pady=20)

    def select_input_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mov")])
        if file_path:
            self.input_file_path = file_path
            self.input_file_label.configure(text=file_path)

    def select_output_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_folder_path = folder_path
            self.output_folder_label.configure(text=folder_path)

    def select_download_location(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.download_location_entry.delete(0, tk.END)
            self.download_location_entry.insert(0, folder_path)

    def add_conversion_task(self):
        # Get user inputs
        input_file = getattr(self, 'input_file_path', None)
        output_folder = getattr(self, 'output_folder_path', None)
        output_file_name = self.output_file_name_entry.get()
        file_format = self.format_var.get()

        if not input_file or not output_folder or not output_file_name:
            messagebox.showerror("Error", "Please fill all fields and select files/folders.")
            return

        task_description = f"Converting {os.path.basename(input_file)} to {file_format.upper()} in {output_folder} as {output_file_name}.{file_format}"
        self.task_list.configure(text=task_description)
        self.status_label.configure(text="Conversion in progress...")
        self.spinner.grid()

        # Create a thread to perform the conversion
        conversion_thread = threading.Thread(target=self.convert_video, args=(input_file, output_folder, output_file_name, file_format))
        conversion_thread.start()

    def convert_video(self, input_file, output_folder, output_file_name, file_format):
        # Perform the video conversion
        try:
            output_file = os.path.join(output_folder, f"{output_file_name}.{file_format}")
            cap = cv2.VideoCapture(input_file)
            fourcc = cv2.VideoWriter_fourcc(*"XVID")
            out = cv2.VideoWriter(output_file, fourcc, 20.0, (640, 480))
            
            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                out.write(frame)
            
            cap.release()
            out.release()
            self.status_label.configure(text="Conversion completed!")
        except Exception as e:
            self.status_label.configure(text=f"Error: {str(e)}")
        finally:
            self.spinner.grid_forget()

    def download_video(self):
        url = self.youtube_url_entry.get()
        download_location = self.download_location_entry.get()
        format_choice = self.format_var.get()

        if not url or not download_location:
            self.youtube_status_label.configure(text="Please fill all fields.")
            return

        self.youtube_status_label.configure(text="Downloading...")
        self.youtube_spinner.grid()

        # Create a thread to perform the download
        download_thread = threading.Thread(target=self._download_video, args=(url, download_location, format_choice))
        download_thread.start()

    def _download_video(self, url, download_location, format_choice):
        try:
            ydl_opts = {
                'outtmpl': os.path.join(download_location, '%(title)s.%(ext)s'),
                'format': 'best' if format_choice == 'video' else 'bestaudio',
                'noplaylist': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }] if format_choice == 'audio' else [],
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.youtube_status_label.configure(text="Download completed!")
        except Exception as e:
            self.youtube_status_label.configure(text=f"Error: {str(e)}")
        finally:
            self.youtube_spinner.grid_forget()

    def show_home_screen(self):
        self.tabview.set("Home")

    def open_video_converter(self):
        self.tabview.set("Video Conversion")

    def open_youtube_downloader(self):
        self.tabview.set("YouTube Downloader")

if __name__ == "__main__":
    root = ctk.CTk()
    app = VideoConverterApp(root)
    root.mainloop()