import cv2
from ultralytics import YOLO

# Initialize the YOLO model
model = YOLO('yolov8m-pose.pt')

# Initialize pushup count and state
pushup_count = 0
is_down = False
ELBOW_ANGLE_THRESHOLD = 90
def calculate_elbow_angle(keypoints):
    # Example implementation (you need to replace this with actual logic)
    # This is just a placeholder
    return 90
def is_down_position(keypoints):
    elbow_angle = calculate_elbow_angle(keypoints)
    return elbow_angle > ELBOW_ANGLE_THRESHOLD

def is_up_position(keypoints):
    # Hypothetical condition: Check if arms are relatively straight
    elbow_angle = calculate_elbow_angle(keypoints)
    return elbow_angle < ELBOW_ANGLE_THRESHOLD

def analyze_pose_and_count(keypoints):
    global pushup_count, is_down
    if is_down_position(keypoints) and not is_down:
        is_down = True
    elif is_up_position(keypoints) and is_down:
        is_down = False
        pushup_count = pushup_count + 1 if pushup_count is not None else 1
    return pushup_count

# Initialize video capture
cap = cv2.VideoCapture(1)  # Change 1 to 0 for default webcam

# Initialize video writer
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Perform pose estimation
    results = model(frame)

    if results and hasattr(results[0], 'keypoints'):
        keypoints = results[0].keypoints
        # Analyze keypoints and update pushup count
        current_count = analyze_pose_and_count(keypoints)

        # Display the pushup count on the frame
        cv2.putText(frame, f'Pushups: {current_count if current_count is not None else 0}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

    # Write the frame to the output video file
    out.write(frame)

    # Display the frame
    cv2.imshow('Pushup Counter', frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
out.release()
cv2.destroyAllWindows()
