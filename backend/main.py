from fastapi import FastAPI
from pydantic import BaseModel
from backend.poem_generator import (
    generate_haiku,
    generate_sonnet,
    generate_limerick,
    generate_free_verse
)

app = FastAPI()

# Request model
class PoemRequest(BaseModel):
    poem_type: str  # haiku, sonnet, limerick, free_verse
    emotion: str
    style: str

@app.get("/")
def root():
    return {"message": "AI Poetry Generator API is running!"}

@app.post("/generate")
def generate_poem(request: PoemRequest):
    poem_type = request.poem_type.lower()
    emotion = request.emotion.lower()
    style = request.style.lower()

    if poem_type == "haiku":
        poem = generate_haiku(emotion, style)
    elif poem_type == "sonnet":
        poem = generate_sonnet(emotion, style)
    elif poem_type == "limerick":
        poem = generate_limerick(emotion, style)
    elif poem_type == "free_verse":
        poem = generate_free_verse(emotion, style)
    else:
        return {"error": f"Invalid poem type: {poem_type}"}

    return {
        "poem": poem,
        "poem_type": poem_type,
        "emotion": emotion,
        "style": style
    }
