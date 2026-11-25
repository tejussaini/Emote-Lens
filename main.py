from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model

from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from fastapi.responses import FileResponse

from pydantic import BaseModel, Field

import numpy as np
import pickle
import re
import os


# A. Model Path (BiGRU)
model_path = "Artifacts/BiGRU_Model.keras"

# B. Tokenizer Path
tokenizer_path = "Artifacts/tokenizer.pkl"

# C. Maximum Sequence Length
max_sequence_length = 50

# D. Emotion Labels
emotion_labels = ["sadness", "joy", "love", "anger", "fear", "surprise"]

# E. Emotion Emojis
EMOTION_EMOJIS = {
    "sadness": "😢",
    "joy": "😄",
    "love": "❤️",
    "anger": "😠",
    "fear": "😨",
    "surprise": "😲",
}


# Text Preprocessing
def preprocess_text(text: str) -> str:

    text = text.lower()
    text = re.sub(r"'", "", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()

    return text


# Request Schema
class TextInput(BaseModel):

    text: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="The sentence to analyze",
        json_schema_extra={
            "example": "I feel so happy and excited"
        }
    )


# Prediction Response Schema
class PredictionResponse(BaseModel):

    text: str
    predicted_emotion: str
    confidence: float
    all_probabilities: dict[str, float]


# Health Response Schema
class HealthResponse(BaseModel):

    status: str
    model_loaded: bool


# Model Storage
dl_model = {}


# Model Loading and Unloading
@asynccontextmanager
async def lifespan(app: FastAPI):

    print("Loading the model and tokenizer...")

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found: {model_path}")

    if not os.path.exists(tokenizer_path):
        raise FileNotFoundError(f"Tokenizer not found: {tokenizer_path}")

    dl_model["BiGRU"] = load_model(model_path)

    with open(tokenizer_path, "rb") as file:
        dl_model["Tokenizer"] = pickle.load(file)

    print("Model and tokenizer loaded successfully!")

    yield

    dl_model.clear()

    print("Model resources released.")


# FastAPI Application
app = FastAPI(
    title="Emote Lens API",
    description="Text-based Emotion Detection using BiGRU",
    version="1.0.0",
    lifespan=lifespan
)


# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Static Files
app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# A. Homepage
@app.get("/", include_in_schema=False)
def server_ui():

    return FileResponse("static/index.html")


# B. Health Check
@app.get("/health", response_model=HealthResponse)
def health_check():

    return HealthResponse(
        status="Server is running",
        model_loaded=bool(dl_model)
    )


# C. Emotion Prediction
@app.post("/predict", response_model=PredictionResponse)
def predict_emotion(text_input: TextInput):

    """
    1. Clean the input sentence.
    2. Convert words into numerical sequences.
    3. Pad sequences to a fixed length.
    4. Predict emotion using BiGRU.
    5. Return predicted emotion and probabilities.
    """

    BiGRU_model = dl_model.get("BiGRU")
    tokenizer_model = dl_model.get("Tokenizer")

    if BiGRU_model is None or tokenizer_model is None:

        raise HTTPException(
            status_code=503,
            detail="Model is not loaded yet."
        )

    # 1. Text Preprocessing
    cleaned_text = preprocess_text(text_input.text)

    if not cleaned_text:
        raise HTTPException(
            status_code=422,
            detail="Please provide meaningful text."
        )

    # 2. Tokenization
    tokenized_text = tokenizer_model.texts_to_sequences(
        [cleaned_text]
    )

    # 3. Padding
    padded_sequence = pad_sequences(
        tokenized_text,
        maxlen=max_sequence_length,
        padding="post",
        truncating="post"
    )

    # 4. Prediction
    probabilities = BiGRU_model.predict(
        padded_sequence,
        verbose=0
    )[0]

    if len(probabilities) != len(emotion_labels):
        raise HTTPException(
            status_code=500,
            detail="Model output dimensions do not match emotion labels."
        )

    top_emotion_index = int(np.argmax(probabilities))

    # 5. Probability Breakdown
    all_probabilities = {
        label: float(prob)
        for prob, label in zip(probabilities, emotion_labels)
    }

    return PredictionResponse(

        text=text_input.text,

        predicted_emotion=emotion_labels[top_emotion_index],

        confidence=float(probabilities[top_emotion_index]),

        all_probabilities=all_probabilities

    )