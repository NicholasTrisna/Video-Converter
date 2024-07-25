# Red Halo Audio and Video Converter
<img src="https://redhalo.net/Images/logo.png" alt="Red Halo Logo" width="100">

Welcome to the Red Halo Audio and Video Converter! This application allows you to convert audio and video files between various formats with ease.

> [!IMPORTANT]
> The Red Halo Converter is in a pre-alpha state, and only suitable for use by developers

## Features
- Convert audio files to formats like MP3, WAV, AAC, and more.
- Convert video files to formats like MP4, AVI, MOV, and more.
- Batch processing for multiple files.
- Easy-to-use interface built with Tkinter.
- Compatible with Windows.

# Releases
[Versions](https://github.com/NicholasTrisna/Video-Converter/releases)

[Download Version 1.0 LTS [Windows]](https://github.com/NicholasTrisna/Video-Converter/blob/main/dist/Red%20Halo%20Converter.exe)

# Manual Installation
### 1. Clone the Repository

```
git clone https://github.com/NicholasTrisna/Video-Converter.git
cd Video-Converter
```

### 2. Set Up a Virtual Environment

```
python -m venv myenv
```
### 3. Activate the Virtual Environment
- On Windows:
```
myenv\Scripts\activate
```
On macOS/Linux:
```
source myenv/bin/activate
```
### 4. Install Required Packages

```
pip install -r requirements.txt
```
### 4. Download FFmpeg
- Download FFmpeg from FFmpeg Official Site.

- Extract and place the binaries in a known location.

- Update the path in main.py:
```
AudioSegment.converter = r"path_to_ffmpeg\ffmpeg.exe"
```
## Usage
### 1. Run the Application
```
python main.py
```
### 2. Select Files
- Click "Select File" to choose the audio or video file you want to convert.
  
### 3. Choose Output Format
- Select the desired output format from the dropdown menu.
  
### 4. Convert
- Click "Convert" to start the conversion process.
