# Real-Time Finger Detection System

## Project Overview
This project implements a real-time finger detection system using OpenCV and MediaPipe. It captures video from a webcam, detects a single hand, counts the number of raised fingers (0-5), and displays the results on screen. The system includes bounding boxes, hand landmarks, finger count, gesture mapping, and FPS display. It is optimized for real-time performance and handles various edge cases.

## Setup Instructions
1. Ensure Python 3.7+ is installed.
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   python main.py
   ```
4. Press 'q' to quit.

## Requirements
- Python 3.7+
- Webcam
- OpenCV
- MediaPipe

## Features
- Real-time hand detection and tracking
- Finger counting (0-5 fingers)
- Gesture mapping (e.g., 1 finger = "Start", 5 fingers = "Stop")
- Bounding box and landmark visualization
- FPS display
- Edge case handling (no hand, multiple hands, partial visibility)
- Robust to different lighting conditions

## Explanation of Algorithm
The system uses MediaPipe's hand tracking model to detect hand landmarks (21 key points per hand). Finger counting is based on the relative positions of these landmarks:

- **Thumb**: Checks if the tip (landmark 4) is above the IP joint (landmark 3) in the y-direction.
- **Other fingers**: Checks if the fingertip is above the PIP joint for index (8 vs 6), middle (12 vs 10), ring (16 vs 14), and pinky (20 vs 18).

This assumes the hand is oriented with the palm facing the camera. The count is the sum of raised fingers.

Bounding box is calculated from the min/max x,y coordinates of all landmarks.

## Possible Improvements
- Improve finger counting accuracy for different hand orientations.
- Add support for multiple hands with selection.
- Implement more complex gestures.
- Add audio feedback or integration with other systems.
- Optimize for mobile devices.
- Use GPU acceleration for better performance.