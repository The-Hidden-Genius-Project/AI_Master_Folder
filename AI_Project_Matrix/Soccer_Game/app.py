import cv2

import numpy as np



# Load the pre-trained MobileNet SSD model and the class labels

prototxt = 'deploy.prototxt'  # Path to the .prototxt file

model = 'mobilenet_iter_73000.caffemodel'  # Path to the .caffemodel file

net = cv2.dnn.readNetFromCaffe(prototxt, model)



# Function to detect the sports ball

def detect_ball(frame):

    # Get the height and width of the frame

    (h, w) = frame.shape[:2]

    

    # Preprocess the frame and create a blob

    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 0.007843, (300, 300), 127.5)

    

    # Set the blob as input to the model

    net.setInput(blob)

    

    # Perform forward pass to get detections

    detections = net.forward()

    

    ball_position = None

    

    # Loop over the detections

    for i in range(detections.shape[2]):

        confidence = detections[0, 0, i, 2]

        

        # Filter out weak detections

        if confidence > 0.2:

            idx = int(detections[0, 0, i, 1])

            

            # Check if the detected object is a sports ball

            if idx == 37:  # The class label ID for sports ball in COCO dataset

                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])

                (startX, startY, endX, endY) = box.astype("int")

                

                # Calculate the centroid of the detected ball

                ball_position = ((startX + endX) // 2, (startY + endY) // 2)

                break

    

    return ball_position



# Function to simulate AI player movement

def ai_player_movement(frame, ball_position, player_position, player_trail):

    player_x, player_y = player_position

    

    # If ball position is detected

    if ball_position is not None:

        ball_x, ball_y = ball_position

        

        # Calculate movement direction towards the ball

        dx = ball_x - player_x

        dy = ball_y - player_y

        

        # Normalize movement direction

        if dx != 0 or dy != 0:

            norm = np.sqrt(dx**2 + dy**2)

            speed_multiplier = 10

            dx = int(speed_multiplier * dx / norm)

            dy = int(speed_multiplier * dy / norm)

        

        # Update player position

        player_x = max(0, min(player_x + dx, frame.shape[1] - 1))

        player_y = max(0, min(player_y + dy, frame.shape[0] - 1))

        

        # Update player trail with previous position

        player_trail.append((player_x, player_y))

        

        # Limit the trail length

        while len(player_trail) > 20:

            player_trail.pop(0)

        

        # Draw player trail with fading effect

        for i in range(len(player_trail) - 1):

            alpha = int(255 * (i + 1) / len(player_trail))

            cv2.line(frame, player_trail[i], player_trail[i+1], (0, 255, 0), 2)

    

    return player_x, player_y



# Main function

def main():

    # Open video capture device

    cap = cv2.VideoCapture(0)

    

    # Initialize player position and player trail

    player_position = (50, 240)  # Initial position of the AI player

    player_trail = []

    

    while True:

        # Read frame from the camera

        ret, frame = cap.read()

        if not ret:

            break

        

        # Flip the frame horizontally for easier movement simulation

        frame = cv2.flip(frame, 1)

        

        # Detect the sports ball in the frame

        ball_position = detect_ball(frame)

        

        # Simulate AI player movement

        player_position = ai_player_movement(frame, ball_position, player_position, player_trail)

        

        # Draw player

        cv2.rectangle(frame, (player_position[0] - 20, player_position[1] - 50), (player_position[0] + 20, player_position[1] + 50), (0, 255, 0), -1)

        

        # Draw ball (if detected)

        if ball_position is not None:

            cv2.circle(frame, ball_position, 10, (0, 0, 255), -1)

        

        # Display the frame

        cv2.imshow('Soccer Game', frame)

        

        # Check for 'q' key press to exit

        if cv2.waitKey(1) & 0xFF == ord('q'):

            break

        

    # Release video capture device and close windows

    cap.release()

    cv2.destroyAllWindows()



if __name__ == "__main__":

    main()