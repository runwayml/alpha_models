# import the necessary packages
from threading import Thread
from features import extract_image_features
from lib import current_time
import time
import cv2


class FaceAndEyeDetectorWorker:
    def __init__(self, socket_video_stream):
        print('initializing stream')
        self.webcam_stream = socket_video_stream

        print('initialized')


        self.img = None
        self.faces = None
        self.face_features = None
        self.frame_time = current_time()
        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        print('starting update')
        while True:
            # if the thread indicator variable is set, stop the thread
            #  print('updating')
            if self.stopped:
                #  print('returning')
                return

            # otherwise, read the next frame from the stream
            frame, frame_time = self.webcam_stream.read()
            
            if frame is not None and frame_time != self.frame_time:
                (self.img, self.faces, self.face_features) = extract_image_features(frame)
                self.frame_time = frame_time

            time.sleep(5. / 1000)
                
            #  print('the faces', self.faces)
            #  print('updated', self.grabbed)

    def read(self):
        # return the frame most recently read
        return (self.img, self.faces, self.face_features, self.frame_time)

    def stop(self):
        # indicate that the thread should be stopped
        self.webcam_stream.stop()
        self.stopped = True
