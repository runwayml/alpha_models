# GazeCapture RunwayML

This repository brings the pre-trained model from [Eye Tracking for Everyone](https://github.com/CSAILVision/GazeCapture)
into python and RunwayML.

It allows for a server to be spun up in a docker container that performs real-
time gaze estimation from a video stream.  It works with any webcam.

I have used this model successfully in my project [Presence](http://www.danioved.com/portfolio/presence/) - a kinetic sculpture that reacts to a users gaze.

### The server:

Install Docker.

Build the docker container in a tag:

    docker build . -t gaze

Launch the container:

    ./start_container.sh


### The client:

The client opens a webcam video feed and sends it in a stream to the server, getting gaze positions back.

Install dependencies:

    pip install opencv-python zmq
        
Launch the client:

    python test_client.py