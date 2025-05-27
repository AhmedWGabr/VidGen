# VidGen Project Structure

This project is in the process of being reorganized from the old flat structure to a new modular package structure.

## Project Organization

### Current Structure

The codebase currently contains two parallel implementations:

1. **Legacy Structure (Root Directory)**
   - `app.py` - Main application with Gradio UI
   - `agent.py` - Script parsing and processing
   - `models.py` - ML models for video, image, and audio generation
   - `assemble.py` - Video assembly functions
   - `config.py` - Configuration settings
   - Other helper files

2. **New Package Structure (src/vidgen/)**
   - Organized in a proper Python package structure
   - Cleaner separation of concerns
   - Better testability
   - Proper module organization

The plan is to fully migrate to the new structure and eventually remove the legacy files.

## Migration Status

| Component | Legacy File | New Location | Status |
|-----------|-------------|--------------|--------|
| Config | `config.py` | `src/vidgen/core/config.py` | ✅ Complete |
| Script Parser | `agent.py` | `src/vidgen/services/script_parser.py` | ✅ Complete |
| Image Generation | `models.py` | `src/vidgen/models/image.py` | ✅ Complete |
| TTS Generation | `models.py` | `src/vidgen/models/tts.py` | ✅ Complete |
| Video Generation | `models.py` | `src/vidgen/models/video.py` | ✅ Complete |
| Audio Generation | `models.py` | `src/vidgen/models/audio.py` | ✅ Complete |
| Gemini API | `app.py` | `src/vidgen/services/gemini_api.py` | ✅ Complete |
| Video Assembly | `assemble.py` | `src/vidgen/services/video_assembler.py` | ✅ Complete |
| Main App | `app.py` | `src/vidgen/main.py` | ✅ Complete |
| UI Components | `app.py` | `src/vidgen/ui/gradio_app.py` | ⚠️ Partial |

## Next Steps

1. Complete the missing unit tests
2. Finish migrating any remaining UI components
3. Update the entry point scripts to use the new structure
4. Remove the old legacy files after ensuring all functionality is preserved
5. Update documentation to reflect the new structure

## Usage

For now, the project can still be run using the legacy entry points, but we recommend moving to the new structure:

```bash
# Legacy entry point
python app.py

# New entry point
python -m src.vidgen.main
```

## Testing

Tests are being written for the new structure:

```bash
# Run all tests
pytest tests/

# Run specific test category
pytest tests/test_models/
pytest tests/test_services/
```
