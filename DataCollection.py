import cv2
import BlynkLib
import numpy as np
import sys
import os
from dotenv import load_dotenv
load_dotenv()

# must run the below 2 lines to access provided functions to manipulate the motor for this particular car:
sys.path.append(os.path.join(os.path.dirname(__file__), 'providedCarModules'))
from Motor import *

# init the camera
cap = cv2.VideoCapture(0)

# connect to the blynk cloud
BLYNK_AUTH = os.getenv('BLYNK_AUTH_CODE')
blynk = BlynkLib.Blynk(BLYNK_AUTH, server="blynk.cloud")

# define the pin numbers for each direction
FORWARD = 2
BACKWARD = 3
RIGHT = 4
LEFT = 5

# wrapper function to instruct the motors
def setMotors(l, r=None):
  if r is None:
    r = l

  # this is specific to the car used
  PWM.setMotorModel(l, l, r, r)

# will store the collected samples
data = []

# function to take a sample (what direction car went for the current image)
def takeSample(direction):
  print("direction is ", direction)
  ret, frame = cap.read()
  if ret:
    frame = cv2.resize(frame, (64, 64))
    data.append((frame, direction))

# define how motors should move when the virtual pins change -----------------------------
@blynk.VIRTUAL_WRITE(FORWARD)
def forward_write_handler(value):
  if int(value[0]) == 1:
    setMotors(1200)
    takeSample("F")
  else:
    setMotors(0)

@blynk.VIRTUAL_WRITE(BACKWARD)
def backward_write_handler(value):
  if int(value[0]) == 1:
    setMotors(-1200)
    takeSample("B")
  else:
    setMotors(0)

@blynk.VIRTUAL_WRITE(RIGHT)
def right_write_handler(value):
  if int(value[0]) == 1:
    setMotors(1500, -1500)
    takeSample("R")
  else:
    setMotors(0)

@blynk.VIRTUAL_WRITE(LEFT)
def left_write_handler(value):
  if int(value[0]) == 1:
    setMotors(-1500, 1500)
    takeSample("L")
  else:
    setMotors(0)

# define main loop (run blynk app, until an exception occurs, at which point save the data collected to file data.npy and free camera)
def main():
  try:
    while True:
      blynk.run()
  except KeyboardInterrupt:
    pass
  except Exception as e:
    print("An error occurred:", e)
  finally:
    cap.release()
    cv2.destroyAllWindows()
    np.save('data.npy', np.array(data, dtype=object))
    print("Data saved with shape:", np.array(data, dtype=object).shape)


if __name__ == "__main__":
  main()
