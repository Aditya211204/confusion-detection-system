# AI-Based Silent Confusion Detection System - Project Documentation

**Purpose of this Document:** This file contains a comprehensive overview of the "AI-Based Silent Confusion Detection System". It is intended to be provided to an AI assistant to give it full context of the project, enabling it to answer questions, debug, or suggest improvements without needing to re-read the entire codebase.

---

## 1. Project Overview
This project is an intelligent learning assistant that detects **silent confusion** in students during video-based learning sessions. Unlike traditional systems that rely on quiz answers, this system detects confusion *implicitly* using multimodal signals:
1.  **Facial Expressions** (Emotion Recognition via Webcam)
2.  **Behavioral Patterns** (Mouse movements, hesitation, typing speed)
3.  **Video Interactions** (Pausing, rewinding, replaying)

When confusion is detected (score > 60%), the system automatically triggers a helpful **Intervention** (popup) to assist the learner.

## 2. System Architecture
The system follows a standard Client-Server architecture:

-   **Frontend**: HTML/CSS/JavaScript. Runs in the browser. Handles UI, webcam capture, event tracking, and displaying interventions.
-   **Backend**: Python (Flask). exposes REST APIs. Handles data processing, model inference, confusion fusion, and logging.

### Technnology Stack
-   **Frontend**: HTML5, CSS3, JavaScript (Vanilla), YouTube IFrame Player API.
-   **Backend**: Python 3.8+, Flask, OpenCV (for image processing), FER (Facial Emotion Recognition library).
-   **Data**: CSV logging (in `logs/` directory).

## 3. Core Logic & Algorithms

### 3.1 Confusion Fusion Algorithm
The core intelligence lies in the **Fusion Engine** (`backend/models/fusion_engine.py`). It calculates a single "Confusion Score" from three inputs:

**Formula:**
```python
Confusion_Score = (0.4 * Emotion_Score) + (0.3 * Behavior_Score) + (0.3 * Video_Score)
```

**Weights:**
-   **Emotion (40%)**: Primary indicator. Driven by 'Sad', 'Fear', 'Angry' expressions. 'Happy' reduces confusion.
-   **Behavior (30%)**: Derived from mouse hesitation, inactivity, and deletion keys (backspace).
-   **Video (30%)**: Derived from frequent pauses, rewinds, and replaying the same segment.

### 3.2 Temporal Smoothing
To prevent flickering (false positives), the system applies a **Moving Average** over the last 5 measurements.

### 3.3 Intervention Trigger
-   **Condition**: Smoothed Confusion Score ≥ **0.6 (60%)**.
-   **Action**: Returns an intervention payload to the frontend containing a helpful message or resource.

## 4. File Structure & Responsibilities

### Root Directory
-   `README.md`: High-level user documentation.
-   `requirements.txt`: Python dependencies.

### Backend (`/backend`)
-   `app.py`: **Entry Point**. Flask application factory. Registers blueprints and sets up CORS.
-   `config.py`: Central configuration (weights, thresholds, API ports).
-   `api/`: Route handlers.
    -   `emotion_api.py`: Endpoint `/api/emotion/detect`. Receives base64 image -> Returns emotion score.
    -   `behavior_api.py`: Endpoint `/api/behavior/track`. Receives tracking data -> Returns behavior score.
    -   `intervention_api.py`: Endpoint `/api/intervention/check`. Calls Fusion Engine.
-   `models/`: Core logic.
    -   `fusion_engine.py`: **CRITICAL**. Implements the fusion equation and smoothing logic.
    -   `emotion_model.py`: Wraps the FER library.
    -   `behavior_model.py`: Heuristics for behavior analysis.
    -   `recommendation.py`: Selects which intervention to show based on the confusion source.
-   `utils/`:
    -   `logger.py`: Writes session data to CSV files in `logs/`.

### Frontend (`/frontend`)
-   `index.html`: Main UI. Contains the YouTube Player `div`, webcam preview, and debug panel.
-   `js/`:
    -   `api_client.js`: **Bridge**. Handles all `fetch` requests to the Flask backend. Manages Session IDs.
    -   `behavioral_tracker.js`: **Complex Logic**. Tracks mouse/keyboard events. **Crucially**, it integrates with the **YouTube IFrame API** to track video state (Play, Pause, "Seek" detection via time monitoring).
    -   `webcam.js`: Manages `getUserMedia`, captures frames, and sends them to the backend.
    -   `intervention.js`: UI logic for showing/hiding the intervention popup.

## 5. Data Flow Example
1.  **Frontend**: `webcam.js` captures a frame every 3 seconds.
2.  **API**: Sends frame to `/api/emotion/detect`.
3.  **Backend**: `emotion_model.py` analyzes face. Returns `emotion_score`.
4.  **Frontend**: `behavioral_tracker.js` aggregates mouse/key/video events over 5 seconds.
5.  **API**: Sends metrics to `/api/behavior/track`.
6.  **Backend**: `behavior_model.py` calculates `behavior_score` and `video_score`.
7.  **Auto-Check**: The system periodically calls `/api/intervention/check` with all three current scores.
8.  **Backend**: `fusion_engine.py` computes the weighted average, smooths it, and checks threshold (0.6).
9.  **Response**: If threshold met, returns `intervention_needed: true` and recommendation content.
10. **Frontend**: `intervention.js` displays the popup.

## 6. Known Context & Recent Changes
-   **Video Source**: The project was recently migrated from a local `<video>` file to using the **YouTube IFrame Player API**. logic for tracking "rewinds" was custom-implemented in `behavioral_tracker.js` by polling the current time, as the YouTube API does not have a native 'seeked' event.
