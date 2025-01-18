import cv2
import os
import matplotlib.pyplot as plt
import uuid

def detect_bounding_box(self, frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detect faces in the grayscale frame
    faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))

    # Iterate over each detected face
    for (x, y, w, h) in faces:
        # crop_img = frame[y-50:y+50 + h, x-50:x+50 + w]
        self.save_frame(frame)
        # Draw a rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)

        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        plt.figure(figsize=(20, 10))
        plt.imshow(img_rgb)
        plt.axis('off')
    return faces


def save_frame(frame):
  new_filename = str(uuid.uuid4())+'.jpg'
  cv2.imwrite(new_filename, frame)
  return new_filename

def start(self):
  while True:
      # Read the current frame from the video capture
      result, frame = self.video_capture.read()
      if result is False:
          break  # terminate the loop if the frame is not read successfully

      faces = self.detect_bounding_box(
          frame
      )  # apply the function we created to the video frame

      # Display the resulting frame
      cv2.imshow('Face Recognizer', frame)

      if len(faces) >0:
          #saves the frame for processing
          self.save_frame(frame)
          self.process_photo()
          self.process_insult()



      # Break the loop if 'q' is pressed
      if cv2.waitKey(1) & 0xFF == ord("q"):
          break

  # Release the video capture and close all windows
  self.video_capture.release()
  cv2.destroyAllWindows()