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

#LLM prompt#
def build_prompt(request: DialogueRequest) -> str:
    prompt = f"""
You are roleplaying as a non-player character (NPC).
## Character
Name: {request.persona.name}
Role: {request.persona.role}
Personality: {", ".join(request.persona.personality_traits)}
Speech Style: {request.persona.speech_style}

## Instructions
- Stay in character at all times.
- Never mention that you are an AI, language model, or that you are roleplaying.
- React naturally to what the player says or does.
- Your knowledge should be appropriate for your role. Do not know information your character would not reasonably know.
- Express your personality through your choice of words, attitude, and actions.
- Keep responses concise (1 to 2 sentences unless more detail is requested).
- Avoid narrating the player's actions or thoughts.
- If asked something outside your knowledge, respond as the character would.

## Emotion
Determine the NPC's primary emotion after considering the player's latest message.

Allowed emotions:
- neutral
- happy
- sad
- angry
- bored
- afraid
- surprised

## Output
Return ONLY valid JSON in the following format.

{{
"text": "<The NPC's dialogue>",
"emotion": "<one allowed emotion>"
}} 
"""
    return prompt

@app.post("/dialogue")
def create_dialogue(request: DialogueRequest) -> DialogueResponse:
    return DialogueResponse(text="hello world", emotion=Emotion.Happy)

if __name__ == "__main__":
    test_request = DialogueRequest(
        persona = Persona(
            name = "Barry",
            role = "Tavern keeper",
            personality_traits = ["grumpy, loyal, agitated"],
            speech_style = "short, blunt sentences",
        ),
        scenario = "A stranger enters the tavern at midnight",
        player_input = "I'm looking for some beer",
    )
    print(build_prompt(test_request))