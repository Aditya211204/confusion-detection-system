# AI-Based Silent Confusion Detection System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.3.0-green.svg)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13.0-orange.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## 🎓 Project Overview

An intelligent AI-powered learning assistant that detects **silent confusion** in students during video-based learning without requiring explicit questions. The system uses multimodal analysis combining facial expressions, behavioral patterns, and video interaction data to provide timely, adaptive interventions.

**Academic Context**: B.Tech Major Project (ES-452) - Development-Based

## ✨ Key Features

- 🎭 **Facial Emotion Recognition**: Real-time emotion detection using webcam
- 🖱️ **Behavioral Analysis**: Mouse movement, keyboard typing, and video interaction tracking
- 🧠 **Intelligent Fusion**: Weighted combination of multiple confusion signals
- 💡 **Adaptive Interventions**: Smart recommendations that learn from user feedback
- 📊 **Explainable AI**: Clear explanations for why confusion was detected
- 📈 **Session Logging**: Comprehensive data logging for analysis

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (HTML/CSS/JS)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Video Player │  │ Webcam Feed  │  │ Intervention │      │
│  │              │  │              │  │    Popup     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↕ REST API
┌─────────────────────────────────────────────────────────────┐
│                   Backend (Flask Server)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ Emotion API  │  │ Behavior API │  │Intervention  │      │
│  │              │  │              │  │     API      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                      AI Processing Modules                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Emotion    │  │  Behavioral  │  │   Fusion     │      │
│  │ Recognition  │  │   Analysis   │  │   Engine     │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│                    ┌──────────────┐                         │
│                    │Recommendation│                         │
│                    │    Engine    │                         │
│                    └──────────────┘                         │
└─────────────────────────────────────────────────────────────┘
```

## 📁 Project Structure

```
confusion-detection-system/
├── backend/
│   ├── app.py                    # Flask main application
│   ├── config.py                 # Configuration settings
│   ├── models/
│   │   ├── emotion_model.py      # Emotion recognition (FER)
│   │   ├── behavior_model.py     # Behavioral analysis
│   │   ├── fusion_engine.py      # Confusion score fusion
│   │   └── recommendation.py     # Recommendation engine
│   ├── api/
│   │   ├── emotion_api.py        # Emotion endpoints
│   │   ├── behavior_api.py       # Behavioral endpoints
│   │   └── intervention_api.py   # Intervention endpoints
│   └── utils/
│       ├── logger.py             # Data logging
│       └── session.py            # Session management
├── frontend/
│   ├── index.html                # Main interface
│   ├── css/style.css             # Modern styling
│   └── js/
│       ├── webcam.js             # Webcam capture
│       ├── behavioral_tracker.js # Behavior tracking
│       ├── intervention.js       # Popup logic
│       └── api_client.js         # Backend communication
├── tests/
│   ├── test_emotion.py           # Emotion tests
│   ├── test_behavior.py          # Behavioral tests
│   └── test_fusion.py            # Fusion tests
├── logs/                         # Session data logs
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## 🚀 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Webcam (for emotion detection)
- Modern web browser (Chrome/Firefox recommended)

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd confusion-detection-system
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask backend**
   ```bash
   cd backend
   python app.py
   ```
   
   The server will start at `http://127.0.0.1:5000`

5. **Open the frontend**
   - Open `frontend/index.html` in your web browser
   - Allow webcam access when prompted
   - Start learning!

## 🎮 Usage

1. **Start Learning Session**
   - Open the application in your browser
   - Grant webcam permissions
   - Play the learning video

2. **System Monitors**
   - Facial expressions (every 3 seconds)
   - Mouse and keyboard activity (every 5 seconds)
   - Video interactions (pause, rewind, replay)

3. **Intervention Popup**
   - Appears when confusion score > 60%
   - Provides helpful suggestions
   - Give feedback (helpful/dismiss)

4. **View Debug Info**
   - Bottom-right panel shows real-time scores
   - Monitor emotion, behavior, and video scores
   - Track intervention count

## 🧪 Testing

Run the test suite to verify all modules:

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python tests/test_emotion.py
python tests/test_behavior.py
python tests/test_fusion.py
```

## 📊 Confusion Detection Algorithm

### Confusion Score Calculation

```
Confusion Score = 0.4 × Emotion_Score + 0.3 × Behavior_Score + 0.3 × Video_Score
```

**Emotion Score** (from facial expressions):
- Sad: 0.5 weight
- Fear: 0.4 weight
- Angry: 0.3 weight
- Happy: -0.2 weight (reduces confusion)

**Behavior Score** (from user actions):
- Mouse inactivity (>30s)
- Keyboard pauses (>15s)
- Low typing speed (<20 cpm)

**Video Score** (from interactions):
- Pause frequency (>5 in 5 min)
- Rewind count (>3 in 5 min)
- Segment replays (>2)

### Temporal Smoothing

Moving average over 5 measurements to reduce false positives.

### Intervention Trigger

Intervention shown when smoothed confusion score ≥ 0.6 (60%)

## 🎯 Intervention Types

1. **Simpler Explanation** - For emotion-based confusion
2. **Real-Life Example** - For behavior-based confusion
3. **Concept Recap** - For video-based confusion
4. **Short Quiz** - For mixed confusion signals

## 📈 Data Logging

Session data is automatically logged to `logs/session_data.csv`:
- Timestamp
- Emotion, behavior, and video scores
- Confusion scores (raw and smoothed)
- Intervention triggers
- Primary confusion factors

Feedback data logged to `logs/feedback_data.csv`:
- Intervention type
- User feedback (helpful/dismissed)
- Confusion score at intervention time

## 🔧 Configuration

Edit `backend/config.py` to customize:
- Emotion detection thresholds
- Behavioral analysis parameters
- Fusion weights
- Intervention cooldown period
- Logging settings

## 📚 Academic Deliverables

This project supports the following B.Tech report chapters:

1. **Introduction** - Problem statement and objectives
2. **Literature Review** - AI in education, emotion recognition
3. **System Analysis** - Requirements and feasibility
4. **System Design** - Architecture and algorithms
5. **Implementation** - Code with detailed comments
6. **Testing** - Unit tests and validation results
7. **Results** - Screenshots and session logs
8. **Conclusion** - Achievements and future scope

## 🎨 UI Features

- Modern glassmorphism design
- Smooth animations and transitions
- Responsive layout
- Real-time confusion score visualization
- Debug panel for development

## 🔮 Future Enhancements

- [ ] LLM integration for dynamic explanations
- [ ] Multi-user support with authentication
- [ ] Advanced analytics dashboard
- [ ] Mobile app version
- [ ] Integration with LMS platforms
- [ ] Voice-based confusion detection
- [ ] Personalized learning paths

## 📝 License

MIT License - Free for academic and educational use

## 👨‍💻 Author

B.Tech Major Project (ES-452)  
Development-Based Implementation

## 🙏 Acknowledgments

- FER library for emotion recognition
- Flask framework for backend
- OpenCV for image processing
- Academic mentors and guides

---

**Note**: This system is designed for educational purposes and demonstration. For production use, additional security, scalability, and privacy measures should be implemented.
