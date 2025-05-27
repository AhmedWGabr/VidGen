"""
Reusable UI components for VidGen gradio interface

This module provides reusable UI components and utilities for the Gradio interface.
"""

import gradio as gr

def create_script_input_area():
    """Create the script input area with text field and settings"""
    with gr.Column():
        script_input = gr.Textbox(
            label="Enter General Scene Script", 
            lines=10, 
            placeholder="Describe your scene..."
        )
        api_key_input = gr.Textbox(
            label="Google Gemini API Key", 
            type="password"
        )
        segment_duration_slider = gr.Slider(
            label="Segment Duration (seconds)", 
            minimum=2, 
            maximum=30, 
            value=5, 
            step=1
        )
        seed_input = gr.Number(
            label="Seed (for reproducibility)", 
            value=42, 
            precision=0
        )
        generate_btn = gr.Button("Generate Video")
    
    return script_input, api_key_input, segment_duration_slider, seed_input, generate_btn

def create_output_display_tabs():
    """Create output display tabs for generated content"""
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
    
    return (
        detailed_script_box,
        parsed_box,
        tts_audio_gallery,
        image_gallery,
        video_gallery,
        bg_audio_gallery,
        final_video_box
    )
