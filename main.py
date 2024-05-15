import requests
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()
origins = {
    "http://localhost:8000",
    "http://localhost:5173",
    "https://localhost:5173",
}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

API_URL = "https://api-inference.huggingface.co/models/openai/whisper-medium"
HEADERS = {"Authorization": "Bearer "+os.getenv("API_KEY")}


def query(filename):
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers=HEADERS, data=data)
    return response.json()


@app.post("/post-audio")
async def post_audio(file: UploadFile = File(...)):
    try:
        # Save the uploaded audio file
        with open("temp_audio.flac", "wb") as f:
            f.write(await file.read())

        # Query the Hugging Face API to convert audio to text
        text_response = query("temp_audio.flac")

        # Extract the converted text
        converted_text = text_response['text']

        # Print the converted text
        print("Converted Text:", converted_text)

        # Return the text response
        return JSONResponse(content=text_response)

    except Exception as e:
        return JSONResponse(content={"error": str(e)})


@app.get("/health")
async def root():
    return {"message": "Hello World"}
