# from FaceAndEyeDetectorWorker import FaceAndEyeDetectorWorker  
from SocketVideoStream import SocketVideoStream
from FaceAndEyeDetectorWorker import FaceAndEyeDetectorWorker
from lib import current_time
import time
import zmq
import json
import gaze

# vs.start()

def has_valid_feature(faces, face_features):
    if faces is None or face_features is None or len(faces) == 0 or len(face_features) == 0:
        return False
    
    print('face detected...checking for eyes')

    for i, face in enumerate(faces):
        face_feature = face_features[i]
        eyes, _ = face_feature
        if len(eyes) == 2:
            return True

    print('no eyes detected')
    return False

def to_int_list(numpy_list):
    return map(lambda x: int(x), numpy_list)

def get_eyes(face_feature):
    eyes, _ = face_feature

    if len(eyes) == 0:
        return []

    return map(lambda eye: to_int_list(eye), eyes)

def main():
    # initialize the video camera stream and read the first frame
    # from the stream
 
    context = zmq.Context()
    pull_socket = context.socket(zmq.PULL)
    pull_socket.bind('tcp://*:5555')

    push_socket = context.socket(zmq.PUSH)
    push_socket.bind('tcp://*:5556')

    video_stream = SocketVideoStream(context, pull_socket).start()
    face_detector_stream = FaceAndEyeDetectorWorker(video_stream).start()

    last_frame_time = None

    while True:
        img, faces, face_features, frame_time = face_detector_stream.read()

        # frontend.send_json(['hi'])

        if last_frame_time == frame_time:
            continue

        last_frame_time = frame_time

        response = {}
        if (faces is not None):
            # dumped = json.dumps(faces)
            faces_list = list(map(lambda face: to_int_list(face) if face is not None else [], faces))
            response['faces'] = faces_list
            response['eyes'] = list(map(lambda face_feature: get_eyes(face_feature), face_features))

            # print('faces', response['faces'])
            # print('jsoned', json.dumps(faces_list))
            # print("faces fson:", json.dumps(response['faces']))
            # # response['eyes'] = map(lambda face_feature: face_feature[0] if face_feature is not None else [], face_features)
        # response['face_features'] = face_features

        if has_valid_feature(faces, face_features):
            print('has valid features')
            outputs = gaze.test_faces(img, faces, face_features)

            print('outputs, detection time', outputs, current_time() - frame_time)

            if outputs and outputs[0] is not None:
                print('sending json')
                # response = {
                #    'outputs:', outputs[0].tolist(),
                #    'faces': faces,
                #    'face_features': face_features
                # }
                response['gazes'] = list(map(lambda output: 
                output.tolist() if output is not None else [], 
                outputs))
        # else:
        #     push_socket.send_json({
        #         'faces': faces,
        #         'face_features': face_features
        #     })

 
        # print("sending response", response)
        # print("final json:", json.dumps(response))
        push_socket.send_json(response)


        time.sleep(10./1000)

if __name__ == "__main__":
    main()