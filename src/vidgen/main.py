import gradio as gr
import asyncio
import logging

from vidgen.services.gemini_api import call_gemini_api
from vidgen.services.script_parser import parse_detailed_script
from vidgen.models.video import generate_video_segment
from vidgen.models.tts import generate_tts_audio
from vidgen.models.audio import generate_background_audio
from vidgen.models.image import generate_character_image
from vidgen.services.video_assembler import assemble_video
from vidgen.core.config import VideoGenConfig
from vidgen.core.exceptions import VidGenError

# Initialize application
VideoGenConfig.ensure_dirs()
VideoGenConfig.configure_logging()
logger = logging.getLogger("VidGen.app")

# Safe wrapper functions for async error handling
def safe_generate_video_segment(cmd, face_cache, segment_duration):
    """Safe wrapper for video segment generation with error handling."""
    try:
        return generate_video_segment(cmd, face_cache, segment_duration)
    except Exception as e:
        logger.error(f"Video segment generation failed for command {cmd}: {e}")
        return None

def safe_generate_tts_audio(cmd):
    """Safe wrapper for TTS audio generation with error handling."""
    try:
        return generate_tts_audio(cmd)
    except Exception as e:
        logger.error(f"TTS audio generation failed for command {cmd}: {e}")
        return None

def safe_generate_background_audio(cmd):
    """Safe wrapper for background audio generation with error handling."""
    try:
        return generate_background_audio(cmd)
    except Exception as e:
        logger.error(f"Background audio generation failed for command {cmd}: {e}")
        return None

def safe_generate_character_image(cmd, seed):
    """Safe wrapper for character image generation with error handling."""
    try:
        return generate_character_image(cmd, seed)
    except Exception as e:
        logger.error(f"Character image generation failed for command {cmd}: {e}")
        return None

def safe_assemble_video(video_segments, tts_audios, background_audios, character_images):
    """Safe wrapper for video assembly with error handling."""
    try:
        return assemble_video(video_segments, tts_audios, background_audios, character_images)
    except Exception as e:
        logger.error(f"Video assembly failed: {e}")
        return None

async def generate_video_async(script, gemini_api_key, segment_duration, seed, progress_callback=None):
    """
    Generate video asynchronously with comprehensive error handling and progress indicators.
    
    Args:
        script (str): Input script text
        gemini_api_key (str): Gemini API key
        segment_duration (int): Duration for each segment
        seed (int): Random seed for reproducibility
        progress_callback (callable): Optional callback for progress updates
        
    Returns:
        tuple: Results tuple with generated content or error messages
    """
    def update_progress(message, progress=None):
        """Update progress with optional percentage."""
        if progress_callback:
            progress_callback(message, progress)
        logger.info(message)
    
    try:
        # Validate inputs
        if not script or not script.strip():
            logger.error("Empty script provided")
            return ("Error: Please provide a script", None, [], [], [], [], None)
            
        if not gemini_api_key or not gemini_api_key.strip():
            logger.error("Empty API key provided")
            return ("Error: Please provide a valid Gemini API key", None, [], [], [], [], None)
        
        update_progress("🚀 Starting video generation...", 0)
        logger.info(f"Starting video generation for script: {script[:100]}...")
        
        # Call Gemini API with error handling
        try:
            update_progress("🔍 Analyzing script with Gemini AI...", 10)
            detailed_script = call_gemini_api(script, gemini_api_key, segment_duration)
            if detailed_script is None:
                return ("Error: Failed to get response from Gemini API", None, [], [], [], [], None)
            update_progress("✅ Script analysis completed", 20)
        except Exception as e:
            logger.error(f"Gemini API call failed: {e}")
            return (f"Error: Gemini API call failed: {str(e)}", None, [], [], [], [], None)
          # Parse script with error handling
        try:
            update_progress("📝 Parsing detailed script...", 30)
            parsed = parse_detailed_script(detailed_script)
            update_progress(f"✅ Parsed script into {len(parsed['video'])} segments", 40)
            logger.info(f"Parsed script into {len(parsed['video'])} segments")
        except Exception as e:
            logger.error(f"Script parsing failed: {e}")
            return (detailed_script, f"Error: Script parsing failed: {str(e)}", [], [], [], [], None)
        
        # Initialize caches and async processing
        face_cache = {}
        loop = asyncio.get_event_loop()
        
        # Generate video segments with error handling
        try:
            update_progress("🎥 Generating video segments...", 50)
            video_segments = await asyncio.gather(*[
                loop.run_in_executor(None, safe_generate_video_segment, cmd, face_cache, segment_duration)
                for cmd in parsed["video"]
            ])
            successful_videos = len([v for v in video_segments if v])
            update_progress(f"✅ Generated {successful_videos}/{len(parsed['video'])} video segments", 60)
            logger.info(f"Generated {successful_videos} video segments")
        except Exception as e:
            logger.error(f"Video segment generation failed: {e}")
            video_segments = []
        
        # Generate TTS audio with error handling  
        try:
            update_progress("🎙️ Generating TTS audio...", 70)
            tts_audios = await asyncio.gather(*[
                loop.run_in_executor(None, safe_generate_tts_audio, cmd)
                for cmd in parsed["tts"]
            ])
            successful_tts = len([a for a in tts_audios if a])
            update_progress(f"✅ Generated {successful_tts}/{len(parsed['tts'])} TTS audio files", 75)
            logger.info(f"Generated {successful_tts} TTS audio files")
        except Exception as e:
            logger.error(f"TTS generation failed: {e}")
            tts_audios = []
        
        # Generate background audio with error handling
        try:
            update_progress("🎵 Generating background audio...", 80)
            background_audios = await asyncio.gather(*[
                loop.run_in_executor(None, safe_generate_background_audio, cmd)
                for cmd in parsed["audio"]
            ])
            successful_bg = len([a for a in background_audios if a])
            update_progress(f"✅ Generated {successful_bg}/{len(parsed['audio'])} background audio files", 85)
            logger.info(f"Generated {successful_bg} background audio files")
        except Exception as e:
            logger.error(f"Background audio generation failed: {e}")
            background_audios = []
        
        # Generate character images with error handling
        try:
            update_progress("🎨 Generating character images...", 90)
            character_images = await asyncio.gather(*[
                loop.run_in_executor(None, safe_generate_character_image, cmd, seed)
                for cmd in parsed["image"]
            ])
            successful_images = len([i for i in character_images if i and i != 'placeholder_image.png'])
            update_progress(f"✅ Generated {successful_images}/{len(parsed['image'])} character images", 95)
            logger.info(f"Generated {successful_images} character images")
        except Exception as e:
            logger.error(f"Character image generation failed: {e}")
            character_images = []
        
        # Assemble final video with error handling
        try:
            update_progress("🎬 Assembling final video...", 98)
            final_video_path = await loop.run_in_executor(
                None, safe_assemble_video, video_segments, tts_audios, background_audios, character_images
            )
            if final_video_path:
                update_progress(f"🎉 Video generation completed! Saved to: {final_video_path}", 100)
                logger.info(f"Final video assembled: {final_video_path}")
            else:
                update_progress("❌ Video assembly failed", 100)
                logger.error("Video assembly failed")
        except Exception as e:
            logger.error(f"Video assembly failed: {e}")
            final_video_path = None
          return (
            detailed_script,
            str(parsed),
            tts_audios,
            character_images,
            video_segments,
            background_audios,
            final_video_path
        )
        
    except Exception as e:
        logger.error(f"Unexpected error in generate_video_async: {e}")
        return (f"Error: Unexpected error occurred: {str(e)}", None, [], [], [], [], None)

def generate_video(script, gemini_api_key, segment_duration, seed):
    return asyncio.run(generate_video_async(script, gemini_api_key, segment_duration, seed))

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

def main():
    """Main entry point for console script"""
    demo.launch()
