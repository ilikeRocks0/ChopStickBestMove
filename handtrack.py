import cv2
import mediapipe as mp
import numpy as np

# Function to load CSV into a 2D array
def load_csv_to_array(file_path):
    return np.genfromtxt(file_path, delimiter=',')

# Function to map hand counts to index
def index(i):
    match i:
        case (1, 1):
            return 0
        case (2, 1) | (1, 2):
            return 1
        case (3, 1) | (1, 3):
            return 2
        case (4, 1) | (1, 4):
            return 3
        case (0, 1) | (1, 0):
            return 4
        case (2, 2):
            return 5
        case (3, 2) | (2, 3):
            return 6
        case (4, 2) | (2, 4):
            return 7
        case (0, 2) | (2, 0):
            return 8
        case (3, 3):
            return 9
        case (4, 3) | (3, 4):
            return 10
        case (0, 3) | (3, 0):
            return 11
        case (4, 4):
            return 12
        case (0, 4) | (4, 0):
            return 13
        case (0, 0):
            return 14
    return -1
    # raise ValueError("ERROR: INDEX INPUTTED NUMBER GREATER THAN 15!!!")

# Load the CSV files as 2D arrays
array0 = load_csv_to_array('slice_t0.csv')
array1 = load_csv_to_array('slice_t1.csv')
print(array0)
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

    # Count fingers on the left side
    if left_result.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(left_result.multi_hand_landmarks):
            mp_drawing.draw_landmarks(left_side, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingers_up = count_fingers(hand_landmarks)
            left_finger_counts.append(fingers_up)

    # Count fingers on the right side
    if right_result.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(right_result.multi_hand_landmarks):
            mp_drawing.draw_landmarks(right_side, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingers_up = count_fingers(hand_landmarks)
            right_finger_counts.append(fingers_up)

    # Ensure exactly two hand counts per side
    while len(left_finger_counts) < 2:
        left_finger_counts.append(0)
    while len(right_finger_counts) < 2:
        right_finger_counts.append(0)

    team1_value = -1
    team2_value = -1
    # Calculate the team indices
    team1 = index(tuple(left_finger_counts))
    team2 = index(tuple(right_finger_counts))
    if(team1 != -1 and team2 != -1):
        team1_value = array0[team1][team2]
        team2_value = array1[team1][team2]

    # Display the results from the array


    # Combine the two sides back into a single frame
    combined_frame = cv2.hconcat([left_side, right_side])

    # Display structured information on the left side
    cv2.putText(combined_frame, f'Team 1: {team1_value:.2f}%', (10, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(combined_frame, f'Hands: {tuple(left_finger_counts)}', (10, 100), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    # Display structured information on the right side
    cv2.putText(combined_frame, f'Team 2: {team2_value:.2f}%', (width//2 + 10, 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
    cv2.putText(combined_frame, f'Hands: {tuple(right_finger_counts)}', (width//2 + 10, 100), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # Display the frame
    cv2.imshow('Hand Tracking - Team 1 (Left) vs Team 2 (Right)', combined_frame)

    # Break loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
