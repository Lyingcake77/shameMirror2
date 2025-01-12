import cv2
import os
import matplotlib.pyplot as plt
from ollama import chat
from ollama import ChatResponse
import pyttsx3
import random
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration

class ShameMirror:
  def __init__(self,mode):
    self.mode = mode

    self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # Load the pre-trained face recognition model
    self.recognizer = cv2.face.LBPHFaceRecognizer_create()
    # Initialize the video capture
    self.video_capture = cv2.VideoCapture(0)

    self.processing = 0
    self.insult_param = []
  def process_insult(self):
      randomCharacteristics = random.sample(self.insult_param, 1)
      print(randomCharacteristics)
      response: ChatResponse = chat(model='llama2-uncensored', messages=[
          {
              'role': 'user',
              #'content': 'Generate an insult toward me based on the following features about my face:'+', '.join(randomCharacteristics),
              'content': 'Generate an insult based on the following criteria:'+', '.join(randomCharacteristics),
          },
      ])
      print(response.message.content)
      engine = pyttsx3.init()
      engine.say(response.message.content)
      engine.runAndWait()

  def ai_generate_text(self):
      processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-large")
      model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-large").to("cuda")

      img_url = 'framed.jpg'
      raw_image = Image.open(img_url).convert('RGB')

      # conditional image captioning
      text = "the face of"
      inputs = processor(raw_image, text, return_tensors="pt").to("cuda")

      out = model.generate(**inputs)
      print(processor.decode(out[0], skip_special_tokens=True))

      # unconditional image captioning
      inputs = processor(raw_image, return_tensors="pt").to("cuda")

      out = model.generate(**inputs)
      print(processor.decode(out[0], skip_special_tokens=True))
      return processor.decode(out[0], skip_special_tokens=True)
  def detect_bounding_box(self,frame):
      gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
      # Detect faces in the grayscale frame
      faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))

      # Iterate over each detected face
      for (x, y, w, h) in faces:
          #crop_img = frame[y-50:y+50 + h, x-50:x+50 + w]
          self.save_frame(frame)
          # Draw a rectangle around the face
          cv2.rectangle(frame, (x, y), (x + w, y + h), color = (0, 255, 0), thickness = 2)

          img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
          plt.figure(figsize=(20, 10))
          plt.imshow(img_rgb)
          plt.axis('off')
      return faces
  def save_frame(self,frame):
      if self.processing == 0:
          cv2.imwrite("framed.jpg", frame)
          #self.processing = 1
  def process_photo(self):
      result = self.ai_generate_text()
      self.insult_param = [result]
      # self.insult_param = ['large nose', 'crooked teeth', 'asymmetrical face', 'scar below the lip', 'mole under the right eye']
      pass
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
              #self.save_frame(frame)
              self.process_photo()
              self.process_insult()



          # Break the loop if 'q' is pressed
          if cv2.waitKey(1) & 0xFF == ord("q"):
              break

      # Release the video capture and close all windows
      self.video_capture.release()
      cv2.destroyAllWindows()

sm = ShameMirror("shame")
sm.start()