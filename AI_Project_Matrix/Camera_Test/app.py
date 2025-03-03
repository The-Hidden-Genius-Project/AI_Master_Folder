import cv2
import time

   # Try different indices. Increase the range if you have many video inputs.
for index in range(0, 100):
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print(f"No camera on index {index}")
        continue
       
    print(f"Testing camera on index {index}...")
    ret, frame = cap.read()
    if ret:
        cv2.imshow(f"Camera Index {index}", frame)
        cv2.waitKey(1000)  # Show the frame for 1 second
        print(f"Camera on index {index} is working.")
    else:
        print(f"Camera on index {index} found but cannot capture.")

    cap.release()
    cv2.destroyAllWindows()
    time.sleep(1)