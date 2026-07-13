from fastapi import FastAPI
from typing import Annotated
from pydantic import BaseModel, Field
from enum import Enum

Trait = Annotated[str, Field(min_length=1, max_length=50)]

class Persona(BaseModel):
    name: Annotated[str, Field(min_length=1, max_length=200)]
    role: Annotated[str, Field(min_length=1, max_length=200)]
    personality_traits: Annotated[list[Trait], Field(min_length=1, max_length=20)]
    speech_style: Annotated[str, Field(min_length=1, max_length=200)]
    
class Speaker(str, Enum):
    Player = "player"
    NPC = "npc"

class Turn(BaseModel):
    speaker: Speaker
    text: Annotated[str, Field(min_length=1, max_length=500)]

class DialogueRequest(BaseModel):
    persona: Persona
    scenario: Annotated[str, Field(min_length=1, max_length=200)]
    player_input: Annotated[str, Field(min_length=1, max_length=500)]

class Emotion(str, Enum):
    Neutral = "neutral"
    Happy = "happy"
    Sad = "sad"
    Angry = "angry"
    Bored = "bored"
    Afraid = "afraid"
    Surprised = "surprised"

class DialogueResponse(BaseModel):
    text: Annotated[str, Field(min_length=1, max_length=500)]
    emotion: Emotion

app = FastAPI()

@app.post("/dialogue")
def create_dialogue(request: DialogueRequest) -> DialogueResponse:
    return DialogueResponse(text="hello world", emotion=Emotion.Happy)
