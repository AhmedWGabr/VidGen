from pydantic import BaseModel, validator
from typing import List, Optional

class Character(BaseModel):
    name: str
    description: str
    seed: Optional[int] = None

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Character name cannot be empty')
        return v

class ScriptSegment(BaseModel):
    timestamp: float
    duration: float
    narration: str
    character: Optional[Character] = None
    scene_description: str

    @validator('duration')
    def duration_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Duration must be positive')
        return v

class VideoProject(BaseModel):
    script: str
    segments: List[ScriptSegment]
    characters: List[Character]
    output_path: str
