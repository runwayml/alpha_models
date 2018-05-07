# import the necessary packages
from threading import Thread
import zmq
import numpy as np
import time
from lib import current_time 

class SocketVideoStream:
    def __init__(self, context, socket):
        self.context = context
        poller = zmq.Poller()
        poller.register(socket, zmq.POLLIN)

        self.socket = socket
        self.poller = poller

        self.frame = None
        self.frame_time = None
        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False

    def start(self):
        # start the thread to read frames from the video stream
        print('started thread')
        t = Thread(target=self.update, args=())
        t.daemon = True
        t.start()
        return self

    def update(self):
        print('called update')
        # flushed = self.socket.recv(flags=0)
        # print('the flushed stream', flushed_stream)
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            #  print('updating')
            if self.stopped:
                #  print('returning')
                return
            
            # try:
            # print("receiving json")
            sockets = dict(self.poller.poll())
            if self.socket in sockets:
                msg = self.socket.recv()
                print("message", msg)
                # msg = self.socket.recv_json(flags=0)
                # data = self.socket.recv(flags=0, copy=True, track=False)
                # A = np.frombuffer(data, msg['dtype'])
                # self.frame = A.reshape(msg['shape'])
                # _=  self.socket.recv(flags=0, copy=True, track=False)
        # # except KeyboardInterrupt:
        #     #     print("W: interrupt received, stopping...")
        #     #     self.worker.close()
        #     #     self.context.term()

        #         self.frame = A.reshape(msg['shape'])
                # print('got socket:', self.socket.recv())
                self.frame_time = current_time()

        self.worker.close()

    def read(self):
        # return the frame most recently read
        return (self.frame, self.frame_time)

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True
