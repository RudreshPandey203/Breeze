from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi import File, UploadFile
from pydantic import BaseModel

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class MessageIn(BaseModel):
    message: str

@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your todo list."}

@app.post("/upload_audio/")
async def upload_audio(audio_file: UploadFile = File(...)):
    return {"res":0}

@app.post("/transcript")
async def transcript(message_in: MessageIn):
    print("hello")
    print(message_in.message) 
    print("hello print")
    request = 1
    return {"req": request}

@app.get("/abort")
async def abort():
    print("process aborted")
    return {"message":"process aborted"}