# Emote Lens — AI-Powered Text Emotion Detection

<p align="center">
  <strong>Read the feeling behind the words.</strong>
</p>

<p align="center">
  An end-to-end Deep Learning application that detects emotions in text using a Bidirectional Gated Recurrent Unit (BiGRU) model.
</p>

<p align="center">
  <a href="https://emote-lens-2.onrender.com/">🚀 Live Demo</a> |
  <a href="https://github.com/tejussaini/Emote-Lens">GitHub Repository</a>
</p>

---

## Overview

**Emote Lens** is an AI-powered text emotion detection application designed to identify the emotional tone behind written text.

Built using a trained **Bidirectional Gated Recurrent Unit (BiGRU)** deep learning model, the application analyzes user-provided text and classifies it into six different emotion categories.

Users can enter a sentence or paragraph and receive the predicted emotion, model confidence score, and probability distribution across all six emotion categories.

The project combines Deep Learning, Natural Language Processing (NLP), FastAPI, and modern web technologies to deliver an interactive emotion classification experience.

## Live Demo

🌐 **Try Emote Lens:** https://emote-lens-2.onrender.com/

---

## Supported Emotions

Emote Lens recognizes six emotion categories:

| Emotion | Description | Emoji |
|---|---|---|
| Sadness | Expressions of sorrow or disappointment | 😢 |
| Joy | Expressions of happiness or excitement | 😄 |
| Love | Expressions of affection or attachment | ❤️ |
| Anger | Expressions of frustration or irritation | 😠 |
| Fear | Expressions of worry or apprehension | 😨 |
| Surprise | Expressions of unexpected events or reactions | 😲 |

---

## Key Features

- **Six-Class Emotion Classification:** Identifies sadness, joy, love, anger, fear, and surprise.
- **BiGRU Deep Learning Model:** Uses bidirectional recurrent neural networks to process textual sequences.
- **Text Preprocessing:** Cleans and normalizes input text before tokenization.
- **Automated Tokenization:** Converts text into numerical sequences using a trained tokenizer.
- **Sequence Padding:** Standardizes input sequences to a maximum length of 50 tokens.
- **Prediction Confidence:** Displays the confidence score of the predicted emotion.
- **Probability Distribution:** Visualizes prediction probabilities for all six emotions.
- **Interactive Web Interface:** Provides a modern, responsive interface with sample inputs and character counting.
- **REST API:** Uses FastAPI to expose prediction and health-check endpoints.
- **Cloud Deployment:** Deployed using Render.

---

## Technology Stack

### Machine Learning & Deep Learning
- Python
- TensorFlow
- Keras
- Bidirectional GRU (BiGRU)
- NumPy

### Natural Language Processing
- Text Preprocessing
- Tokenization
- Sequence Padding
- Emotion Classification

### Backend
- FastAPI
- Uvicorn
- Pydantic

### Frontend
- HTML5
- CSS3
- JavaScript

### Deployment & Version Control
- Render
- Git
- GitHub

---

## Project Architecture

```text
                    USER INPUT
                        |
                        v
                FRONTEND INTERFACE
                 HTML / CSS / JS
                        |
                        v
                  FASTAPI BACKEND
                        |
                        v
                 TEXT PREPROCESSING
                        |
                        v
                    TOKENIZER
                        |
                        v
                  SEQUENCE PADDING
                   Max Length: 50
                        |
                        v
                 TRAINED BiGRU MODEL
                        |
                        v
                 EMOTION PREDICTION
                        |
                        v
              PROBABILITY DISTRIBUTION
                        |
                        v
                  JSON RESPONSE
                        |
                        v
                 RESULTS DISPLAY
```

---

## How It Works

The application follows a sequential emotion prediction pipeline.

### 1. User Input

The user enters text through the Emote Lens web interface.

The application accepts input between 1 and 2,000 characters.

### 2. Text Preprocessing

The input text undergoes preprocessing operations:

- Converts text to lowercase.
- Removes apostrophes.
- Removes special characters.
- Normalizes whitespace.

### 3. Tokenization

The preprocessed text is converted into numerical sequences using the saved tokenizer.

### 4. Sequence Padding

The numerical sequences are padded or truncated to a fixed length of 50 tokens.

### 5. BiGRU Prediction

The processed sequence is passed to the trained BiGRU deep learning model.

The model generates prediction probabilities for all six emotion categories.

### 6. Result Generation

The application identifies the emotion with the highest prediction probability.

The final response includes:
- Predicted emotion.
- Confidence score.
- Probability distribution across all six emotions.

---

## Project Structure

```text
Emote-Lens/
│
├── Artifacts/
│   ├── BiGRU_Model.keras
│   └── tokenizer.pkl
│
├── static/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── main.py
├── requirements.txt
├── runtime.txt
├── .python-version
└── README.md
```

---

## Installation and Setup

Follow these steps to run Emote Lens locally.

### 1. Clone the Repository

```bash
git clone https://github.com/tejussaini/Emote-Lens.git
```

### 2. Navigate to the Project Directory

```bash
cd Emote-Lens
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

**Linux / macOS:**

```bash
source venv/bin/activate
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the FastAPI Application

```bash
python -m uvicorn main:app --reload
```

### 7. Access the Application

Once the server starts, open:

| Service | URL |
|---|---|
| Web Application | http://127.0.0.1:8000 |
| API Documentation | http://127.0.0.1:8000/docs |
| Health Check | http://127.0.0.1:8000/health |

---

## API Documentation

The backend provides three primary endpoints.

### 1. Homepage

**Endpoint:**

```http
GET /
```

Serves the Emote Lens web application.

### 2. Health Check

**Endpoint:**

```http
GET /health
```

Checks whether the API is running and whether the deep learning model is loaded.

**Example Response:**

```json
{
  "status": "Server is running",
  "model_loaded": true
}
```

### 3. Emotion Prediction

**Endpoint:**

```http
POST /predict
```

Accepts text input and returns the predicted emotion.

**Example Request:**

```json
{
  "text": "I feel so happy and excited today!"
}
```

**Example Response:**

```json
{
  "text": "I feel so happy and excited today!",
  "predicted_emotion": "joy",
  "confidence": 0.94,
  "all_probabilities": {
    "sadness": 0.01,
    "joy": 0.94,
    "love": 0.02,
    "anger": 0.01,
    "fear": 0.01,
    "surprise": 0.01
  }
}
```

*Note: The numerical prediction values above are illustrative and do not represent measured model performance.*

---

## Deployment

Emote Lens is deployed using **Render**.

**Live Application:** https://emote-lens-2.onrender.com/

### Render Configuration

**Build Command:**

```bash
pip install -r requirements.txt
```

**Start Command:**

```bash
python -m uvicorn main:app --host 0.0.0.0 --port $PORT
```

The trained BiGRU model and tokenizer must be available in the `Artifacts/` directory during deployment.

---

## Future Improvements

Potential areas for further development:

- Improve model performance through hyperparameter tuning.
- Compare BiGRU with LSTM and Transformer-based architectures.
- Introduce multilingual emotion detection.
- Implement batch text prediction.
- Add prediction history and analytics.
- Explore explainability techniques for model predictions.
- Experiment with larger pretrained language models.

---

## Limitations

- The model currently supports six predefined emotion categories.
- Predictions depend on the quality and context of the input text.
- Sarcasm, irony, and complex emotional expressions may be difficult to classify accurately.
- Confidence scores represent model output probabilities, not certainty about a person's actual feelings.
- The application is intended for educational and experimental purposes, not psychological diagnosis.

---

## Author

**Tejus Saini**

AI/ML Developer | Deep Learning Enthusiast

- GitHub: https://github.com/tejussaini
- Project: https://github.com/tejussaini/Emote-Lens
- Live Demo: https://emote-lens-2.onrender.com/

---

<p align="center">
  Built with Python, TensorFlow, FastAPI and JavaScript.
</p>

<p align="center">
  <strong>Emote Lens — Read the feeling behind the words.</strong>
</p>