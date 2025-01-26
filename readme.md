# Wav2Lip News Anchor Project

This project demonstrates a lip-synced video generation system using the Wav2Lip model. The application takes an image of a person (e.g., a news anchor) and synchronizes their lip movements with an input audio file (e.g., text-to-speech output). The result is a realistic video of the person speaking the provided audio.

---

## Features

- **Text-to-Speech Integration**: Generate audio from text using `gTTS` (Google Text-to-Speech).
- **Wav2Lip Lip Synchronization**: Use the Wav2Lip GAN model to create realistic lip-synced videos.
- **Streamlit Interface**: Run the application through a browser-based UI.
- **CPU Compatibility**: Works without requiring a GPU.

---

## Project Structure

```plaintext
News Anchor/
├── Wav2Lip/                 # Wav2Lip source code and related files
│   ├── checkpoints/        # Pretrained models (e.g., wav2lip_gan.pth)
│   ├── face_detection/     # Face detection module
│   ├── inference.py        # Main Wav2Lip inference script
│   └── ...                 # Other files for Wav2Lip
├── env/                    # Virtual environment for dependencies
├── main.py                 # Streamlit application
├── requirements.txt        # Required Python packages
├── temp/                   # Temporary folder for intermediate files
├── face_a99740.png         # Example input image
└── README.md               # Project documentation (this file)
```

---

## Prerequisites

1. **Python 3.7+**
2. **FFmpeg**
   - Install via Homebrew (macOS):
     ```bash
     brew install ffmpeg
     ```
3. **Virtual Environment**
   - Recommended to avoid dependency conflicts.

---

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/aaviix/Open-Source-AI-News-Anchor.git
   cd wav2lip-news-anchor
   ```
2. **Set Up Virtual Environment**:

   ```bash
   python3 -m venv env
   source env/bin/activate  # macOS/Linux
   ```
3. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```
4. **Download Wav2Lip Checkpoints**:

   - Place the pretrained Wav2Lip model (`wav2lip_gan.pth`) in the `checkpoints/` directory.
     ```bash
     mkdir -p Wav2Lip/checkpoints
     mv downloaded_model_path/wav2lip_gan.pth Wav2Lip/checkpoints/
     ```
5. **Create ****\`\`**** Directory**:

   ```bash
   mkdir temp
   ```

---

## Usage

### 1. Run the Streamlit Application

```bash
streamlit run main.py
```

- Local URL: [http://localhost:8501](http://localhost:8501)
- Network URL: Accessible over your network.

### 2. Upload Inputs

- **Input Image**: Upload a photo of a person’s face (e.g., `face_a99740.png`).
- **Input Text**: Enter text to convert into speech (TTS).

### 3. Output

- The app generates a video of the input image lip-synced to the TTS audio.
- The final video is saved in the `temp/` folder.

---

## Troubleshooting

### 1. Missing `ffmpeg` Errors

- Ensure FFmpeg is installed and accessible in the system PATH.
  ```bash
  ffmpeg -version
  ```

### 2. `temp/result.avi` Not Found

- Use the `--static True` flag for single-image input:
  ```bash
  python inference.py \
    --checkpoint_path Wav2Lip/checkpoints/wav2lip_gan.pth \
    --face path/to/your_image.png \
    --audio path/to/your_audio.wav \
    --outfile path/to/result.mp4 \
    --static True
  ```

### 3. SSL Certificate Errors

- Fix SSL certificate verification on macOS:
  ```bash
  /Applications/Python\ 3.x/Install\ Certificates.command
  ```

### 4. Other Dependency Issues

- Ensure all dependencies are installed:
  ```bash
  pip install -r requirements.txt
  ```

---

## Key Notes

- **Pretrained Models**: Ensure `wav2lip_gan.pth` is properly downloaded and placed in the `checkpoints/` directory.
- **TTS Audio Quality**: Modify `gTTS` parameters in `main.py` to adjust language or speed.
- **Intermediate Files**: Use the `temp/` directory to store intermediate results.

---

## Credits

- **Wav2Lip**: [Original Wav2Lip Repository](https://github.com/Rudrabha/Wav2Lip)
- **FFmpeg**: Video processing library.
- **Streamlit**: Interactive web app framework.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## Future Enhancements

- Add GPU acceleration for faster inference.
- Enhance the UI with real-time video preview.
- Support multiple faces in a single image.
