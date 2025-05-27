# Model Files Guide

## ✅ What IS Included (Source Code)

The following **source code files** are included in the repository and are essential for VidGen to function:

### Core Model Source Files
- `src/vidgen/models/` - **ALL Python source files are included**
  - `video.py` - Video generation and processing logic
  - `image.py` - Stable Diffusion image generation
  - `tts.py` - Bark TTS text-to-speech
  - `audio.py` - Background audio generation
  - `data_models.py` - Pydantic data models
  - `model_utils.py` - Model utility functions

### Legacy Model Files (Backup)
- `legacy/models.py` - Original model implementations

## ❌ What is NOT Included (Large Binaries)

The following **large binary files** are excluded from git and downloaded automatically:

### Pre-trained Model Weights
- Stable Diffusion model weights (several GB)
- Bark TTS model weights (several GB)  
- Hugging Face cached models (~/.cache/huggingface/)

### Generated Content
- `outputs/videos/` - Generated video files
- `outputs/audio/` - Generated audio files
- `outputs/images/` - Generated image files
- `outputs/temp/` - Temporary processing files

## 🔄 Model Download Process

### Automatic Download
When you first run VidGen, the models will be automatically downloaded:

1. **Stable Diffusion**: `runwayml/stable-diffusion-v1-5`
2. **Bark TTS**: Models downloaded via `pip install bark`

### Manual Download
You can also pre-download models using:

```powershell
python scripts/download_models.py
```

## 🗂️ Directory Structure

```
VidGen/
├── src/vidgen/models/          # ✅ Source code (INCLUDED)
│   ├── video.py
│   ├── image.py  
│   ├── tts.py
│   └── audio.py
├── ~/.cache/huggingface/       # ❌ Downloaded models (EXCLUDED)
├── outputs/                    # ❌ Generated content (EXCLUDED)
└── scripts/download_models.py  # ✅ Download script (INCLUDED)
```

## 🚨 Important Notes

- **Source code** in `src/vidgen/models/` is **ALWAYS included**
- **Binary model files** are **automatically downloaded** when needed
- **Generated content** is excluded to keep repository size manageable
- Use **Git LFS** if you need to include specific model files

## 🔧 Troubleshooting

If models aren't loading:

1. Check internet connection (models download from Hugging Face)
2. Run: `python scripts/download_models.py`
3. Verify disk space (models require several GB)
4. Check CUDA setup for GPU acceleration
