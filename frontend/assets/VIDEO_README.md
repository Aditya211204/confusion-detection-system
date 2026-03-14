# Sample Video Note

## Important: Add Your Own Learning Video

The system is designed to work with any educational video. To add your own video:

1. **Place your video file** in the `frontend/assets/` folder
2. **Rename it** to `sample_video.mp4` (or update the path in `index.html`)
3. **Supported formats**: MP4, WebM, OGG

## Recommended Video Characteristics

- **Duration**: 5-15 minutes (for testing)
- **Content**: Any educational topic (programming, math, science, etc.)
- **Quality**: 720p or higher recommended
- **Size**: Keep under 100MB for smooth playback

## Alternative: Use YouTube Video

If you don't have a local video, you can modify `index.html` to use a YouTube embed:

```html
<!-- Replace the video tag with: -->
<iframe 
    id="learningVideo" 
    width="100%" 
    height="100%" 
    src="https://www.youtube.com/embed/y4JcRWR4rUg?enablejsapi=1"
    frameborder="0" 
    allowfullscreen>
</iframe>
```

## For Demo/Testing

You can use any of these free educational videos:
- Khan Academy videos
- MIT OpenCourseWare
- Coursera sample lectures
- Your own recorded lectures

## Note for Academic Evaluation

For your project demonstration, use a video that:
1. Is relevant to your field of study
2. Has moderate complexity (to naturally induce some confusion)
3. Is long enough to demonstrate the system (5+ minutes)
4. You can explain the content during viva

The video content itself is not evaluated - the focus is on the AI system's ability to detect confusion regardless of the subject matter.
