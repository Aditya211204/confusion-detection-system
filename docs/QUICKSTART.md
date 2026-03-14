# Quick Start Guide

## Installation (5 minutes)

1. **Install Python dependencies**
   ```bash
   cd confusion-detection-system
   pip install -r requirements.txt
   ```

2. **Start the backend**
   ```bash
   cd backend
   python app.py
   ```
   
   Wait for: `Server running at: http://127.0.0.1:5000`

3. **Open the frontend**
   - Open `frontend/index.html` in Chrome or Firefox
   - Allow webcam access
   - Done!

## First Run

1. Click play on the video
2. Watch the confusion score (right side)
3. Debug panel shows live scores
4. Simulate confusion to trigger intervention:
   - Pause video 5+ times, OR
   - Show sad expression to webcam, OR
   - Stop moving mouse for 30+ seconds

## Testing

```bash
# Run all tests
python tests/test_emotion.py
python tests/test_behavior.py
python tests/test_fusion.py
```

## Troubleshooting

**Webcam not working?**
- Check browser permissions
- Try Chrome (best compatibility)

**Backend errors?**
- Make sure all dependencies installed
- Check Python version (3.8+)

**No intervention appearing?**
- Check debug panel scores
- Try multiple confusion signals together
- Wait for scores to build up (temporal smoothing)

## For Demo/Viva

1. Start backend first
2. Open frontend
3. Explain the architecture while system initializes
4. Show normal usage
5. Trigger intervention by pausing video multiple times
6. Show feedback mechanism
7. Show session logs in `logs/session_data.csv`
8. Show code comments for key modules

## Key Files to Explain

- `backend/models/fusion_engine.py` - Core algorithm
- `backend/config.py` - All thresholds
- `frontend/js/behavioral_tracker.js` - Tracking logic
- `logs/session_data.csv` - Data output
