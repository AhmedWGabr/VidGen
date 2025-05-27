# VidGen Examples

This document provides practical examples of how to use VidGen for various video generation tasks, from simple scripts to advanced customizations.

## Getting Started

### 1. Using the Command Line Interface

The simplest way to use VidGen is through the command line interface:

```bash
# Generate a video from a script file
python -m vidgen.main --script path/to/script.txt --output my_video.mp4

# Generate with specific settings
python -m vidgen.main --script path/to/script.txt --duration 5 --seed 42 --api-key YOUR_API_KEY
```

### 2. Using the Gradio Web Interface

For a visual interface, VidGen provides a Gradio-based web UI:

```bash
# Start the web interface
python -m vidgen.ui
```

This will open a browser window where you can:
1. Enter your scene script in the text area
2. Configure generation parameters (API key, duration, seed)
3. Preview generated segments in real-time
4. Download the final video when complete

### 3. Using the Python API

For programmatic usage and integration into your own applications:

```python
from vidgen.main import generate_video
from vidgen.core.config import VideoGenConfig

# Configure global settings
VideoGenConfig.OUTPUT_DIR = "my_custom_output_folder"
VideoGenConfig.STABLE_DIFFUSION_MODEL = "runwayml/stable-diffusion-v1-5"

# Load script from a file
with open("scripts/nature_documentary.txt", "r") as f:
    script = f.read()

# Generate the video
output_paths = generate_video(
    script=script,
    gemini_api_key="YOUR_API_KEY",
    segment_duration=5,
    seed=42,
    output_filename="nature_documentary.mp4"
)

# output_paths contains paths to all generated assets:
# - output_paths['video']: Final video path
# - output_paths['images']: Generated image paths
# - output_paths['audio']: Generated audio paths
```

## Script Examples

### 1. Educational Video

```
Title: "The Quantum World"

Open with an abstract visualization of atoms and quantum particles.
[Background: Subtle electronic ambient music]

NARRATOR: "Welcome to the quantum world, where the rules of classical physics break down."

Show a comparison between a classical billiard ball collision and quantum particle interaction.
[Background: Same ambient music continues quietly]

NARRATOR: "Unlike macroscopic objects that follow predictable paths, quantum particles exist in states of probability."

Visualization of the Schrödinger equation and wave functions.

NARRATOR: "The Schrödinger equation describes how these probability waves evolve over time."

Show the double-slit experiment with particles creating an interference pattern.

NARRATOR: "In the famous double-slit experiment, particles somehow pass through both slits simultaneously."

Close-up of quantum computers with glowing circuits.

NARRATOR: "These strange properties are now being harnessed in quantum computers, promising computational power beyond anything possible today."
```

### 2. Product Showcase

```
Title: "Introducing the EcoTech Smart Home System"

Start with a modern, minimalist home exterior.
[Background: Soft, uplifting instrumental music]

PRESENTER (Sarah): "Home automation reimagined with sustainability at its core."

Pan to show solar panels on the roof connecting to the home system.
[Background: Continue soft music]

PRESENTER (Sarah): "The EcoTech system intelligently balances energy harvesting with consumption, reducing your carbon footprint without sacrificing comfort."

Show a person using the smartphone app to control home features.

PRESENTER (Sarah): "Control everything from lighting to climate with our intuitive app, designed to make sustainable living effortless."

Display the central hub device with its soft blue glow.

PRESENTER (Sarah): "The heart of the system is our AI-powered hub, which learns your preferences while optimizing energy usage."

Show various rooms adapting automatically as a person moves through the house.

PRESENTER (Sarah): "Experience a home that responds to your needs while respecting our planet's limited resources."
```

### 3. Travel Vlog Style

```
Title: "Hidden Gems of Kyoto"

Open with a timelapse of sunrise over Kyoto's skyline, temples visible in the distance.
[Background: Traditional Japanese flute music]

VLOGGER (Alex): "Ohayou gozaimasu! Welcome to day three of our Kyoto adventure."

Walking shot through a narrow alleyway lined with traditional wooden buildings.
[Background: Ambient street sounds]

VLOGGER (Alex): "I'm heading to a local tea house that my friend Takeshi recommended - supposedly it's been operated by the same family for seven generations!"

Interior shot of a traditional tea house, minimalist aesthetic with tatami mats.
[Background: Soft sounds of water and ceramics]

VLOGGER (Alex): "The attention to detail in the tea ceremony is incredible. Every movement has meaning, developed over centuries of tradition."

Close-up of matcha tea being prepared with a bamboo whisk.

VLOGGER (Alex): "You can really taste the difference when the matcha is prepared this way - it's earthy but slightly sweet, with none of the bitterness you might expect."
```

## Advanced Usage Examples

### 1. Component-Level Control

For more precise control, you can use VidGen's components directly:

```python
import json
from vidgen.services.gemini_api import call_gemini_api
from vidgen.services.script_parser import parse_detailed_script
from vidgen.models.video import generate_video_segment
from vidgen.models.tts import generate_tts_audio
from vidgen.models.image import generate_character_image
from vidgen.services.video_assembler import assemble_video

# 1. Generate detailed script
script = "A short story about space exploration."
detailed_script_json = call_gemini_api(script, api_key="YOUR_API_KEY", segment_duration=5)

# 2. Parse the script into components
parsed = parse_detailed_script(detailed_script_json)

# 3. Generate character images first (for consistency)
character_images = []
for img_cmd in parsed["image"]:
    image_path = generate_character_image(
        img_cmd["face_prompt"], 
        seed=img_cmd["seed"]
    )
    character_images.append(image_path)

# 4. Generate TTS audio for each narration
tts_audio_paths = []
for narration in parsed["tts"]:
    audio_path = generate_tts_audio(narration)
    tts_audio_paths.append(audio_path)

# 5. Generate video segments with face consistency
face_cache = {}  # Ensures character face consistency
video_segments = []
for cmd in parsed["video"]:
    segment = generate_video_segment(cmd, face_cache=face_cache)
    video_segments.append(segment)

# 6. Assemble the final video
output_path = assemble_video(
    video_segments=video_segments,
    tts_audios=tts_audio_paths,
    background_audios=parsed["audio"],
    character_images=character_images,
    output_file="custom_assembly.mp4"
)

print(f"Video generated at: {output_path}")
```

### 2. Custom Scene Transitions

Adding custom transitions between scenes:

```python
from vidgen.services.video_assembler import assemble_video_with_transitions

# After generating your video segments
output_path = assemble_video_with_transitions(
    video_segments=video_segments,
    tts_audios=tts_audio_paths,
    transitions=[
        "fade",         # Fade transition between segments 1-2
        "dissolve",     # Dissolve transition between segments 2-3
        "wipe_left",    # Wipe transition between segments 3-4
        "zoom"          # Zoom transition between segments 4-5
    ],
    transition_duration=1.0  # 1 second transitions
)
```

### 3. Batch Processing with Progress Reporting

Process multiple scripts with progress reporting:

```python
import os
from vidgen.main import generate_video
from tqdm import tqdm

# Directory with script files
scripts_dir = "data/scripts"
output_dir = "outputs/batch_results"
os.makedirs(output_dir, exist_ok=True)

# Get all script files
script_files = [f for f in os.listdir(scripts_dir) if f.endswith(".txt")]

# Process with progress bar
for script_file in tqdm(script_files, desc="Processing videos"):
    script_path = os.path.join(scripts_dir, script_file)
    
    # Read script
    with open(script_path, "r") as f:
        script = f.read()
    
    # Generate video
    output_name = os.path.splitext(script_file)[0] + ".mp4"
    output_path = os.path.join(output_dir, output_name)
    
    try:
        result = generate_video(
            script=script,
            gemini_api_key="YOUR_API_KEY",
            segment_duration=5,
            seed=42,
            output_filename=output_path
        )
        tqdm.write(f"✓ {script_file}")
    except Exception as e:
        tqdm.write(f"✗ {script_file}: {e}")
```

### 4. Custom Model Integration

Using a different image generation model:

```python
from vidgen.core.config import VideoGenConfig
from vidgen.models.image import get_image_pipeline, generate_character_image

# Configure VidGen to use a different model
VideoGenConfig.STABLE_DIFFUSION_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"

# Now your character generations will use the specified model
character_image = generate_character_image(
    "A futuristic robot assistant with sleek white casing and blue glowing eyes",
    seed=123
)
```

### 5. Creating an Interactive Application

Example of creating a simple Streamlit app with VidGen:

```python
# Save this as app.py
import streamlit as st
from vidgen.main import generate_video

st.title("VidGen Video Creator")

# Input area for script
script = st.text_area("Enter your video script:", height=200)

# Configuration sidebar
with st.sidebar:
    st.header("Video Settings")
    api_key = st.text_input("Gemini API Key:", type="password")
    duration = st.slider("Segment Duration (seconds):", 3, 10, 5)
    seed = st.number_input("Random Seed:", value=42)

# Generate button
if st.button("Generate Video") and script and api_key:
    with st.spinner("Generating your video..."):
        try:
            result = generate_video(
                script=script,
                gemini_api_key=api_key,
                segment_duration=duration,
                seed=seed
            )
            # Show the video
            st.success("Video generated successfully!")
            st.video(result['video'])
            st.download_button(
                "Download Video", 
                open(result['video'], 'rb').read(), 
                file_name="generated_video.mp4"
            )
        except Exception as e:
            st.error(f"Error generating video: {e}")
```

Run with:
```bash
pip install streamlit
streamlit run app.py
```
