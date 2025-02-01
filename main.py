import streamlit as st
import subprocess
import os
import uuid
from gtts import gTTS
from io import BytesIO

# ----------------------------------------------------------------------------
# Paths: Adjust these to match your system
# ----------------------------------------------------------------------------
WAV2LIP_DIR = os.path.join(os.getcwd(), "Wav2Lip")  # Where you cloned Wav2Lip
CHECKPOINT_PATH = os.path.join(WAV2LIP_DIR, "checkpoints", "wav2lip_gan.pth")

# ----------------------------------------------------------------------------
# Function: Generate Talking Head Video using Wav2Lip
# ----------------------------------------------------------------------------
def generate_talking_head(script_text: str, face_image_path: str, lang: str = "en", slow: bool = False) -> str:
    """
    1) Convert script_text to TTS audio.
    2) Run Wav2Lip's inference to lip-sync the face image.
    3) Return the path to the final MP4 video.
    """
    if not os.path.isfile(CHECKPOINT_PATH):
        st.error("Wav2Lip checkpoint not found. Please download `wav2lip_gan.pth` and place it in the checkpoints folder.")
        return None

    output_video = f"output_{uuid.uuid4().hex[:6]}.mp4"
    audio_path = f"temp_{uuid.uuid4().hex[:6]}.wav"

    # -------------------------
    # Step 1: Generate TTS Audio
    # -------------------------
    try:
        tts = gTTS(script_text, lang=lang, slow=slow)
        tts.save(audio_path)
    except Exception as e:
        st.error(f"Failed to generate TTS audio: {e}")
        return None

    # -------------------------
    # Step 2: Run Wav2Lip Inference
    # -------------------------
    inference_script = os.path.join(WAV2LIP_DIR, "inference.py")
    command = [
        "python",  # or "python3" if necessary
        inference_script,
        "--checkpoint_path", CHECKPOINT_PATH,
        "--face", face_image_path,
        "--audio", audio_path,
        "--outfile", output_video,
        "--static", "True"  # Assuming a static image input
    ]

    st.info("Running Wav2Lip. This may take a while...")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as e:
        st.error(f"Wav2Lip inference failed: {e}")
        return None
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

    if os.path.isfile(output_video):
        return output_video
    else:
        st.error("Wav2Lip finished but no output video was found.")
        return None

# ----------------------------------------------------------------------------
# Streamlit UI Setup
# ----------------------------------------------------------------------------
st.set_page_config(page_title="AI News Anchor", layout="centered")

# Custom CSS for a clean and appealing look
st.markdown(
    """
    <style>
    /* Hide Streamlit default header and footer */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Background color for the main container */
    .reportview-container {
        background-color: #F9F9F9;
    }
    
    /* Button styling */
    .stButton > button {
        background-color: #2C3E50;
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.6em 1.2em;
        font-size: 1em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Sidebar Settings
# ----------------------------------------------------------------------------
st.sidebar.header("Settings")
# TTS Language selection
language_options = [("English", "en"), ("Spanish", "es"), ("French", "fr"), ("German", "de")]
selected_language = st.sidebar.selectbox(
    "TTS Language", options=language_options, format_func=lambda x: x[0]
)
# TTS slow mode toggle
tts_slow = st.sidebar.checkbox("Slow TTS", value=False)

# ----------------------------------------------------------------------------
# Main UI: Tabs for Generating Video, Instructions, and About
# ----------------------------------------------------------------------------
tabs = st.tabs(["Generate Video", "Instructions", "About"])

# --- Tab 1: Generate Video ---
with tabs[0]:
    st.title("Generate Your AI Talking Head")
    st.markdown("Enter your script and upload a face image below to create your talking head video.")
    
    script_text = st.text_area("Script", value="Hello, I'm your AI News Anchor.", height=150)
    uploaded_image = st.file_uploader("Upload Face Image", type=["jpg", "jpeg", "png"])
    
    col1, col2 = st.columns(2)
    
    # Button to preview TTS audio
    with col1:
        if st.button("Preview TTS Audio"):
            if not script_text.strip():
                st.warning("Please enter some text for the TTS preview.")
            else:
                try:
                    tts = gTTS(script_text, lang=selected_language[1], slow=tts_slow)
                    audio_buffer = BytesIO()
                    tts.write_to_fp(audio_buffer)
                    audio_buffer.seek(0)
                    st.audio(audio_buffer, format="audio/wav")
                except Exception as e:
                    st.error(f"Error generating TTS preview: {e}")
    
    # Button to generate video
    with col2:
        if st.button("Generate Video"):
            if not script_text.strip():
                st.warning("Please enter some text.")
            elif not uploaded_image:
                st.warning("Please upload a face image.")
            else:
                # Save the uploaded image to a temporary file
                face_image_path = f"face_{uuid.uuid4().hex[:6]}.png"
                with open(face_image_path, "wb") as f:
                    f.write(uploaded_image.read())

                with st.spinner("Generating video..."):
                    result_path = generate_talking_head(
                        script_text, face_image_path, lang=selected_language[1], slow=tts_slow
                    )

                # Clean up the temporary face image file
                if os.path.exists(face_image_path):
                    os.remove(face_image_path)

                if result_path:
                    st.success("Video generated successfully!")
                    st.video(result_path)

# --- Tab 2: Instructions ---
with tabs[1]:
    st.header("Instructions")
    st.markdown(
        """
        **Steps to Generate Your Video:**
        
        1. **Enter Script**: Type in the text you want your AI anchor to speak.
        2. **Upload Face Image**: Provide a clear, front-facing image.
        3. **Preview TTS Audio**: (Optional) Listen to the generated TTS audio.
        4. **Generate Video**: Click the button to run the lip-sync process.
        
        **Notes:**
        - Ensure that the Wav2Lip repository is cloned locally and that the `wav2lip_gan.pth` checkpoint is in the correct folder.
        - Video generation may take some time, especially on CPU.
        """
    )

# --- Tab 3: About ---
with tabs[2]:
    st.header("About")
    st.markdown(
        """
        **AI News Anchor** is an open-source project that combines:
        
        - **gTTS**: For generating natural-sounding text-to-speech audio.
        - **Wav2Lip**: For synchronizing lip movements with the audio.
        
        This project demonstrates the potential of combining TTS and lip-syncing technologies to create engaging content.
        
        *Developed by the open-source community with passion and collaboration.*
        """
    )
