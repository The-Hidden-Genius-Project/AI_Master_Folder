import requests
import tensorflow as tf
import numpy as np
import cv2
from tkinter import Tk, Button, Label
import time

# Base URL for the music control service
BASE_URL = "http://localhost:10767/api/v1/playback"

# Define the endpoint paths
ENDPOINTS = {
    'skip': f"{BASE_URL}/next",
    'playpause': f"{BASE_URL}/playpause",
    'previous': f"{BASE_URL}/previous",
    'currentsong': f"{BASE_URL}/currentPlayingSong",
    'status': f"{BASE_URL}/status"  # Endpoint to check playback status,
}

# Function to send a POST request for playback actions and GET request for current song
def send_request(action):
    try:
        if action == 'currentsong':
            response = requests.get(ENDPOINTS[action])
            if response.status_code == 200:
                return response.json().get('name', 'Unknown Song')
            else:
                print(f"Failed to retrieve current song. Status Code: {response.status_code}, Response: {response.text}")
                return "Error retrieving song"
        elif action == 'status':
            response = requests.get(ENDPOINTS[action])
            if response.status_code == 200:
                return response.json().get('playbackState', 'UNKNOWN')
            else:
                print(f"Failed to retrieve playback status. Status Code: {response.status_code}, Response: {response.text}")
                return "UNKNOWN"
        else:
            response = requests.post(ENDPOINTS[action])
            if response.status_code in [200, 204]:
                print(f"{action.capitalize()} action performed successfully.")
                return None
            else:
                print(f"Failed to perform {action} action. Status Code: {response.status_code}, Response: {response.text}")
                return None
    except Exception as e:
        print(f"Request error: {e}")
        return None

# Load the Teachable Machine model
class InferenceModel(tf.keras.Model):
    def __init__(self, saved_model_path):
        super(InferenceModel, self).__init__()
        self.tf_layer = tf.saved_model.load(saved_model_path)
    
    def call(self, inputs, training=False):
        return self.tf_layer(inputs)

# Function to load the model
def load_model(model_path):
    try:
        model = InferenceModel(model_path)
        print("Model loaded successfully.")
        return model
    except Exception as e:
        print(f"Model could not be loaded: {e}")
        return None

# Make sure to replace this with the actual path to your model
model_path = '/Users/demetriousbrown/Downloads/Realmodel/model.savedmodel'
model = load_model(model_path)
model_loaded = model is not None

def make_prediction(input_data):
    if model_loaded:
        try:
            input_data = np.expand_dims(input_data, axis=0)
            tf_input = tf.convert_to_tensor(input_data, dtype=tf.float32)
            prediction = model(tf_input, training=False)
            predicted_class = np.argmax(prediction.numpy(), axis=1)  # .numpy() to convert tensors to numpy arrays
            confidence = np.max(prediction.numpy(), axis=1)
            return predicted_class[0], confidence[0]
        except Exception as e:
            print(f"Prediction error: {e}")
            return None, None
    else:
        return None, None

def update_current_song(label):
    song_name = send_request('currentsong')
    label.config(text=f"Current Song: {song_name}")
    label.after(10000, lambda: update_current_song(label))  # Update every 10 seconds

def check_playback_status():
    playback_status = send_request('status')
    if playback_status not in ['PLAYING', 'UNKNOWN']:
        send_request('playpause')  # Ensure the music plays if not in PLAYING state

def continuous_capture(prediction_label, song_label):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not access the webcam.")
        return

    last_action_time = time.time()
    action_interval = 2  # Set to 2 seconds for faster reaction times
    confidence_threshold = 0.6  # Adjust based on your model's performance
    no_action_class = 3  # Assuming 3 is 'no-action' in your model

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame.")
                break

            # Convert frame to RGB and resize
            image = cv2.resize(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), (224, 224))
            img_array = np.array(image) / 255.0
            prediction, confidence = make_prediction(img_array)

            if prediction is not None and confidence >= confidence_threshold:
                current_time = time.time()
                if current_time - last_action_time > action_interval:
                    if prediction != no_action_class:
                        if prediction == 0:
                            send_request('skip')
                        elif prediction == 1:
                            send_request('playpause')
                        elif prediction == 2:
                            send_request('previous')
                        last_action_time = current_time

                prediction_label.config(text=f"Current Prediction: {prediction}, Confidence: {confidence:.2f}")

            cv2.imshow('Webcam', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            # Check playback status periodically and ensure music plays if not already playing
            if int(time.time()) % 10 == 0:
                check_playback_status()

    except Exception as e:
        print(f"Processing error: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()

    update_current_song(song_label)

def create_gui():
    root = Tk()
    root.title("Music Controller")
    prediction_label = Label(root, text="Current Prediction: None")
    prediction_label.pack()
    
    song_label = Label(root, text="Current Song: Unknown")
    song_label.pack()

    def on_closing():
        root.quit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    return root, prediction_label, song_label

def create_manual_controls():
    root = Tk()
    root.title("Music Controller - Manual Mode")
    
    skip_button = Button(root, text="Skip", command=lambda: send_request('skip'))
    skip_button.pack()

    play_pause_button = Button(root, text="Play/Pause", command=lambda: send_request('playpause'))
    play_pause_button.pack()

    previous_button = Button(root, text="Previous", command=lambda: send_request('previous'))
    previous_button.pack()

    current_song_label = Label(root, text="Current Song: Unknown")
    current_song_label.pack()
    update_current_song(current_song_label)

    def on_closing():
        root.quit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    return root

def main():
    if model_loaded:
        root, prediction_label, song_label = create_gui()
        root.after(0, lambda: continuous_capture(prediction_label, song_label))
        root.mainloop()
    else:
        print("Model is not available. Displaying manual controls.")
        root = create_manual_controls()
        root.mainloop()

if __name__ == "__main__":
    main()