import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread
import os
from PIL import Image, ImageTk
import customtkinter as ctk

class VideoConverterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Red Halo Converter")
        self.root.geometry("900x900")
        self.root.resizable(False, False)
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
        self.audio_tab = self.tabview.add("Audio Conversion")

        # Setup Tabs
        self.setup_home_tab()
        self.setup_video_tab()
        self.setup_audio_tab()

    def setup_home_tab(self):
        self.home_tab.grid_columnconfigure(0, weight=1)
        self.home_tab.grid_rowconfigure(0, weight=1)
        self.home_tab.grid_rowconfigure(1, weight=1)

        # Add logo
        logo_label = tk.Label(self.home_tab, image=self.logo, bg="#333333")
        logo_label.grid(row=0, column=0, columnspan=1, pady=30)

        title_label = ctk.CTkLabel(self.home_tab, text="Red Halo Converter", font=("Arial", 30, "bold"), text_color="#FFFFFF")
        title_label.grid(row=1, column=0, pady=40, padx=20)

        video_button = ctk.CTkButton(self.home_tab, text="Video Converter", command=self.open_video_converter, 
                                    fg_color="#E53935", hover_color="#D32F2F", text_color="#FFFFFF", font=("Arial", 18, "bold"))
        video_button.grid(row=2, column=0, pady=20, padx=20, ipadx=10, ipady=10)

        audio_button = ctk.CTkButton(self.home_tab, text="Audio Converter", command=self.open_audio_converter, 
                                    fg_color="#E53935", hover_color="#D32F2F", text_color="#FFFFFF", font=("Arial", 18, "bold"))
        audio_button.grid(row=3, column=0, pady=20, padx=20, ipadx=10, ipady=10)

    def setup_video_tab(self):
        self.video_tab.grid_columnconfigure(0, weight=1)
        self.video_tab.grid_columnconfigure(1, weight=2)
        self.video_tab.grid_rowconfigure(0, weight=1)
        self.video_tab.grid_rowconfigure(1, weight=1)
        self.video_tab.grid_rowconfigure(2, weight=1)
        self.video_tab.grid_rowconfigure(3, weight=1)
        self.video_tab.grid_rowconfigure(4, weight=1)
        self.video_tab.grid_rowconfigure(5, weight=1)
        self.video_tab.grid_rowconfigure(6, weight=1)
        self.video_tab.grid_rowconfigure(7, weight=1)
        self.video_tab.grid_rowconfigure(8, weight=1)
        self.video_tab.grid_rowconfigure(9, weight=1)

        # Add logo
        logo_label = tk.Label(self.video_tab, image=self.logo, bg="#333333")
        logo_label.grid(row=0, column=0, columnspan=3, pady=30)

        title_label = ctk.CTkLabel(self.video_tab, text="Video Converter", font=("Arial", 30, "bold"), text_color="#FFFFFF")
        title_label.grid(row=1, column=0, columnspan=3, pady=20)

        # Input file
        self._create_file_selector(self.video_tab, "Input File:", 2, self.select_input_file)

        # Output folder
        self._create_file_selector(self.video_tab, "Output Folder:", 3, self.select_output_folder)

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
        self.create_rounded_button(self.video_tab, "Convert", self.start_conversion, row=6, column=1, font=("Arial", 20, "bold"), button_height=50, button_width=200)

        # Status label and spinner
        self.status_label = ctk.CTkLabel(self.video_tab, text="", font=("Arial", 20), text_color="#FFFFFF")
        self.status_label.grid(row=7, column=0, columnspan=3, pady=15, sticky='n')
        self.spinner = ctk.CTkLabel(self.video_tab, text="", font=("Arial", 36), text_color="#FFFFFF")
        self.spinner.grid(row=8, column=0, columnspan=3, pady=15, sticky='n')

        # Spinner animation
        self.spinner_sequence = ["|", "/", "-", "\\"]
        self.spinner_index = 0

        # Add Back button
        back_button = ctk.CTkButton(self.video_tab, text="Back", command=self.show_home_screen, 
                                    fg_color="#E53935", hover_color="#D32F2F", text_color="#FFFFFF", font=("Arial", 20, "bold"), width=200, height=50)
        back_button.grid(row=9, column=0, padx=20, pady=20, sticky='w')

    def setup_audio_tab(self):
        self.audio_tab.grid_columnconfigure(0, weight=1)
        self.audio_tab.grid_rowconfigure(0, weight=1)
        self.audio_tab.grid_rowconfigure(1, weight=1)

        # Add logo
        logo_label = tk.Label(self.audio_tab, image=self.logo, bg="#333333")
        logo_label.grid(row=0, column=0, columnspan=1, pady=30)

        title_label = ctk.CTkLabel(self.audio_tab, text="Audio Converter", font=("Arial", 30, "bold"), text_color="#FFFFFF")
        title_label.grid(row=1, column=0, pady=30, padx=20)

        # Placeholder label for audio functionality
        ctk.CTkLabel(self.audio_tab, text="Audio Conversion functionality will be implemented here.", 
                     font=("Arial", 18), text_color="#FFFFFF").grid(row=2, column=0, pady=30, padx=20)

        # Add Back button
        back_button = ctk.CTkButton(self.audio_tab, text="Back", command=self.show_home_screen, 
                                    fg_color="#E53935", hover_color="#D32F2F", text_color="#FFFFFF", font=("Arial", 18, "bold"))
        back_button.grid(row=3, column=0, pady=30, padx=20)

    def _create_file_selector(self, tab, label_text, row, command):
        ctk.CTkLabel(tab, text=label_text, font=("Arial", 20), text_color="#FFFFFF").grid(row=row, column=0, padx=20, pady=15, sticky='e')

        # Label to display file or folder path
        path_label = ctk.CTkLabel(tab, text="No file selected", font=("Arial", 20), fg_color="#FFFFFF", text_color="#000000")
        path_label.grid(row=row, column=1, padx=20, pady=15, sticky='ew')

        # Select button
        self.create_rounded_button(tab, "Select", command, row=row, column=2, font=("Arial", 20, "bold"), button_height=40, button_width=100)

        # Store the path label as an attribute
        if label_text.startswith("Input"):
            self.input_file_label = path_label
        elif label_text.startswith("Output"):
            self.output_folder_label = path_label

    def create_rounded_button(self, parent, text, command, row, column, font=("Arial", 20), button_height=50, button_width=150):
        button = ctk.CTkButton(parent, text=text, command=command, fg_color="#E53935", hover_color="#D32F2F", text_color="#FFFFFF", font=font, width=button_width, height=button_height)
        button.grid(row=row, column=column, padx=20, pady=15, sticky='ew')

    def select_input_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mov")])
        if file_path:
            self.input_file_label.configure(text=file_path)

    def select_output_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_folder_label.configure(text=folder_path)

    def start_conversion(self):
        input_file = self.input_file_label.cget("text")
        output_folder = self.output_folder_label.cget("text")
        output_file_name = self.output_file_name_entry.get()
        output_format = self.format_var.get()

        if not input_file or not output_folder or not output_file_name:
            messagebox.showerror("Error", "Please select input file, output folder, and provide output file name.")
            return

        output_file_path = os.path.join(output_folder, f"{output_file_name}.{output_format}")

        # Start conversion in a separate thread to avoid blocking the UI
        conversion_thread = Thread(target=self.convert_video, args=(input_file, output_file_path))
        conversion_thread.start()

    def convert_video(self, input_file, output_file_path):
        self.update_status("Converting...")
        try:
            cap = cv2.VideoCapture(input_file)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)

            # Use mp4v codec for better compatibility
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_file_path, fourcc, fps, (width, height))

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                out.write(frame)

            cap.release()
            out.release()
            self.update_status("Conversion Complete!")
        except Exception as e:
            self.update_status(f"Error: {str(e)}")

    def update_status(self, message):
        self.status_label.configure(text=message)

    def show_home_screen(self):
        self.tabview.set("Home")

    def open_video_converter(self):
        self.tabview.set("Video Conversion")

    def open_audio_converter(self):
        self.tabview.set("Audio Conversion")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoConverterApp(root)
    root.mainloop()
