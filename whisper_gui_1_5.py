import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import subprocess
import os
import logging
import shutil
import datetime

class WhisperGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Jack's Whisper GUI Tool")
        self.root.geometry("500x400")

        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            filename='whisper_gui.log',
            filemode='a'
        )

        # Model selection with a default value
        self.model_var = tk.StringVar(value="base")
        models = ["tiny", "base", "small", "medium", "large"]
        ttk.Label(root, text="Select Model:").pack()
        self.model_dropdown = ttk.Combobox(root, textvariable=self.model_var, values=models, state="readonly")
        self.model_dropdown.pack()
        self.model_dropdown.current(1)  # Automatically select 'base' model as default

        # Task selection
        self.task_var = tk.StringVar(value="transcribe")
        ttk.Label(root, text="Task:").pack()
        self.task_radio_transcribe = ttk.Radiobutton(root, text="Transcribe", variable=self.task_var, value="transcribe")
        self.task_radio_transcribe.pack()
        self.task_radio_translate = ttk.Radiobutton(root, text="Translate", variable=self.task_var, value="translate")
        self.task_radio_translate.pack()

        # File selection
        ttk.Button(root, text="Select Source File", command=self.select_source_file).pack()
        self.source_file_label = ttk.Label(root, text="No file selected")
        self.source_file_label.pack()

        # Output destination
        ttk.Button(root, text="Select Output Directory", command=self.select_output_directory).pack()
        self.output_directory_label = ttk.Label(root, text="No directory selected")
        self.output_directory_label.pack()

        # Checkbox for lower resolution output
        self.low_res_var = tk.BooleanVar(value=False)
        self.low_res_check = ttk.Checkbutton(root, text="Output Lower Resolution for Email", variable=self.low_res_var)
        self.low_res_check.pack()

        # Start button
        ttk.Button(root, text="Start", command=self.start_operation).pack()

        # Progress label
        self.progress_label = ttk.Label(root, text="")
        self.progress_label.pack()

        # File paths
        self.source_file_path = ""
        self.output_directory = ""

    def select_source_file(self):
        self.source_file_path = filedialog.askopenfilename()
        if self.source_file_path:
            self.source_file_label.config(text=f"Source File: {self.source_file_path}")

    def select_output_directory(self):
        self.output_directory = filedialog.askdirectory()
        if self.output_directory:
            self.output_directory_label.config(text=f"Output Directory: {self.output_directory}")

    def start_operation(self):
        if not self.source_file_path or not self.output_directory:
            messagebox.showerror("Error", "Please select both source file and output directory")
            return

        model = self.model_var.get()
        task = self.task_var.get()

        # Create a dynamically named output folder
        input_video_name = os.path.splitext(os.path.basename(self.source_file_path))[0]
        output_folder = os.path.join(self.output_directory, f"{input_video_name}_Whisper_Output")
        os.makedirs(output_folder, exist_ok=True)

        # Constructing the Whisper command with the full path
        command = [
            "/home/keys/.local/bin/whisper",  # Replace with the actual path to the whisper executable
            self.source_file_path,
            "--model", model,
            "--task", task,
            "--output_dir", output_folder,
        ]

        try:
            self.progress_label.config(text="Processing...")
            self.root.update()
            subprocess.run(command, check=True, shell=False)

            # Copy the input video file to the output folder
            output_video_path = os.path.join(output_folder, os.path.basename(self.source_file_path))
            shutil.copy2(self.source_file_path, output_video_path)

            # Generate video with embedded subtitles
            subtitle_file = os.path.join(output_folder, os.path.splitext(os.path.basename(self.source_file_path))[0] + ".srt")
            current_datetime = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            output_video = os.path.join(output_folder, f"WhisperOutput_{current_datetime}.mp4")

            logging.info(f"Subtitle file: {subtitle_file}")

            if os.path.isfile(subtitle_file):
                if self.low_res_var.get():
                    ffmpeg_command = [
                        "ffmpeg",
                        "-i", output_video_path,
                        "-vf", f"subtitles={subtitle_file},scale=854:-1",  # Scale video to 480p width, maintain aspect ratio
                        "-b:v", "1000k",  # Lower bitrate
                        "-c:a", "aac",
                        "-c:v", "libx264",
                        "-pix_fmt", "yuv420p",
                        "-shortest",
                        output_video
                    ]
                else:
                    ffmpeg_command = [
                        "ffmpeg",
                        "-i", output_video_path,
                        "-vf", f"subtitles={subtitle_file}",
                        "-c:a", "aac",
                        "-c:v", "libx264",
                        "-pix_fmt", "yuv420p",
                        "-shortest",
                        output_video
                    ]

                logging.info(f"FFmpeg command: {' '.join(ffmpeg_command)}")

                try:
                    subprocess.run(ffmpeg_command, check=True, shell=False)
                except subprocess.CalledProcessError as e:
                    logging.error(f"Error during FFmpeg execution: {e}")
                    raise

            else:
                logging.warning(f"Subtitle file not found: {subtitle_file}")
                messagebox.showwarning("Warning", "Subtitle file not found. Skipping subtitle embedding.")

            self.progress_label.config(text="")
            messagebox.showinfo("Success", "Operation completed successfully")

        except subprocess.CalledProcessError as e:
            self.progress_label.config(text="")
            logging.error(f"An error occurred: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WhisperGUI(root)
    root.mainloop()
