import gradio as gr
from vidgen.main import generate_video

def create_gradio_interface():
    """Create and return the Gradio interface for VidGen"""
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

    return demo
