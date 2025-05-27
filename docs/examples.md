# VidGen Examples

This document provides practical examples of how to use VidGen for various video generation tasks, from simple scripts to advanced customizations and production workflows.

## Table of Contents
1. [Quick Start Examples](#quick-start-examples)
2. [Script Writing Guide](#script-writing-guide)
3. [Advanced Programming Examples](#advanced-programming-examples)
4. [Production Workflows](#production-workflows)
5. [Integration Examples](#integration-examples)
6. [Performance Optimization](#performance-optimization)

## Quick Start Examples

### 1. Command Line Interface

The simplest way to use VidGen is through the command line:

```bash
# Basic video generation
python -m vidgen.main --script path/to/script.txt --output my_video.mp4

# With custom settings
python -m vidgen.main \
  --script path/to/script.txt \
  --output video.mp4 \
  --duration 7 \
  --resolution 1920x1080 \
  --fps 30 \
  --seed 42 \
  --api-key YOUR_GEMINI_API_KEY

# Batch processing multiple scripts
python -m vidgen.batch \
  --input-dir ./scripts \
  --output-dir ./outputs \
  --parallel 3 \
  --api-key YOUR_API_KEY
```

### 2. Gradio Web Interface

For a visual interface with real-time preview:

```bash
# Start the web interface
python -m vidgen.ui

# With custom configuration
python -m vidgen.ui --port 8080 --share --debug
```

### 3. Basic Python API

```python
from vidgen import VidGen
from vidgen.core.config import VideoGenConfig

# Initialize VidGen
vg = VidGen(api_key="YOUR_GEMINI_API_KEY")

# Configure settings
VideoGenConfig.OUTPUT_DIR = "./my_videos"
VideoGenConfig.VIDEO_RESOLUTION = "1920x1080"

# Generate from script text
script = """
A serene mountain landscape at sunrise.
[Background: Gentle acoustic guitar music]

NARRATOR: "In the early morning light, nature awakens with quiet beauty."

A deer drinking from a crystal-clear stream.

NARRATOR: "Wildlife begins their daily rituals, undisturbed by the world beyond."
"""

# Generate the video
result = vg.generate_video(
    script=script,
    segment_duration=6,
    output_filename="nature_scene.mp4"
)

print(f"Video created: {result.video_path}")
print(f"Assets created: {len(result.image_paths)} images, {len(result.audio_paths)} audio files")
```

## Script Writing Guide

### Script Format Specification

VidGen uses a structured script format that combines visual descriptions, narration, and audio cues:

```
Title: "Your Video Title"

[Optional: Global settings like background music]

VISUAL_DESCRIPTION_1
[Background: Optional background audio description]

SPEAKER_NAME: "Dialogue or narration text"

VISUAL_DESCRIPTION_2

SPEAKER_NAME: "More dialogue"
```

### Example Scripts by Category

#### Educational Content
```
Title: "Understanding Climate Change"

A graph showing global temperature trends over the past century.
[Background: Subtle ambient music]

DR. SMITH: "Climate data shows a clear warming trend accelerating since 1980."

Satellite imagery of Arctic ice coverage comparison between 1980 and 2020.

DR. SMITH: "Arctic sea ice has decreased by approximately 13% per decade."

Animation of greenhouse gases trapping heat in Earth's atmosphere.

DR. SMITH: "The greenhouse effect, enhanced by human activities, is the primary driver of this change."

Renewable energy facilities: solar panels and wind turbines.

DR. SMITH: "Transitioning to renewable energy sources offers our best path forward."
```

#### Product Demonstration
```
Title: "SmartHome Pro - Your Intelligent Living Solution"

Modern living room with seamless smart home integration.
[Background: Upbeat, tech-inspired background music]

PRESENTER: "Welcome to the future of home automation with SmartHome Pro."

Close-up of the central hub device with its sleek LED indicators.

PRESENTER: "Our AI-powered hub learns your preferences and optimizes your home environment automatically."

Person using smartphone app to control lights, temperature, and security systems.

PRESENTER: "Control every aspect of your home with intuitive touch controls or simple voice commands."

Energy usage dashboard showing significant savings over time.

PRESENTER: "SmartHome Pro doesn't just add convenience - it reduces your energy bills by up to 30%."
```

#### Storytelling / Narrative
```
Title: "The Last Library"

A vast, abandoned library with dust motes dancing in shafts of sunlight.
[Background: Melancholy orchestral music]

NARRATOR: "In a world where knowledge had become digital, the old libraries stood empty."

An elderly librarian, ELENA, carefully tending to ancient books.

ELENA: "These books hold stories that algorithms can't capture."

Close-up of weathered hands turning delicate pages of a leather-bound tome.

NARRATOR: "Elena had spent forty years as guardian of humanity's written heritage."

A young girl, MAYA, discovering the library and looking around in wonder.

MAYA: "What are all these things?"

ELENA: "These, my dear, are books. Each one contains an entire world."
```

#### Corporate/Marketing
```
Title: "GreenTech Solutions - Sustainable Innovation"

Aerial view of a modern corporate campus with integrated solar panels and green spaces.
[Background: Inspiring, forward-thinking instrumental music]

CEO: "At GreenTech Solutions, we believe technology should heal our planet, not harm it."

Research lab with scientists developing biodegradable electronics.

CEO: "Our breakthrough in biodegradable semiconductors will revolutionize the electronics industry."

Factory floor showing automated, zero-waste manufacturing processes.

CEO: "Every product we create is designed for complete recyclability from day one."

Montage of various products in use: phones, computers, and IoT devices.

CEO: "Join us in building a sustainable tomorrow, today."
```

## Advanced Programming Examples

### 1. Component-Level Control

For maximum flexibility, use VidGen's individual components:

```python
from vidgen.services.gemini_api import call_gemini_api
from vidgen.services.script_parser import parse_detailed_script
from vidgen.models import VideoModel, AudioModel, TTSModel, ImageModel
from vidgen.services.video_assembler import VideoAssembler
from vidgen.core.config import VideoGenConfig
from vidgen.utils.progress import ProgressTracker

class CustomVideoGenerator:
    def __init__(self, api_key: str):
        # Initialize models
        self.video_model = VideoModel(VideoGenConfig)
        self.audio_model = AudioModel(VideoGenConfig)
        self.tts_model = TTSModel(VideoGenConfig)
        self.image_model = ImageModel(VideoGenConfig)
        self.assembler = VideoAssembler(VideoGenConfig)
        self.api_key = api_key
        
    def generate_with_custom_pipeline(self, script: str, **kwargs):
        """Custom generation pipeline with detailed control"""
        
        tracker = ProgressTracker("Custom Video Generation", total_steps=7)
        
        # Step 1: Generate detailed script
        tracker.update(1, "Generating detailed script...")
        detailed_script = call_gemini_api(
            script, 
            api_key=self.api_key,
            segment_duration=kwargs.get('duration', 5)
        )
        
        # Step 2: Parse script components
        tracker.update(2, "Parsing script components...")
        parsed = parse_detailed_script(detailed_script)
        
        # Step 3: Generate character consistency images
        tracker.update(3, "Creating character references...")
        character_cache = {}
        for img_cmd in parsed.get("character_images", []):
            char_id = img_cmd.get("character_id")
            if char_id and char_id not in character_cache:
                character_cache[char_id] = self.image_model.generate_character_image(
                    img_cmd["prompt"],
                    seed=img_cmd.get("seed", 42)
                )
        
        # Step 4: Generate background audio
        tracker.update(4, "Generating background audio...")
        bg_audio_paths = []
        for audio_cmd in parsed.get("audio", []):
            audio_path = self.audio_model.generate_audio(
                description=audio_cmd["description"],
                duration=audio_cmd.get("duration", 30),
                style=audio_cmd.get("style", "ambient")
            )
            bg_audio_paths.append(audio_path)
        
        # Step 5: Generate TTS narration
        tracker.update(5, "Creating voice narration...")
        tts_paths = []
        for tts_cmd in parsed.get("tts", []):
            tts_path = self.tts_model.generate_speech(
                text=tts_cmd["text"],
                voice=tts_cmd.get("voice", "default"),
                emotion=tts_cmd.get("emotion", "neutral")
            )
            tts_paths.append(tts_path)
        
        # Step 6: Generate video segments
        tracker.update(6, "Generating video segments...")
        video_segments = []
        for i, video_cmd in enumerate(parsed.get("video", [])):
            # Apply character consistency
            if "character_id" in video_cmd:
                video_cmd["character_image"] = character_cache.get(video_cmd["character_id"])
            
            segment = self.video_model.generate_video_segment(
                **video_cmd,
                segment_index=i,
                total_segments=len(parsed["video"])
            )
            video_segments.append(segment)
        
        # Step 7: Assemble final video
        tracker.update(7, "Assembling final video...")
        output_path = self.assembler.assemble_video_with_effects(
            video_segments=video_segments,
            tts_audios=tts_paths,
            background_audios=bg_audio_paths,
            transitions=kwargs.get('transitions', ['fade'] * (len(video_segments)-1)),
            effects=kwargs.get('effects', []),
            output_file=kwargs.get('output_filename', 'custom_video.mp4')
        )
        
        tracker.complete()
        return {
            'video_path': output_path,
            'segments': video_segments,
            'audio_paths': tts_paths + bg_audio_paths,
            'character_images': list(character_cache.values())
        }

# Usage example
generator = CustomVideoGenerator(api_key="YOUR_API_KEY")

result = generator.generate_with_custom_pipeline(
    script="A space exploration documentary",
    duration=8,
    transitions=['fade', 'slide_left', 'zoom', 'dissolve'],
    effects=['color_grade', 'stabilization'],
    output_filename="space_documentary.mp4"
)
```

### 2. Advanced Scene Transitions and Effects

```python
from vidgen.services.video_assembler import VideoAssembler
from vidgen.utils.effects import VideoEffects

class AdvancedVideoProducer:
    def __init__(self):
        self.assembler = VideoAssembler()
        self.effects = VideoEffects()
    
    def create_cinematic_video(self, segments, audio_paths):
        """Create a video with cinematic transitions and effects"""
        
        # Define sophisticated transition sequence
        transitions = [
            {"type": "fade", "duration": 1.5, "easing": "ease_in_out"},
            {"type": "slide_right", "duration": 1.0, "blur": True},
            {"type": "zoom_in", "duration": 2.0, "focal_point": "center"},
            {"type": "wipe_diagonal", "duration": 1.2, "direction": "top_left"},
            {"type": "dissolve", "duration": 1.8, "opacity_curve": "smooth"}
        ]
        
        # Apply sophisticated effects
        effects_pipeline = [
            {"name": "color_grade", "params": {"warmth": 1.2, "contrast": 1.1}},
            {"name": "film_grain", "params": {"intensity": 0.3, "size": 1.0}},
            {"name": "vignette", "params": {"strength": 0.4, "radius": 0.8}},
            {"name": "stabilization", "params": {"strength": 0.7}},
            {"name": "auto_levels", "params": {"gamma": 1.1}}
        ]
        
        # Create advanced audio mix
        audio_mix = {
            "narration": {"volume": 0.8, "eq": "voice_enhance"},
            "background": {"volume": 0.3, "fade_in": 2.0, "fade_out": 3.0},
            "sfx": {"volume": 0.6, "spatial": True}
        }
        
        return self.assembler.assemble_with_advanced_features(
            video_segments=segments,
            audio_paths=audio_paths,
            transitions=transitions,
            effects=effects_pipeline,
            audio_mix=audio_mix,
            output_resolution="3840x2160",  # 4K
            output_framerate=60,
            quality_preset="high"
        )
```

### 3. Batch Processing with Error Recovery

```python
import os
import json
from typing import List, Dict
from pathlib import Path
from tqdm import tqdm
from vidgen import VidGen
from vidgen.core.exceptions import VidGenError, with_error_recovery

class BatchVideoProcessor:
    def __init__(self, api_key: str, output_dir: str = "./batch_outputs"):
        self.vidgen = VidGen(api_key=api_key)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        # Create subdirectories
        (self.output_dir / "videos").mkdir(exist_ok=True)
        (self.output_dir / "logs").mkdir(exist_ok=True)
        (self.output_dir / "failed").mkdir(exist_ok=True)
    
    @with_error_recovery
    def process_single_script(self, script_path: str, config: Dict) -> Dict:
        """Process a single script with error recovery"""
        
        script_name = Path(script_path).stem
        
        # Read script
        with open(script_path, 'r', encoding='utf-8') as f:
            script_content = f.read()
        
        # Apply configuration
        for key, value in config.items():
            if hasattr(VideoGenConfig, key.upper()):
                setattr(VideoGenConfig, key.upper(), value)
        
        # Generate video
        result = self.vidgen.generate_video(
            script=script_content,
            output_filename=str(self.output_dir / "videos" / f"{script_name}.mp4"),
            **config
        )
        
        return {
            "status": "success",
            "script_name": script_name,
            "output_path": result.video_path,
            "duration": result.metadata.get("duration"),
            "file_size": os.path.getsize(result.video_path),
            "assets_created": len(result.image_paths) + len(result.audio_paths)
        }
    
    def process_batch(self, 
                     script_directory: str,
                     config_file: str = None,
                     parallel_jobs: int = 2,
                     resume_from_checkpoint: bool = True) -> Dict:
        """
        Process multiple scripts with advanced features:
        - Progress tracking and checkpointing
        - Error recovery and retry logic
        - Detailed logging and reporting
        - Parallel processing with resource management
        """
        
        # Load configuration
        config = {}
        if config_file and os.path.exists(config_file):
            with open(config_file, 'r') as f:
                config = json.load(f)
        
        # Find script files
        script_files = list(Path(script_directory).glob("*.txt"))
        
        # Load checkpoint if resuming
        checkpoint_file = self.output_dir / "checkpoint.json"
        completed = set()
        if resume_from_checkpoint and checkpoint_file.exists():
            with open(checkpoint_file, 'r') as f:
                checkpoint_data = json.load(f)
                completed = set(checkpoint_data.get("completed", []))
        
        # Filter out already completed scripts
        remaining_scripts = [s for s in script_files if s.stem not in completed]
        
        results = []
        failed_scripts = []
        
        # Process with progress tracking
        with tqdm(total=len(remaining_scripts), desc="Processing scripts") as pbar:
            for script_path in remaining_scripts:
                try:
                    # Process with configuration
                    result = self.process_single_script(str(script_path), config)
                    results.append(result)
                    completed.add(script_path.stem)
                    
                    # Update checkpoint
                    with open(checkpoint_file, 'w') as f:
                        json.dump({"completed": list(completed)}, f)
                    
                    # Log success
                    self._log_result(result, "success")
                    pbar.set_postfix(success=len(results), failed=len(failed_scripts))
                    
                except VidGenError as e:
                    # Handle VidGen-specific errors
                    error_info = {
                        "script_name": script_path.stem,
                        "error_type": type(e).__name__,
                        "error_message": str(e),
                        "recovery_suggestion": getattr(e, 'recovery_suggestion', 'None')
                    }
                    failed_scripts.append(error_info)
                    self._log_result(error_info, "error")
                    
                    # Move failed script to failed directory
                    failed_path = self.output_dir / "failed" / script_path.name
                    script_path.rename(failed_path)
                    
                except Exception as e:
                    # Handle unexpected errors
                    error_info = {
                        "script_name": script_path.stem,
                        "error_type": "UnexpectedError",
                        "error_message": str(e),
                        "recovery_suggestion": "Check logs for details"
                    }
                    failed_scripts.append(error_info)
                    self._log_result(error_info, "error")
                
                pbar.update(1)
        
        # Generate summary report
        summary = {
            "total_scripts": len(script_files),
            "successful": len(results),
            "failed": len(failed_scripts),
            "success_rate": len(results) / len(script_files) * 100,
            "results": results,
            "failed_scripts": failed_scripts
        }
        
        # Save detailed report
        report_path = self.output_dir / "batch_report.json"
        with open(report_path, 'w') as f:
            json.dump(summary, f, indent=2)
        
        return summary
    
    def _log_result(self, result_data: Dict, status: str):
        """Log processing results"""
        log_file = self.output_dir / "logs" / f"batch_processing.log"
        
        with open(log_file, 'a') as f:
            timestamp = datetime.now().isoformat()
            f.write(f"[{timestamp}] {status.upper()}: {json.dumps(result_data)}\n")

# Usage example
processor = BatchVideoProcessor(api_key="YOUR_API_KEY")

# Process a directory of scripts
summary = processor.process_batch(
    script_directory="./marketing_scripts",
    config_file="./batch_config.json",
    parallel_jobs=3,
    resume_from_checkpoint=True
)

print(f"Batch processing complete:")
print(f"Success rate: {summary['success_rate']:.1f}%")
print(f"Videos created: {summary['successful']}")
print(f"Failed scripts: {summary['failed']}")
```

## Production Workflows

### 1. Content Creator Pipeline

A complete workflow for content creators producing educational videos:

```python
from vidgen import VidGen
from vidgen.workflows import ContentCreatorWorkflow
from vidgen.utils.content_tools import ScriptValidator, ContentOptimizer

class EducationalVideoWorkflow:
    def __init__(self, api_key: str, brand_config: Dict):
        self.vidgen = VidGen(api_key=api_key)
        self.brand_config = brand_config
        self.validator = ScriptValidator()
        self.optimizer = ContentOptimizer()
        
        # Apply brand configuration
        self._setup_brand_defaults()
    
    def _setup_brand_defaults(self):
        """Apply consistent branding across all videos"""
        VideoGenConfig.update({
            'default_color_palette': self.brand_config['colors'],
            'brand_fonts': self.brand_config['fonts'],
            'logo_watermark': self.brand_config['logo_path'],
            'intro_template': self.brand_config['intro_template'],
            'outro_template': self.brand_config['outro_template']
        })
    
    def create_educational_series(self, 
                                topic: str, 
                                num_episodes: int,
                                target_duration: int = 300) -> List[str]:
        """Create a complete educational video series"""
        
        # 1. Generate series outline
        series_outline = self.optimizer.create_series_outline(
            topic=topic,
            episodes=num_episodes,
            target_audience="general",
            difficulty_progression=True
        )
        
        video_paths = []
        
        for i, episode_data in enumerate(series_outline['episodes']):
            print(f"Creating Episode {i+1}: {episode_data['title']}")
            
            # 2. Generate detailed script
            script = self.optimizer.create_detailed_script(
                title=episode_data['title'],
                learning_objectives=episode_data['objectives'],
                key_concepts=episode_data['concepts'],
                target_duration=target_duration
            )
            
            # 3. Validate script
            validation_result = self.validator.validate_educational_script(script)
            if not validation_result['is_valid']:
                script = self.optimizer.fix_script_issues(script, validation_result['issues'])
            
            # 4. Add series-specific elements
            script_with_branding = self._add_series_branding(
                script, 
                episode_number=i+1,
                total_episodes=num_episodes,
                series_title=series_outline['series_title']
            )
            
            # 5. Generate video
            result = self.vidgen.generate_video(
                script=script_with_branding,
                output_filename=f"episode_{i+1:02d}_{episode_data['slug']}.mp4",
                quality_preset="educational",  # Optimized for learning content
                include_captions=True,
                include_chapter_markers=True
            )
            
            video_paths.append(result.video_path)
            
            # 6. Generate accompanying materials
            self._create_study_materials(episode_data, result)
        
        return video_paths
    
    def _add_series_branding(self, script: str, **metadata) -> str:
        """Add consistent branding elements to script"""
        branded_script = f"""
Title: "{metadata['series_title']} - Episode {metadata['episode_number']}"

{self.brand_config['intro_template']}

{script}

{self.brand_config['outro_template'].format(
    next_episode=metadata['episode_number'] + 1 if metadata['episode_number'] < metadata['total_episodes'] else None
)}
"""
        return branded_script
    
    def _create_study_materials(self, episode_data: Dict, video_result):
        """Generate supplementary educational materials"""
        # Generate transcript
        transcript_path = video_result.video_path.replace('.mp4', '_transcript.txt')
        
        # Generate summary PDF
        summary_path = video_result.video_path.replace('.mp4', '_summary.pdf')
        
        # Generate quiz questions
        quiz_path = video_result.video_path.replace('.mp4', '_quiz.json')
        
        # Implementation would use additional AI services
        # for transcript generation, summarization, etc.

# Usage
brand_config = {
    'colors': ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D'],
    'fonts': ['Roboto', 'Open Sans'],
    'logo_path': 'assets/logo.png',
    'intro_template': 'Welcome to TechEd Academy. Today we explore...',
    'outro_template': 'Thanks for watching! Next episode: {next_episode}'
}

workflow = EducationalVideoWorkflow(
    api_key="YOUR_API_KEY",
    brand_config=brand_config
)

# Create a 5-episode series on machine learning
series_videos = workflow.create_educational_series(
    topic="Introduction to Machine Learning",
    num_episodes=5,
    target_duration=600  # 10 minutes each
)
```

### 2. Marketing Agency Workflow

```python
from vidgen.workflows import MarketingWorkflow
from vidgen.utils.analytics import PerformancePredictor
from vidgen.utils.brand_tools import BrandGuideline

class MarketingCampaignGenerator:
    def __init__(self, api_key: str):
        self.workflow = MarketingWorkflow(api_key=api_key)
        self.predictor = PerformancePredictor()
        
    def create_campaign_variants(self, 
                               brief: Dict,
                               num_variants: int = 3,
                               platforms: List[str] = ['youtube', 'instagram', 'tiktok']) -> Dict:
        """Create multiple variants for A/B testing"""
        
        campaign_results = {}
        
        for platform in platforms:
            platform_variants = []
            
            for variant in range(num_variants):
                # Generate platform-specific script
                script = self.workflow.generate_platform_script(
                    brief=brief,
                    platform=platform,
                    variant_style=variant,
                    target_audience=brief['target_audience']
                )
                
                # Predict performance
                predicted_metrics = self.predictor.predict_engagement(
                    script=script,
                    platform=platform,
                    audience=brief['target_audience']
                )
                
                # Generate video
                video_result = self.workflow.generate_marketing_video(
                    script=script,
                    platform_specs=self._get_platform_specs(platform),
                    brand_guidelines=brief['brand_guidelines']
                )
                
                platform_variants.append({
                    'video_path': video_result.video_path,
                    'predicted_metrics': predicted_metrics,
                    'variant_id': f"{platform}_v{variant+1}",
                    'optimization_suggestions': predicted_metrics['suggestions']
                })
            
            campaign_results[platform] = platform_variants
        
        return campaign_results
    
    def _get_platform_specs(self, platform: str) -> Dict:
        """Get platform-specific video specifications"""
        specs = {
            'youtube': {
                'resolution': '1920x1080',
                'aspect_ratio': '16:9',
                'max_duration': 600,
                'format': 'mp4'
            },
            'instagram': {
                'resolution': '1080x1080',
                'aspect_ratio': '1:1',
                'max_duration': 60,
                'format': 'mp4'
            },
            'tiktok': {
                'resolution': '1080x1920',
                'aspect_ratio': '9:16',
                'max_duration': 180,
                'format': 'mp4'
            }
        }
        return specs.get(platform, specs['youtube'])

# Usage
campaign_generator = MarketingCampaignGenerator(api_key="YOUR_API_KEY")

brief = {
    'product': 'Eco-friendly water bottle',
    'target_audience': 'environmentally conscious millennials',
    'key_message': 'Sustainable hydration for active lifestyles',
    'call_to_action': 'Shop now for 20% off',
    'brand_guidelines': {
        'tone': 'friendly and energetic',
        'colors': ['#2D5A27', '#8BC34A', '#FFFFFF'],
        'values': ['sustainability', 'health', 'adventure']
    }
}

campaign_variants = campaign_generator.create_campaign_variants(
    brief=brief,
    num_variants=3,
    platforms=['youtube', 'instagram', 'tiktok']
)

# Analyze results
for platform, variants in campaign_variants.items():
    print(f"\n{platform.title()} Variants:")
    for variant in variants:
        print(f"  {variant['variant_id']}: "
              f"Predicted engagement: {variant['predicted_metrics']['engagement_score']:.2f}")
```

## Integration Examples

### 1. Flask Web Application

```python
from flask import Flask, request, jsonify, send_file
from vidgen import VidGen
import os
import uuid
from threading import Thread

app = Flask(__name__)
vidgen_instance = VidGen(api_key=os.getenv('GEMINI_API_KEY'))

# Store for tracking generation status
generation_status = {}

@app.route('/api/generate', methods=['POST'])
def generate_video():
    """Endpoint for video generation requests"""
    data = request.json
    
    # Validate request
    if 'script' not in data:
        return jsonify({'error': 'Script is required'}), 400
    
    # Generate unique job ID
    job_id = str(uuid.uuid4())
    generation_status[job_id] = {'status': 'queued', 'progress': 0}
    
    # Start generation in background
    thread = Thread(target=_generate_async, args=(job_id, data))
    thread.start()
    
    return jsonify({'job_id': job_id, 'status': 'queued'})

@app.route('/api/status/<job_id>')
def check_status(job_id):
    """Check generation status"""
    if job_id not in generation_status:
        return jsonify({'error': 'Job not found'}), 404
    
    return jsonify(generation_status[job_id])

@app.route('/api/download/<job_id>')
def download_video(job_id):
    """Download generated video"""
    if job_id not in generation_status:
        return jsonify({'error': 'Job not found'}), 404
    
    status = generation_status[job_id]
    if status['status'] != 'completed':
        return jsonify({'error': 'Video not ready'}), 400
    
    return send_file(status['video_path'], as_attachment=True)

def _generate_async(job_id: str, data: dict):
    """Background video generation"""
    try:
        # Update status to processing
        generation_status[job_id].update({
            'status': 'processing',
            'progress': 10
        })
        
        # Generate video with progress updates
        def progress_callback(step, total, message):
            progress = int((step / total) * 90) + 10  # 10-100%
            generation_status[job_id].update({
                'progress': progress,
                'current_step': message
            })
        
        result = vidgen_instance.generate_video(
            script=data['script'],
            progress_callback=progress_callback,
            **data.get('options', {})
        )
        
        # Mark as completed
        generation_status[job_id].update({
            'status': 'completed',
            'progress': 100,
            'video_path': result.video_path,
            'metadata': result.metadata
        })
        
    except Exception as e:
        generation_status[job_id].update({
            'status': 'failed',
            'error': str(e)
        })

if __name__ == '__main__':
    app.run(debug=True)
```

### 2. Discord Bot Integration

```python
import discord
from discord.ext import commands
import asyncio
import aiofiles
from vidgen import VidGen

class VidGenBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)
        
        self.vidgen = VidGen(api_key=os.getenv('GEMINI_API_KEY'))
    
    async def on_ready(self):
        print(f'{self.user} has connected to Discord!')

bot = VidGenBot()

@bot.command(name='generate')
async def generate_video_command(ctx, *, script):
    """Generate a video from a script"""
    
    # Send initial response
    embed = discord.Embed(
        title="🎬 Video Generation Started",
        description="Your video is being generated...",
        color=0x00ff00
    )
    message = await ctx.send(embed=embed)
    
    try:
        # Generate video asynchronously
        result = await asyncio.to_thread(
            bot.vidgen.generate_video,
            script=script,
            segment_duration=5,
            output_filename=f"discord_video_{ctx.message.id}.mp4"
        )
        
        # Check file size (Discord limit: 8MB for regular users)
        file_size = os.path.getsize(result.video_path)
        if file_size > 8 * 1024 * 1024:  # 8MB
            embed = discord.Embed(
                title="⚠️ File Too Large",
                description="Video generated but too large for Discord. Uploading to cloud...",
                color=0xff9900
            )
            await message.edit(embed=embed)
            
            # Upload to cloud storage and provide link
            cloud_url = await upload_to_cloud(result.video_path)
            
            embed = discord.Embed(
                title="✅ Video Generated",
                description=f"[Download Video]({cloud_url})",
                color=0x00ff00
            )
            await message.edit(embed=embed)
        else:
            # Send file directly
            embed = discord.Embed(
                title="✅ Video Generated",
                description="Your video is ready!",
                color=0x00ff00
            )
            await message.edit(embed=embed)
            
            await ctx.send(file=discord.File(result.video_path))
    
    except Exception as e:
        embed = discord.Embed(
            title="❌ Generation Failed",
            description=f"Error: {str(e)}",
            color=0xff0000
        )
        await message.edit(embed=embed)

@bot.command(name='help_script')
async def script_help(ctx):
    """Provide script writing help"""
    help_text = """
    **Script Format:**
    ```
    Title: "Your Video Title"
    
    Visual description here.
    [Background: Background audio description]
    
    SPEAKER: "Dialogue or narration"
    
    Another visual description.
    
    SPEAKER: "More dialogue"
    ```
    
    **Tips:**
    • Keep descriptions concise but vivid
    • Include speaker names for different voices
    • Add background audio cues in [brackets]
    • Each segment should be 3-10 seconds of content
    """
    
    embed = discord.Embed(
        title="📝 Script Writing Guide",
        description=help_text,
        color=0x0099ff
    )
    await ctx.send(embed=embed)

async def upload_to_cloud(file_path: str) -> str:
    """Upload large files to cloud storage"""
    # Implementation would use AWS S3, Google Cloud Storage, etc.
    # Return download URL
    pass

bot.run(os.getenv('DISCORD_TOKEN'))
```

## Performance Optimization

### 1. Memory Management

```python
from vidgen.core.config import VideoGenConfig
from vidgen.utils.optimization import MemoryOptimizer
import psutil
import gc

class OptimizedVideoGenerator:
    def __init__(self, api_key: str):
        self.vidgen = VidGen(api_key=api_key)
        self.optimizer = MemoryOptimizer()
        self._setup_optimization()
    
    def _setup_optimization(self):
        """Configure optimal settings based on available resources"""
        
        # Get system specs
        total_ram = psutil.virtual_memory().total / (1024**3)  # GB
        gpu_memory = self._get_gpu_memory()
        
        if total_ram < 16:
            # Low memory configuration
            VideoGenConfig.HALF_PRECISION = True
            VideoGenConfig.MAX_BATCH_SIZE = 1
            VideoGenConfig.STREAMING_MODE = True
            VideoGenConfig.AUTO_CLEANUP = True
        elif total_ram < 32:
            # Medium memory configuration  
            VideoGenConfig.HALF_PRECISION = True
            VideoGenConfig.MAX_BATCH_SIZE = 2
            VideoGenConfig.AUTO_CLEANUP = True
        else:
            # High memory configuration
            VideoGenConfig.HALF_PRECISION = False
            VideoGenConfig.MAX_BATCH_SIZE = 4
            VideoGenConfig.AUTO_CLEANUP = False  # Keep cache for speed
        
        # GPU-specific optimizations
        if gpu_memory and gpu_memory < 8:
            VideoGenConfig.STABLE_DIFFUSION_MODEL = "runwayml/stable-diffusion-v1-5"  # Smaller model
        elif gpu_memory and gpu_memory >= 12:
            VideoGenConfig.STABLE_DIFFUSION_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
    
    def _get_gpu_memory(self) -> float:
        """Get available GPU memory in GB"""
        try:
            import torch
            if torch.cuda.is_available():
                return torch.cuda.get_device_properties(0).total_memory / (1024**3)
        except ImportError:
            pass
        return None
    
    def generate_optimized(self, script: str, **kwargs):
        """Generate video with automatic optimization"""
        
        # Monitor memory during generation
        with self.optimizer.memory_monitor():
            # Pre-generation cleanup
            gc.collect()
            
            # Generate with automatic resource management
            result = self.vidgen.generate_video(
                script=script,
                **kwargs
            )
            
            # Post-generation cleanup if needed
            if psutil.virtual_memory().percent > 85:
                self.optimizer.aggressive_cleanup()
            
            return result

# Usage
generator = OptimizedVideoGenerator(api_key="YOUR_API_KEY")
result = generator.generate_optimized("Your script here")
```

### 2. Caching and Reuse

```python
from vidgen.utils.cache import AssetCache, ModelCache
import hashlib

class CachedVideoGenerator:
    def __init__(self, api_key: str):
        self.vidgen = VidGen(api_key=api_key)
        self.asset_cache = AssetCache(max_size_gb=10)
        self.model_cache = ModelCache()
    
    def generate_with_caching(self, script: str, **kwargs):
        """Generate video with intelligent caching"""
        
        # Generate cache key for script
        script_hash = hashlib.md5(script.encode()).hexdigest()
        cache_key = f"{script_hash}_{kwargs.get('segment_duration', 5)}"
        
        # Check if video already exists
        cached_result = self.asset_cache.get_video(cache_key)
        if cached_result:
            print("✓ Video found in cache")
            return cached_result
        
        # Parse script to identify reusable components
        parsed_script = self.vidgen.parse_script(script)
        
        # Check for cached audio components
        for audio_cmd in parsed_script.get('audio', []):
            audio_key = hashlib.md5(audio_cmd['description'].encode()).hexdigest()
            cached_audio = self.asset_cache.get_audio(audio_key)
            if cached_audio:
                audio_cmd['cached_path'] = cached_audio
                print(f"✓ Reusing cached audio: {audio_cmd['description'][:50]}...")
        
        # Check for cached character images
        character_cache = {}
        for img_cmd in parsed_script.get('image', []):
            char_key = hashlib.md5(img_cmd['prompt'].encode()).hexdigest()
            cached_image = self.asset_cache.get_image(char_key)
            if cached_image:
                character_cache[char_key] = cached_image
                print(f"✓ Reusing cached image: {img_cmd['prompt'][:50]}...")
        
        # Generate video with cache assistance
        result = self.vidgen.generate_video(
            script=script,
            character_cache=character_cache,
            **kwargs
        )
        
        # Store result in cache
        self.asset_cache.store_video(cache_key, result)
        
        return result
```

This comprehensive examples documentation now provides:

1. **Complete practical examples** for different use cases
2. **Advanced programming patterns** for custom workflows
3. **Production-ready code** for content creators and agencies
4. **Integration examples** for web apps and bots
5. **Performance optimization** techniques
6. **Error handling and recovery** patterns
7. **Batch processing** capabilities
8. **Caching and resource management** strategies

The documentation covers everything from simple CLI usage to complex production workflows, making it valuable for users at all levels.
