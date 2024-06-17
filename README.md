# Self-Driving-Car

This repo contains the code for a simple self driving car made with RaspberryPi. The car model has been trained to drive inside a lane/path made with white masking tape. The model was made with Tensorflow and coverted to a lightweight TFLite model to run more efficiently on the RaspberryPi. Also, OpenCV was used to take and process images from the USB camera on the car. In addition, the Blynk IoT app was used to control the car to generate training data. Finally, the car base (including motors) came in a Freenove Car Kit - the modules that were provided with this kit to manipulate the motors are in the providedCarModules folder.

To create this car there were three main steps (and a python script for each):
1. Data collection: data to train the model was collected by driving the car around the track (using the Blynk app), and for each direction driven (forwards, backwards, right, left), an 64x64 image was associated with it; the name of the script was DataCollection.py.
2. Training the model: the Tensorflow model was made and trained on a Google Colab (not on the RaspberryPi), before getting converted to a TFLite model; the notebook to do this is called TrainModel.ipynb.
3. Using the model: after uploading the TFLite model onto the RaspberryPi, the AutoDrive.py script was used to drive the call autonomously around the track.

Here is an image of the car and the track it was trained on:
<br>
<img src="https://github.com/yash-joshi-dev/Self-Driving-Car/assets/62446094/ddf638db-3817-42e9-8eeb-76142e24649c" alt="image of self-driving car" width="300"/>
<img src="https://github.com/yash-joshi-dev/Self-Driving-Car/assets/62446094/a50fb24c-dbf0-41d8-b8f4-97dfbd764c6e" alt="image of self-driving car on training track" width="300"/>
