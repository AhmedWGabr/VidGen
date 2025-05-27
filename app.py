import gradio as gr
import requests
from agent import parse_detailed_script
from models import (
    generate_video_segment,
    generate_tts_audio,
    generate_background_audio,
    generate_character_image,
)
from assemble import assemble_video

def call_gemini_api(script, api_key, segment_duration=5):
    """
    Calls Gemini API (gemini-2.0-flash-001) with a structured prompt to control output.
    Requests timestamps and segment durations.
    """
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash-001:generateContent"
    headers = {
        "Content-Type": "application/json"
    }
    params = {
        "key": api_key
    }
    prompt = (
        f"Expand the following scene script into a detailed, timestamped breakdown for video generation. "
        f"Divide the script into segments of approximately {segment_duration} seconds each. "
        f"For each segment, provide:\n"
        f"- Start and end timestamps\n"
        f"- Scene description\n"
        f"- Narration/dialogue\n"
        f"- Background audio/music\n"
        f"- Visual/motion details\n"
        f"- Character face/image description\n\n"
        f"Output as a JSON list, one object per segment, with keys: start, end, scene, narration, audio, visual, image.\n\n"
        f"Script:\n{script}"
    )
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    response = requests.post(url, headers=headers, params=params, json=data)
    if response.status_code == 200:
        result = response.json()
        try:
            return result["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            return "Failed to parse Gemini response."
    else:
        return f"Gemini API error: {response.status_code} {response.text}"

def generate_video(script, gemini_api_key, segment_duration, seed):
    if not script or not gemini_api_key:
        return [None] * 7
    detailed_script = call_gemini_api(script, gemini_api_key, segment_duration)
    parsed = parse_detailed_script(detailed_script)

    face_cache = {}
    video_segments = [generate_video_segment(cmd, face_cache=face_cache, default_duration=segment_duration) for cmd in parsed["video"]]
    tts_audios = [generate_tts_audio(cmd) for cmd in parsed["tts"]]
    background_audios = [generate_background_audio(cmd) for cmd in parsed["audio"]]
    character_images = [generate_character_image(cmd, seed=seed) for cmd in parsed["image"]]

    final_video_path = assemble_video(video_segments, tts_audios, background_audios, character_images)

    return (
        detailed_script,
        str(parsed),
        tts_audios,
        character_images,
        video_segments,
        background_audios,
        final_video_path
    )

with gr.Blocks() as demo:
    gr.Markdown("# Video Generator from Scene Script")
    script_input = gr.Textbox(label="Enter General Scene Script", lines=10, placeholder="Describe your scene...")
    api_key_input = gr.Textbox(label="Google Gemini API Key", type="password")
    segment_duration_slider = gr.Slider(label="Segment Duration (seconds)", minimum=2, maximum=30, value=5, step=1)
    seed_input = gr.Number(label="Seed (for reproducibility)", value=42, precision=0)
    generate_btn = gr.Button("Generate Video")

    with gr.Tabs():
        with gr.TabItem("Detailed Script"):
            detailed_script_box = gr.Textbox(label="Detailed Script")
        with gr.TabItem("Parsed Commands"):
            parsed_box = gr.Textbox(label="Parsed Commands")
        with gr.TabItem("Generated Audio"):
            tts_audio_gallery = gr.Gallery(label="TTS Audio Files")
        with gr.TabItem("Generated Images"):
            image_gallery = gr.Gallery(label="Character Images")
        with gr.TabItem("Video Segments"):
            video_gallery = gr.Gallery(label="Video Segments")
        with gr.TabItem("Background Audio"):
            bg_audio_gallery = gr.Gallery(label="Background Audios")
        with gr.TabItem("Final Video Path"):
            final_video_box = gr.Textbox(label="Final Video Path")

    generate_btn.click(
        fn=generate_video,
        inputs=[script_input, api_key_input, segment_duration_slider, seed_input],
        outputs=[
            detailed_script_box,
            parsed_box,
            tts_audio_gallery,
            image_gallery,
            video_gallery,
            bg_audio_gallery,
            final_video_box
        ]
    )

if __name__ == "__main__":
    demo.launch()
