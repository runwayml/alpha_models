FROM tensorflow/tensorflow:0.12.1

WORKDIR /root

RUN apt-get update
RUN apt-get install wget -y

# Copy the directory
COPY . .

# Server dependencies
RUN pip install Flask
RUN pip install flask-cors
RUN pip install gevent
RUN pip install flask-socketio

MAINTAINER Cristobal Valenzuela<cv965@nyu.edu>

# Expose the port
EXPOSE 33000

# Get the model checkpoints
RUN wget --load-cookies /tmp/cookies.txt "https://docs.google.com/uc?export=download&confirm=$(wget --quiet --save-cookies /tmp/cookies.txt --keep-session-cookies --no-check-certificate 'https://docs.google.com/uc?export=download&id=1ucLRxg-Nth8k4naqzBuSYnyowZXIdw4U' -O- | sed -rn 's/.*confirm=([0-9A-Za-z_]+).*/\1\n/p')&id=1ucLRxg-Nth8k4naqzBuSYnyowZXIdw4U" -O im2txt_pretrained.zip && rm -rf /tmp/cookies.txt
RUN unzip im2txt_pretrained.zip
RUN rm -rf im2txt_pretrained.zip

# Install im2text dependencies
RUN add-apt-repository ppa:webupd8team/java && apt-get update
RUN echo debconf shared/accepted-oracle-license-v1-1 select true | sudo debconf-set-selections && echo debconf shared/accepted-oracle-license-v1-1 seen true | sudo debconf-set-selections
RUN apt-get install -y oracle-java8-installer
RUN echo "deb [arch=amd64] http://storage.googleapis.com/bazel-apt stable jdk1.8" | sudo tee /etc/apt/sources.list.d/bazel.list && curl https://bazel.build/bazel-release.pub.gpg | sudo apt-key add -
RUN apt-get update && apt-get install -y bazel

# Run inference
RUN ./build_inference.sh

# Start the server
ENTRYPOINT ./im2txt/bazel-bin/im2txt/run_inference