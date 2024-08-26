import cv2
import mediapipe as mp

# Initialize MediaPipe Hand module
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=4)  # Track up to 4 hands
mp_drawing = mp.solutions.drawing_utils

def count_fingers(hand_landmarks):
    """
    Function to count the number of fingers held up (excluding thumb).
    :param hand_landmarks: Detected hand landmarks.
    :return: Number of fingers held up (excluding thumb).
    """
    # Fingers
    fingers = [
        hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y,
        hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y,
        hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.RING_FINGER_PIP].y,
        hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_TIP].y < hand_landmarks.landmark[mp_hands.HandLandmark.PINKY_PIP].y,
    ]
    
    # Count the number of fingers that are held up
    count = fingers.count(True)
    
    return count

# Open the camera
cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for a later selfie-view display
    frame = cv2.flip(frame, 1)
    height, width, _ = frame.shape

    # Split the frame into two sides: left and right
    left_side = frame[:, :width//2]
    right_side = frame[:, width//2:]

    # Convert both sides to RGB for processing
    left_rgb = cv2.cvtColor(left_side, cv2.COLOR_BGR2RGB)
    right_rgb = cv2.cvtColor(right_side, cv2.COLOR_BGR2RGB)

    # Process both sides separately
    left_result = hands.process(left_rgb)
    right_result = hands.process(right_rgb)

    # Initialize finger count displays
    left_finger_counts = []
    right_finger_counts = []

    # Process the left side
    if left_result.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(left_result.multi_hand_landmarks):
            mp_drawing.draw_landmarks(left_side, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingers_up = count_fingers(hand_landmarks)
            left_finger_counts.append(f"Hand {idx+1}: {fingers_up} Fingers")

    # Process the right side
    if right_result.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(right_result.multi_hand_landmarks):
            mp_drawing.draw_landmarks(right_side, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingers_up = count_fingers(hand_landmarks)
            right_finger_counts.append(f"Hand {idx+1}: {fingers_up} Fingers")

    # Combine the two sides back into a single frame
    combined_frame = cv2.hconcat([left_side, right_side])

    # Display labels on the left side
    for i, text in enumerate(left_finger_counts):
        cv2.putText(combined_frame, text, (10, 50 + i * 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    # Display labels on the right side
    for i, text in enumerate(right_finger_counts):
        cv2.putText(combined_frame, text, (width//2 + 10, 50 + i * 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # Display the frame
    cv2.imshow('Hand Tracking - Team 1 (Left) vs Team 2 (Right)', combined_frame)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
