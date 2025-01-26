import streamlit as st
import subprocess
import os
from gtts import gTTS
import uuid

# ----------------------------------------------------------------------------
# Paths: Adjust these to match your system
# ----------------------------------------------------------------------------
WAV2LIP_DIR = os.path.join(os.getcwd(), "Wav2Lip")  # Where you cloned Wav2Lip
CHECKPOINT_PATH = os.path.join(WAV2LIP_DIR, "checkpoints", "wav2lip_gan.pth")

def generate_talking_head(script_text: str, face_image_path: str) -> str:
    """
    1) Convert 'script_text' to TTS audio (temp.wav).
    2) Call Wav2Lip's inference.py (via subprocess) to lip-sync the face image.
    3) Return the path to the final MP4 video or None if something fails.
    """

    # Make sure the Wav2Lip checkpoint exists
    if not os.path.isfile(CHECKPOINT_PATH):
        st.error("Wav2Lip checkpoint not found. Please download wav2lip_gan.pth.")
        return None

    # Generate unique filenames for output
    output_video = f"output_{uuid.uuid4().hex[:6]}.mp4"
    audio_path = f"temp_{uuid.uuid4().hex[:6]}.wav"

    # -------------------------
    # Step 1: Generate TTS audio
    # -------------------------
    try:
        tts = gTTS(script_text, lang="en")
        tts.save(audio_path)
    except Exception as e:
        st.error(f"Failed to generate TTS audio: {e}")
        return None

    # -----------------------------------------------
    # Step 2: Run Wav2Lip's inference to do lip-sync
    # -----------------------------------------------
    inference_script = os.path.join(WAV2LIP_DIR, "inference.py")

    command = [
        "python",  # or "python3"
        inference_script,
        "--checkpoint_path", CHECKPOINT_PATH,
        "--face", face_image_path,
        "--audio", audio_path,
        "--outfile", output_video,
        "--static", "True"  # "True" or "1" if needed
    ]

    st.info("Running Wav2Lip. This can take a while, especially on CPU...")

    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        st.error(f"Wav2Lip inference failed: {e}")
        return None
    finally:
        # Clean up the temporary audio file
        if os.path.exists(audio_path):
            os.remove(audio_path)

    if os.path.isfile(output_video):
        return output_video
    else:
        st.error("Wav2Lip finished but no output video found.")
        return None

# ----------------------------------------------------------------------------
# Streamlit UI
# ----------------------------------------------------------------------------
st.set_page_config(page_title="Open-Source AI News Anchor", layout="centered")
st.title("Open-Source AI News Anchor with Wav2Lip")

st.markdown("""
**Welcome!** This app takes your input text and a face image, then generates a talking head video using:
- **[gTTS](https://pypi.org/project/gTTS/) for Text-to-Speech**  
- **[Wav2Lip](https://github.com/Rudrabha/Wav2Lip) for lip-sync**  

**Requirements**:
- A local clone of Wav2Lip with the `wav2lip_gan.pth` checkpoint.
- This code **will not** run on Streamlit Cloud (free) unless you have a GPU environment & large timeouts.
- On CPU, it might be **very slow** for longer scripts.

**Instructions**:
1. Enter your script text below.
2. Upload a clear front-facing image for the anchor's face.
3. Click "Generate Video" to see the result.
""")

# Input area for script text
script_text = st.text_area(
    "Enter the news or any script you'd like the anchor to speak:",
    value="Hello, I'm your AI News Anchor. Welcome to today's program!"
)

# File uploader for face image
uploaded_image = st.file_uploader("Upload a front-facing image of the anchor:", type=["jpg", "jpeg", "png"])

# Generate button
if st.button("Generate Video"):
    if not script_text.strip():
        st.warning("Please enter some text for the anchor to speak.")
    elif not uploaded_image:
        st.warning("Please upload a face image.")
    else:
        # Save the uploaded image to a temporary file
        face_image_path = f"face_{uuid.uuid4().hex[:6]}.png"
        with open(face_image_path, "wb") as f:
            f.write(uploaded_image.read())

        with st.spinner("Generating your AI anchor video..."):
            result_path = generate_talking_head(script_text, face_image_path)

        # Clean up the face image after use
        if os.path.exists(face_image_path):
            os.remove(face_image_path)

        # Display the video if successful
        if result_path:
            st.success("Video generated successfully!")
            st.video(result_path)
