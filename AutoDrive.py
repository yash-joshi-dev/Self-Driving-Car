import cv2
import numpy as np
from tflite_runtime.interpreter import Interpreter
import sys
import os

# must run below 2 lines to access provided functions to manipulate the motor for this particular car:
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from Motor import *

# load the model
interpreter = Interpreter('model.tflite')
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# init camera
cap = cv2.VideoCapture(0)

# wrapper function around motors (specific to this car)
def setMotors(l, r=None):
  if r is None:
    r = l
  
  # this line is specific to the car used
  PWM.setMotorModel(l, l, r, r)

# function to control car based off direction
def controlCar(direction):
  if direction == 0:
    setMotors(800)
  elif direction == 1:
    setMotors(-800)
  elif direction == 2:
    setMotors(1500, -1500)
  elif direction == 3:
    setMotors(-1500, 1500)

# define main loop
def main():
  while True:
    ret, frame = cap.read()
    
    if not ret:
      continue
    
    # process input frame
    input_frame = cv2.resize(frame, (64, 64))
    input_frame = np.expand_dims(input_frame, axis=0).astype(np.float32) / 255.0

    # perform inference
    interpreter.set_tensor(input_details[0]['index'], input_frame)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])

    # process output
    direction = np.argmax(output)
    controlCar(direction)

if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    cap.release()
    cv2.destroyAllWindows()
    setMotors(0)
