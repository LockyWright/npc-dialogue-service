from fastapi import FastAPI

app = FastAPI()

@app.post("/dialogue")
def create_dialogue():
    return {
        "dialogue": "Hello World",
        "emotion": "Happy"
    }
