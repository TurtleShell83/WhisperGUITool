Whisper GUI Tool:

This is a Python script that provides a graphical user interface (GUI) for using the Whisper speech recognition and translation tool. It allows users to select an audio or video file, choose a Whisper model and task (transcribe or translate), and specify an output directory. The script then processes the file using Whisper and generates transcriptions or translations in the selected output directory.

Prerequisites:

To use this script, you need to have the following:

Python 3.x installed on your system
Whisper tool installed and accessible from the command line
FFmpeg installed and accessible from the command line (for embedding subtitles in the output video)

Installation:

1. Clone or download this repository to your local machine.
2. Install the required Python libraries by running the following command:

pip install tkinter subprocess os logging shutil datetime

3. Modify the whisper_gui_1_4.py file to specify the correct path to the Whisper executable on your system. Update the following line with the appropriate path:

"/home/keys/.local/bin/whisper"  # Replace with the actual path to the whisper executable

Usage:

1. Open a terminal or command prompt and navigate to the directory where the whisper_gui_1_4.py file is located.
2 Run the script using the following command:

python3 whisper_gui_1_4.py

3. The Whisper GUI Tool window will appear.
4. Select the desired Whisper model from the dropdown menu (default is "base").
5. Choose the task (transcribe or translate) using the radio buttons.
6. Click on the "Select Source File" button to choose the audio or video file you want to process.
7. Click on the "Select Output Directory" button to specify the directory where the transcriptions or translations will be saved.
8. Click the "Start" button to begin processing the file.
9. The progress will be displayed in the GUI, and upon completion, a success message will be shown.
10. The transcriptions or translations will be saved in the specified output directory, along with the original input file and a video file with embedded subtitles (if applicable).

Logging:

The script logs information and errors to a file named whisper_gui.log in the same directory as the script. You can view this file to troubleshoot any issues that may occur during the execution of the script.

License:

This project is licensed under the MIT License.

Feedback and Questions:

I would love to hear your CONSTRUCTIVE thoughts, feedback, or any questions you may have about this script! If you have any suggestions for improvements, encountered any issues, or just want to share your experience using the tool, please don't hesitate to reach out to me. You can find me on Twitter @TurtleShell83. Feel free to send me a direct message or mention me in a tweet.

