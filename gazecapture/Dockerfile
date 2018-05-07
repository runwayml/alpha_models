FROM bvlc/caffe:cpu

WORKDIR /root

# download 
RUN wget https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_eye.xml -P data/
RUN wget https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml -P data/

RUN wget https://raw.githubusercontent.com/CSAILVision/GazeCapture/master/models/itracker_deploy.prototxt -P data/
RUN wget https://github.com/CSAILVision/GazeCapture/raw/master/models/snapshots/itracker25x_iter_92000.caffemodel -P data/
RUN wget https://github.com/CSAILVision/GazeCapture/raw/master/models/mean_images/mean_face_224.mat -P data/
RUN wget https://github.com/CSAILVision/GazeCapture/raw/master/models/mean_images/mean_left_224.mat -P data/
RUN wget https://github.com/CSAILVision/GazeCapture/raw/master/models/mean_images/mean_right_224.mat -P data/

ENV MODEL_DIR="/root/data/"
ENV OPENCV_DATA="/root/data/"

ADD setup_zero_mq.sh setup_zero_mq.sh 

RUN ./setup_zero_mq.sh

ENV GPU='false'

ADD requirements.txt requirements.txt

RUN pip install -r requirements.txt

EXPOSE 33000

# Copy the directory
COPY ./src /root/src/

ENTRYPOINT python ./src/server.py