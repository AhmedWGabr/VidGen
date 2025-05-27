# VidGen Migration Guide

This guide helps you migrate from the legacy VidGen structure to the new organized package architecture.

## Overview

The new VidGen structure provides:
- ✅ **Organized Package Structure**: Clean separation of concerns
- ✅ **Enhanced Error Handling**: Comprehensive error recovery system
- ✅ **Advanced Audio/Video**: Professional-grade effects and transitions
- ✅ **Progress Tracking**: Real-time operation monitoring
- ✅ **Comprehensive Testing**: 70+ test cases with >90% coverage
- ✅ **Type Safety**: Full type annotations throughout

## Migration Checklist

### 📋 Pre-Migration Steps

- [ ] **Backup Current Project**: Create a backup of your existing VidGen installation
- [ ] **Review Dependencies**: Check your current `requirements.txt`
- [ ] **Document Custom Changes**: Note any customizations you've made
- [ ] **Test Current Functionality**: Ensure your current setup works

### 🔄 Code Migration Steps

#### 1. Update Project Structure

**Old Structure:**
```
VidGen/
├── vidgen.py           # Main script
├── config.py           # Configuration
├── models/             # Flat model files
├── utils.py            # Utilities
└── requirements.txt
```

**New Structure:**
```
VidGen/
├── src/vidgen/         # Organized package
│   ├── core/           # Core functionality
│   ├── models/         # AI models
│   ├── services/       # Business logic
│   ├── ui/             # User interface
│   └── utils/          # Utilities
├── tests/              # Comprehensive tests
├── docs/               # Documentation
└── requirements.txt
```

#### 2. Update Imports

**Configuration:**
```python
# Old
from config import Config
config = Config()

# New
from src.vidgen.core.config import Config
config = Config()
```

**Audio Generation:**
```python
# Old
from models.audio import generate_audio
audio_path = generate_audio("background music")

# New
from src.vidgen.models.audio import AudioModel
audio_model = AudioModel(config)
audio_path = audio_model.generate_audio("background music")
```

**Video Generation:**
```python
# Old
from models.video import create_video
video_path = create_video(images, audio)

# New
from src.vidgen.models.video import VideoModel
video_model = VideoModel(config)
video_path = video_model.generate_video_with_transitions(
    image_paths=images,
    audio_path=audio,
    transition_type="fade"
)
```

**Image Generation:**
```python
# Old
from models.image import generate_image
image_path = generate_image(prompt)

# New
from src.vidgen.models.image import ImageModel
image_model = ImageModel(config)
image_path = image_model.generate_image(prompt)
```

**Text-to-Speech:**
```python
# Old
from models.tts import text_to_speech
speech_path = text_to_speech(text)

# New
from src.vidgen.models.tts import TTSModel
tts_model = TTSModel(config)
speech_path = tts_model.generate_speech(text)
```

#### 3. Update Main Application

**Old Main Script:**
```python
# vidgen.py
import gradio as gr
from models import *

def generate_video(script):
    # Legacy implementation
    pass

if __name__ == "__main__":
    interface = gr.Interface(...)
    interface.launch()
```

**New Main Script:**
```python
# run_vidgen.py
from src.vidgen.ui.gradio_app import create_interface

if __name__ == "__main__":
    app = create_interface()
    app.launch()
```

#### 4. Update Error Handling

**Old Error Handling:**
```python
try:
    result = generate_video(script)
except Exception as e:
    print(f"Error: {e}")
    return None
```

**New Error Handling:**
```python
from src.vidgen.core.exceptions import with_error_recovery, VidGenError

@with_error_recovery
def generate_video_safe(script):
    return video_generator.generate_video(script)

try:
    result = generate_video_safe(script)
except VidGenError as e:
    print(f"Error: {e}")
    print(f"Suggestion: {e.recovery_suggestion}")
    # Implement recovery based on suggestion
```

### 🆕 New Features to Adopt

#### 1. Progress Tracking

```python
from src.vidgen.utils.logging_config import ProgressTracker

def generate_with_progress(script):
    tracker = ProgressTracker("Video Generation", total_steps=5)
    
    tracker.update(1, "Parsing script...")
    segments = parse_script(script)
    
    tracker.update(2, "Generating images...")
    images = generate_images(segments)
    
    tracker.update(3, "Creating audio...")
    audio = generate_audio(segments)
    
    tracker.update(4, "Assembling video...")
    video = create_video(images, audio)
    
    tracker.update(5, "Complete!")
    return video
```

#### 2. Advanced Audio Features

```python
from src.vidgen.models.audio import AudioModel

audio_model = AudioModel(config)

# Generate ambient sounds
ambient = audio_model.generate_audio(
    "peaceful forest ambient sounds for 30 seconds"
)

# Generate music
music = audio_model.generate_audio(
    "upbeat electronic music in C major for 2 minutes"
)

# Mix tracks
final_audio = audio_model.mix_audio(
    audio_paths=[ambient, music],
    volumes=[0.6, 0.4]
)
```

#### 3. Video Transitions and Effects

```python
from src.vidgen.models.video import VideoModel

video_model = VideoModel(config)

# Add professional transitions
video_with_transitions = video_model.generate_video_with_transitions(
    image_paths=image_list,
    audio_path=audio_path,
    transition_type="slide_left",
    segment_duration=5.0
)

# Add motion effects
dynamic_video = video_model.add_motion_effects(
    video_path=video_with_transitions,
    effect_type="zoom_pan",
    intensity=0.3
)
```

### 🔧 Configuration Migration

#### Old Configuration
```python
# config.py
GEMINI_API_KEY = "your_key"
IMAGE_MODEL = "stable-diffusion"
OUTPUT_DIR = "./outputs"
```

#### New Configuration
```python
# Use environment variables or config object
import os
from src.vidgen.core.config import Config

# Set environment variables
os.environ["GEMINI_API_KEY"] = "your_key"
os.environ["HUGGINGFACE_TOKEN"] = "your_token"

# Or use config object
config = Config()
config.GEMINI_API_KEY = "your_key"
config.IMAGE_MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
```

### 📁 File Structure Migration

#### 1. Move Custom Models

If you have custom models:

```bash
# Old location
models/custom_audio.py

# New location
src/vidgen/models/custom_audio.py

# Update imports in the file
from ..core.config import Config
from ..utils.logging_config import VidGenLogger
```

#### 2. Move Utility Functions

```bash
# Old location
utils.py

# New location
src/vidgen/utils/custom_utils.py

# Update package imports
from .file_manager import FileManager
from .logging_config import VidGenLogger
```

#### 3. Move Configuration Files

```bash
# Old location
config.yaml

# New location
data/config.yaml

# Update loading code
from src.vidgen.core.config import Config
config = Config.from_file("data/config.yaml")
```

### 🧪 Testing Your Migration

#### 1. Install New Version

```bash
# Remove old installation
pip uninstall vidgen

# Install new version
cd VidGen
pip install -e .
```

#### 2. Run Basic Tests

```python
# test_migration.py
from src.vidgen.core.config import Config
from src.vidgen.services.video_generator import VideoGenerator

def test_basic_functionality():
    config = Config()
    generator = VideoGenerator(config)
    
    # Test with simple script
    script = "A beautiful sunset over the mountains."
    try:
        video_path = generator.generate_video(
            script=script,
            output_path="test_output.mp4"
        )
        print(f"✅ Migration successful! Video: {video_path}")
        return True
    except Exception as e:
        print(f"❌ Migration issue: {e}")
        return False

if __name__ == "__main__":
    test_basic_functionality()
```

#### 3. Run Comprehensive Tests

```bash
# Run the full test suite
python -m pytest tests/ -v

# Run specific migration tests
python -m pytest tests/test_integration.py -v
```

### 🐛 Common Migration Issues

#### Issue 1: Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'models.audio'
```

**Solution:**
```python
# Update import
from src.vidgen.models.audio import AudioModel
```

#### Issue 2: Configuration Not Found

**Error:**
```
AttributeError: 'Config' object has no attribute 'API_KEY'
```

**Solution:**
```python
# Use new configuration structure
from src.vidgen.core.config import Config
config = Config()
config.GEMINI_API_KEY = "your_key"  # Note the new attribute name
```

#### Issue 3: Missing Dependencies

**Error:**
```
ImportError: No module named 'some_package'
```

**Solution:**
```bash
# Install updated requirements
pip install -r requirements.txt

# Or install specific package
pip install missing_package
```

#### Issue 4: File Path Issues

**Error:**
```
FileNotFoundError: Output directory not found
```

**Solution:**
```python
from src.vidgen.utils.file_manager import FileManager

file_manager = FileManager(config)
output_dir = file_manager.ensure_directory("outputs")
```

### 📈 Performance Improvements

The new structure provides several performance benefits:

#### 1. Lazy Loading
```python
# Models are loaded only when needed
from src.vidgen.models.audio import AudioModel
audio_model = AudioModel(config)  # Loaded on demand
```

#### 2. Memory Management
```python
# Automatic cleanup of temporary files
from src.vidgen.utils.file_manager import FileManager

file_manager = FileManager(config)
file_manager.cleanup_temp_files(older_than_hours=1)
```

#### 3. Progress Tracking
```python
# Real-time progress monitoring
def generate_with_callback(script):
    def progress_callback(percent):
        print(f"Progress: {percent}%")
    
    return generator.generate_video(
        script=script,
        progress_callback=progress_callback
    )
```

### 🎯 Advanced Migration Tips

#### 1. Gradual Migration

You can migrate gradually by running both versions:

```python
# Use new for new features
from src.vidgen.models.video import VideoModel
video_model = VideoModel(config)

# Keep old for stable features (temporarily)
# from old_models.audio import generate_audio
```

#### 2. Custom Extensions

If you have custom extensions:

```python
# Create custom module in new structure
# src/vidgen/extensions/my_extension.py

from ..core.config import Config
from ..utils.logging_config import VidGenLogger

class MyExtension:
    def __init__(self, config: Config):
        self.config = config
        self.logger = VidGenLogger(self.__class__.__name__)
```

#### 3. Configuration Management

Use environment variables for deployment:

```bash
# .env file
GEMINI_API_KEY=your_key
HUGGINGFACE_TOKEN=your_token
VIDEO_RESOLUTION=1920x1080
```

```python
# Load in application
from dotenv import load_dotenv
load_dotenv()

from src.vidgen.core.config import Config
config = Config()  # Automatically loads from environment
```

### 📞 Support and Troubleshooting

If you encounter issues during migration:

1. **Check the logs:**
   ```python
   from src.vidgen.utils.logging_config import VidGenLogger
   logger = VidGenLogger("migration")
   logger.info("Migration step completed")
   ```

2. **Use error recovery:**
   ```python
   from src.vidgen.core.exceptions import with_error_recovery
   
   @with_error_recovery
   def migrate_component():
       # Your migration code
       pass
   ```

3. **Run diagnostics:**
   ```bash
   python -m src.vidgen.utils.diagnostics
   ```

4. **Get help:**
   - Check [API Reference](API_REFERENCE.md)
   - Review [test examples](../tests/)
   - Open an issue on GitHub

### ✅ Post-Migration Checklist

- [ ] **All imports updated**: No legacy import statements
- [ ] **Configuration migrated**: Using new Config class
- [ ] **Error handling implemented**: Using new exception system
- [ ] **Tests passing**: All functionality working
- [ ] **Performance verified**: No degradation in speed
- [ ] **Documentation updated**: Internal docs reflect new structure
- [ ] **Team trained**: All developers familiar with new structure

## Conclusion

The new VidGen structure provides significant improvements in:
- **Code Organization**: Clear separation of concerns
- **Error Handling**: Comprehensive recovery system
- **Feature Set**: Advanced audio/video capabilities
- **Maintainability**: Better testing and documentation
- **Extensibility**: Plugin-ready architecture

Take your time with the migration and test thoroughly at each step. The new structure will provide a much better foundation for future development and maintenance.

---

**Need Help?** Open an issue on GitHub or check the [API Reference](API_REFERENCE.md) for detailed documentation.
