import requests
import tensorflow as tf
import numpy as np
import cv2
from tkinter import Tk, Button, Label
import time

# Base URL for the music control service
BASE_URL = "http://localhost:10767"
# Define the endpoint paths
ENDPOINTS = {
    'skip': f"{BASE_URL}/next",
    'playpause': f"{BASE_URL}/playPause",
    'previous': f"{BASE_URL}/previous",
    'currentsong': f"{BASE_URL}/currentPlayingSong"
}

def send_request(action):
    try:
        response = requests.post(ENDPOINTS[action])  # Updated to correct POST method
        if response.status_code == 204:
            print(f"{action.capitalize()} action performed successfully.")
        else:
            print(f"Failed to perform {action} action. Status Code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        print(f"Request error: {e}")

# Try to load the Teachable Machine model
model_loaded = False
model = None

try:
    class InferenceModel(tf.keras.Model):
        def __init__(self, saved_model_path):
            super(InferenceModel, self).__init__()
            self.tf_layer = tf.saved_model.load(saved_model_path)  # Load the SavedModel

        def call(self, inputs):
            return self.tf_layer(inputs)
    
    model_path = '/path/to/your/model/directory'  # Provide the correct path to your model
    model = InferenceModel(model_path)
    model_loaded = True
    print("Model loaded successfully.")
except Exception as e:
    print(f"Model could not be loaded: {e}")

def make_prediction(input_data):
    if model_loaded:
        try:
            input_data = np.expand_dims(input_data, axis=0)  # Ensuring batch dimension
            prediction = model(tf.convert_to_tensor(input_data))
            predicted_class = np.argmax(prediction.numpy(), axis=1)
            return predicted_class[0]
        except Exception as e:
            print(f"Prediction error: {e}")
            return None
    else:
        return None

def continuous_capture(prediction_label):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Could not access the webcam.")
        return

    last_action_time = time.time()
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame.")
                break

            image = cv2.resize(frame, (224, 224))  # Resize to model's expected input size
            img_array = np.array(image) / 255.0  # Normalize the image
            prediction = make_prediction(img_array)

            if prediction is not None:
                current_time = time.time()
                if current_time - last_action_time > 8:  # 8 seconds delay
                    if prediction == 0:
                        send_request('skip')
                    elif prediction == 1:
                        send_request('playpause')
                    elif prediction == 2:
                        send_request('previous')
                    else:
                        print("Invalid prediction result")
                    last_action_time = current_time

                # Update the prediction label
                prediction_label.config(text=f"Current Prediction: {prediction}")

            # Display the frame in a window
            cv2.imshow('Webcam', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    except Exception as e:
        print(f"Processing error: {e}")
    finally:
        cap.release()
        cv2.destroyAllWindows()

def create_gui():
    root = Tk()
    root.title("Music Controller")

    prediction_label = Label(root, text="Current Prediction: None")
    prediction_label.pack()

    def on_closing():
        root.quit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    return root, prediction_label

def create_manual_controls():
    root = Tk()
    root.title("Music Controller - Manual Mode")

    skip_button = Button(root, text="Skip", command=lambda: send_request('skip'))
    skip_button.pack()

    play_pause_button = Button(root, text="Play/Pause", command=lambda: send_request('playpause'))
    play_pause_button.pack()

    previous_button = Button(root, text="Previous", command=lambda: send_request('previous'))
    previous_button.pack()

    current_song_button = Button(root, text="Current Song", command=lambda: send_request('currentsong'))
    current_song_button.pack()

    def on_closing():
        root.quit()
        root.destroy()

    root.protocol("WM_DELETE_WINDOW", on_closing)
    return root

def main():
    global model_loaded

    if model_loaded:
        # Create the GUI and get the prediction label
        root, prediction_label = create_gui()
        root.after(0, lambda: continuous_capture(prediction_label))
        root.mainloop()
    else:
        print("Model is not available. Displaying manual controls.")
        root = create_manual_controls()
        root.mainloop()

if __name__ == "__main__":
    main()