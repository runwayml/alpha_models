import zmq
import sys
import threading
import time
import threading
import cv2
import io
import base64
import numpy as np

def tprint(msg):
    """like print, but won't get newlines confused with multiple threads"""
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()

class ClientTask(threading.Thread):
    """ClientTask"""
    def __init__(self, id, src=0):
        self.id = id
        threading.Thread.__init__ (self)
        cap = cv2.VideoCapture(src)
        cap.set(3,1280)
        cap.set(4,720)
        self.stream = cap

        (self.grabbed, self.frame) = self.stream.read()


    def run(self):
        context = zmq.Context()
        push_socket = context.socket(zmq.PUSH)
        pull_socket = context.socket(zmq.PULL)
        identity = u'worker-%d' % self.id
        push_socket.identity = identity.encode('ascii')
        push_socket.connect('tcp://localhost:5555')
        pull_socket.identity = identity.encode('ascii')
        pull_socket.connect('tcp://localhost:5556')
        print('Client %s started' % (identity))
        poll = zmq.Poller()
        poll.register(pull_socket, zmq.POLLIN)
        reqs = 0
        while True:
            reqs = reqs + 1
            if reqs % 100 == 0:
                print('Req #%d sent..' % (reqs))
            _, frame = self.stream.read()
            md = dict(
                dtype = str(frame.dtype),
                shape = frame.shape,
            )
            push_socket.send_json(md, zmq.SNDMORE)
            push_socket.send(memoryview(frame.data), 0, copy=True, track=False)

            sockets = dict(poll.poll(10))
            if pull_socket in sockets:
                msg = pull_socket.recv_json()
                print('Client received: %s' % (msg))

            cv2.imshow('image', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


            # if result in sockets:
            #     msg = result.recv_json()
            #     print("received json", msg)
            # # for i in range(5):
            #     sockets = dict(poll.poll(1000))
            #     if socket in sockets:
            #         msg = socket.recv()
            #         tprint('Client %s received: %s' % (identity, msg))

        push_socket.close()
        context.term()

def main():
    """main function"""
    client = ClientTask(0, 0)
    client.start()

if __name__ == "__main__":
    main()