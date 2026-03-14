# 🧠 AI-Based Silent Confusion Detection System: Knowledge Base

This document provides a comprehensive overview of the project for an AI assistant to understand the implementation details, architecture, and logic of the system.

## 🎯 Project Vision
The system detects "silent confusion" in students during video learning by fusing multimodal data (Webcam, Behavioral, Video Interaction) into a weighted confusion score. It triggers timely interventions (quizzes, recaps) when confusion exceeds a threshold.

## 🛠️ Technology Stack
- **Backend**: Python 3.8+, Flask, OpenCV, TensorFlow/FER.
- **Frontend**: HTML5, Vanilla CSS (Modern UI/Glassmorphism), Vanilla JavaScript.
- **Data**: CSV-based logging (supports SQLite migration).
- **Communication**: REST API (JSON).

## 🏗️ Core Architecture

### Backend Components (`/backend`)
- `app.py`: Entry point, routes blueprint registration, CORS configuration.
- `config.py`: Centralized configuration for weights, thresholds, and server settings.
- `models/`:
  - `emotion_model.py`: Uses `FER` library to detect facial expressions from base64 frames.
  - `behavior_model.py`: Calculates scores from mouse/keyboard/video events.
  - `fusion_engine.py`: The "Brain" - fuses scores using weighted average and temporal smoothing.
  - `recommendation.py`: Selects the best intervention based on the primary confusion factor.
- `api/`: REST endpoints for emotion, behavior, and intervention management.
- `utils/`: Logging and session management utilities.

### Frontend Components (`/frontend`)
- `index.html`: Dashboard with video player, webcam feed, and debug panel.
- `js/webcam.js`: Handles `getUserMedia` and periodic frame capture.
- `js/behavioral_tracker.js`: Event listeners for mouse, keyboard, and video interactions.
- `js/api_client.js`: Centralized `fetch` calls with session handling (UUID in `localStorage`).
- `js/intervention.js`: UI logic for popups and feedback collection.

## 🧠 Confusion Detection Algorithm

### 1. Scoring Weights
The system uses a weighted fusion model defined in `config.py`:
- **Emotion (40%)**: Facial cues (Sad, Fear, Angry are positive weights; Happy is negative).
- **Behavior (30%)**: Mouse inactivity, typing pauses, low typing speed.
- **Video Interaction (30%)**: Rewind frequency, pause counts, segment replay.

### 2. Temporal Smoothing
The `FusionEngine` maintains a moving average (window size = 5) of the raw scores to filter out momentary noise or distractions.

### 3. Intervention Logic
- **Threshold**: 60% (0.6).
- **Intervention Selection**:
  - `simpler_explanation`: Primary factor is Emotion.
  - `real_life_example`: Primary factor is Behavior.
  - `concept_recap`: Primary factor is Video.
  - `short_quiz`: Mixed signals or High overall score.
- **Cooldown**: 120 seconds between interventions to prevent annoyance.

## 📡 API Reference

| Endpoint | Method | Purpose | Key Request Fields | Key Response Fields |
|----------|--------|---------|--------------------|---------------------|
| `/api/emotion/detect` | `POST` | Face analysis | `image` (base64) | `emotions`, `confusion_score` |
| `/api/behavior/track` | `POST` | Action tracking | `mouse_data`, `video_data` | `overall_behavior_score` |
| `/api/intervention/check` | `POST` | Trigger check | `emotion_score`, `behavior_score` | `intervention_needed`, `recommendation` |
| `/api/intervention/feedback` | `POST` | Record utility | `intervention_type`, `was_helpful` | `success` |

## 📊 Data & Logs
Data is stored in `logs/` for academic analysis:
- `session_data.csv`: Timestamp, all component scores, final score, and trigger status.
- `feedback_data.csv`: Intervention type and whether the user marked it as helpful.

## 🚀 Running the Project
1. **Backend**: `pip install -r requirements.txt`, then `python backend/app.py`.
2. **Frontend**: Serve `frontend/index.html` via any web server (or open directly).
3. **Tests**: `python -m pytest tests/` or individual test scripts in `tests/`.
