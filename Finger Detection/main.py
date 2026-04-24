import cv2
import mediapipe as mp
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)

# Gesture mapping
gestures = {
    0: 'None',
    1: 'Start',
    2: 'Two',
    3: 'Three',
    4: 'Four',
    5: 'Stop'
}

def count_fingers(hand_landmarks):
    """
    Count the number of raised fingers based on hand landmarks.
    Assumes hand is facing the camera with palm towards it.
    """
    fingers = []

    # Thumb: Check if tip (4) is to the left of IP joint (3) for right hand, or adjust for left
    # For simplicity, use y-coordinate: if tip is above IP
    fingers.append(hand_landmarks.landmark[4].y < hand_landmarks.landmark[3].y)

    # Index finger: Tip (8) above PIP (6)
    fingers.append(hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y)

    # Middle finger: Tip (12) above PIP (10)
    fingers.append(hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y)

    # Ring finger: Tip (16) above PIP (14)
    fingers.append(hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y)

    # Pinky: Tip (20) above PIP (18)
    fingers.append(hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y)

    return sum(fingers)

def draw_hand(frame, hand_landmarks):
    """
    Draw hand landmarks and bounding box on the frame.
    """
    # Draw landmarks
    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Calculate bounding box
    h, w, c = frame.shape
    x_coords = [lm.x * w for lm in hand_landmarks.landmark]
    y_coords = [lm.y * h for lm in hand_landmarks.landmark]
    x_min, x_max = int(min(x_coords)), int(max(x_coords))
    y_min, y_max = int(min(y_coords)), int(max(y_coords))

    # Draw bounding box
    cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

def main():
    # Initialize webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    prev_time = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Failed to capture frame.")
            break

        # Flip frame horizontally for mirror effect
        frame = cv2.flip(frame, 1)

        # Convert to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            # Process the first hand
            hand_landmarks = results.multi_hand_landmarks[0]
            draw_hand(frame, hand_landmarks)
            finger_count = count_fingers(hand_landmarks)
            gesture = gestures.get(finger_count, 'Unknown')

            # Display finger count and gesture
            cv2.putText(frame, f'Fingers: {finger_count}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            cv2.putText(frame, f'Gesture: {gesture}', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        else:
            # No hand detected
            cv2.putText(frame, 'No hand detected', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Calculate and display FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time != 0 else 0
        prev_time = curr_time
        cv2.putText(frame, f'FPS: {int(fps)}', (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Show frame
        cv2.imshow('Finger Detection', frame)

        # Exit on 'q' key
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    cap.release()
    cv2.destroyAllWindows()
    hands.close()

if __name__ == "__main__":
    main()