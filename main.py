import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from threading import Thread
import os
from PIL import Image, ImageTk
import customtkinter as ctk
from queue import Queue

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

        # Task queue
        self.task_queue = Queue()

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
        self.create_rounded_button(self.video_tab, "Convert", self.add_conversion_task, row=6, column=1, font=("Arial", 20, "bold"), button_height=50, button_width=200)

        # Status label and spinner
        self.status_label = ctk.CTkLabel(self.video_tab, text="", font=("Arial", 20), text_color="#FFFFFF")
        self.status_label.grid(row=7, column=0, columnspan=3, pady=15, sticky='n')

        # Add Back button
        back_button = ctk.CTkButton(self.video_tab, text="Back", command=self.show_home_screen, 
                                    fg_color="#E53935", hover_color="#D32F2F", text_color="#FFFFFF", font=("Arial", 20, "bold"), width=200, height=50)
        back_button.grid(row=9, column=0, padx=20, pady=20, sticky='w')

        # Task list
        self.task_list = ctk.CTkLabel(self.video_tab, text="", font=("Arial", 16), text_color="#FFFFFF", justify="left")
        self.task_list.grid(row=8, column=0, columnspan=3, pady=15, sticky='n')

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
        else:
            self.output_folder_label = path_label

    def create_rounded_button(self, parent, text, command, row, column, font, button_height, button_width):
        button = ctk.CTkButton(parent, text=text, command=command, font=font, fg_color="#E53935", hover_color="#D32F2F", text_color="#FFFFFF", corner_radius=15, width=button_width, height=button_height)
        button.grid(row=row, column=column, pady=10, padx=10, sticky='ew')
        return button

    def show_home_screen(self):
        self.tabview.set("Home")

    def open_video_converter(self):
        self.tabview.set("Video Conversion")

    def open_audio_converter(self):
        self.tabview.set("Audio Conversion")

    def select_input_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.avi *.mov"), ("All Files", "*.*")])
        if file_path:
            self.input_file_label.configure(text=file_path)

    def select_output_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_folder_label.configure(text=folder_path)

    def add_conversion_task(self):
        input_file = self.input_file_label.cget("text")
        output_folder = self.output_folder_label.cget("text")
        output_file_name = self.output_file_name_entry.get().strip()
        format = self.format_var.get()

        if input_file == "No file selected" or not os.path.isfile(input_file):
            messagebox.showerror("Error", "Please select a valid input file.")
            return

        if output_folder == "No file selected" or not os.path.isdir(output_folder):
            messagebox.showerror("Error", "Please select a valid output folder.")
            return

        if not output_file_name:
            messagebox.showerror("Error", "Please enter a valid output file name.")
            return

        # Add task to the queue
        self.task_queue.put((input_file, output_folder, output_file_name, format))
        self.update_task_list()
        self.start_conversion_thread()

    def update_task_list(self):
        tasks = list(self.task_queue.queue)
        task_display = "\n".join([f"Task {i+1}: {task[2]}.{task[3]}" for i, task in enumerate(tasks)])
        self.task_list.configure(text=f"Pending Tasks:\n{task_display}")

    def start_conversion_thread(self):
        if not self.task_queue.empty():
            task = self.task_queue.get()
            Thread(target=self.convert_video, args=task).start()

    def convert_video(self, input_file, output_folder, output_file_name, format):
        self.status_label.configure(text="Converting...")
        output_file = os.path.join(output_folder, f"{output_file_name}.{format}")

        # Video conversion logic
        cap = cv2.VideoCapture(input_file)
        fourcc = cv2.VideoWriter_fourcc(*'XVID' if format == 'avi' else 'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, 30.0, (int(cap.get(3)), int(cap.get(4))))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            out.write(frame)

        cap.release()
        out.release()

        self.status_label.configure(text=f"Conversion completed: {output_file_name}.{format}")

        # Update task list
        self.update_task_list()

        # Start next task if available
        self.start_conversion_thread()

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoConverterApp(root)
    root.mainloop()
