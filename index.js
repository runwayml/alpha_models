export default [
  {
    containerId: '84d72a2f82f6',
    tag: 'cvalenzuelab/im2text:latest',
    name: 'im2txt',
    specs: {
      cpu: true,
      gpu: true,
    },
    port: '33100',
    query: {
      http: {
        route: 'query_once',
        method: 'post',
        type: 'JSON',
      },
      socket: {
        namespace: 'query',
        emit: 'update_request',
        event: 'update_response'
      },
      format: {
        data: 'data:image/jpg;base64,'
      }
    },
    size: ['2.19', 'GB'],
    options: {
      image: '84d72a2f82f6',
      Tty: false,
      Detach: true,
      ExposedPorts: { '33000/tcp': {} },
      HostConfig: {
        AutoRemove: true,
        PortBindings: {
          '33000/tcp': [{
            HostIP: '0.0.0.0',
            HostPort: '33100'
          }],
        },
      }
    },
    needsTraining: false,
    description: {
      first: 'The im2txt model, also called the Show and Tell model, is a deep neural network that learns how to describe the content of images',
      second: 'More technically, it is an example of an encoder-decoder neural network. It works by first "encoding" an image into a fixed-length vector representation, and then "decoding" the representation into a natural language description.',
      third: 'The image encoder is a deep convolutional neural network. This type of network is widely used for image tasks and is currently state-of-the-art for object recognition and detection. Our particular choice of network is the Inception v3 image recognition model pretrained on the ILSVRC-2012-CLS image classification dataset. The decoder is a long short-term memory (LSTM) network. This type of network is commonly used for sequence modeling tasks such as language modeling and machine translation. In the Show and Tell model, the LSTM network is trained as a language model conditioned on the image encoding.',
      authors: 'Oriol Vinyals, Alexander Toshev, Samy Bengio, Dumitru Erhan.',
      image: 'https://raw.githubusercontent.com/cvalenzuela/runway_models/master/im2txt/imgs/demo.png?token=AKHU_R2F7AQImVwfzZ1RqeRfVKYWJYwhks5azcGywA%3D%3D',
      organization: 'Google',
      framework: 'Tensorflow',
      github: 'https://github.com/tensorflow/models/tree/master/research/im2txt',
      paper: 'https://arxiv.org/abs/1609.06647',
      licence: 'Apache License 2.0',
    },
    inputs: ['Image', 'Video']
  },
  {
    containerId: '528c549ae8f8',
    tag: 'cvalenzuelab/openpose:latest',
    name: 'OpenPose',
    specs: {
      cpu: false,
      gpu: true,
    },
    port: '33200',
    query: {
      http: {
        route: 'test',
        method: 'get',
        type: 'JSON',
      },
      socket: {
        namespace: 'query',
        emit: 'update_request',
        event: 'update_response'
      },
      format: {
        data: 'data:image/jpg;base64,'
      }
    },
    size: ['2.69', 'GB'],
    options: {
      image: '528c549ae8f8',
      Tty: false,
      Detach: true,
      ExposedPorts: { '33000/tcp': {} },
      HostConfig: {
        AutoRemove: true,
        PortBindings: {
          '33000/tcp': [{
            HostIP: '0.0.0.0',
            HostPort: '33200'
          }],
        },
      }
    },
    needsTraining: false,
    description: {
      first: 'Real-time multi-person keypoint detection library for body, face, and hands estimation.',
      second: 'OpenPose represents the first real-time multi-person system to jointly detect human body, hand, and facial keypoints (in total 130 keypoints) on single images.',
      third: 'Functionality include: real-time multi-person keypoint detection, 15 or 18-keypoint body estimation. Running time invariant to number of detected people, 2x21-keypoint hand estimation. Currently, running time depends on number of detected people, 70-keypoint face estimation. Currently, running time depends on number of detected people.',
      authors: 'Gines Hidalgo, Zhe Cao, Tomas Simon, Shih-En Wei, Hanbyul Joo, and Yaser Sheikh. ',
      image: 'https://raw.githubusercontent.com/cvalenzuela/runway_models/master/openpose/images/demo.png?token=AKHU_dAn9zHBVGjj1NO-uZn_mo4rALB5ks5azcHSwA%3D%3D',
      organization: 'CMU Perceptual Computing Lab',
      framework: 'Caffe2',
      github: 'https://github.com/CMU-Perceptual-Computing-Lab/openpose',
      paper: 'https://arxiv.org/abs/1611.08050',
      licence: 'Apache License 2.0',
    },
    inputs: ['Image', 'Video']
  },
  {
    containerId: '09b20a63a278',
    tag: 'cvalenzuelab/nodeserver:latest',
    name: 'nodeserver',
    specs: {
      cpu: true,
      gpu: true,
    },
    port: '33100',
    query: {
      http: {
        route: 'query_once',
        method: 'post',
        type: 'JSON',
      },
      socket: {
        namespace: 'query',
        emit: 'update_request',
        event: 'update_response'
      },
      format: {
        data: 'data:image/jpg;base64,'
      }
    },
    size: ['2.19', 'GB'],
    options: {
      image: '84d72a2f82f6',
      Tty: false,
      Detach: true,
      ExposedPorts: { '33000/tcp': {} },
      HostConfig: {
        AutoRemove: true,
        PortBindings: {
          '33000/tcp': [{
            HostIP: '0.0.0.0',
            HostPort: '33100'
          }],
        },
      }
    },
    needsTraining: false,
    description: {
      first: 'The im2txt model, also called the Show and Tell model, is a deep neural network that learns how to describe the content of images',
      second: 'More technically, it is an example of an encoder-decoder neural network. It works by first "encoding" an image into a fixed-length vector representation, and then "decoding" the representation into a natural language description.',
      third: 'The image encoder is a deep convolutional neural network. This type of network is widely used for image tasks and is currently state-of-the-art for object recognition and detection. Our particular choice of network is the Inception v3 image recognition model pretrained on the ILSVRC-2012-CLS image classification dataset. The decoder is a long short-term memory (LSTM) network. This type of network is commonly used for sequence modeling tasks such as language modeling and machine translation. In the Show and Tell model, the LSTM network is trained as a language model conditioned on the image encoding.',
      authors: 'Oriol Vinyals, Alexander Toshev, Samy Bengio, Dumitru Erhan.',
      image: 'https://raw.githubusercontent.com/cvalenzuela/runway_models/master/openpose/images/demo.png?token=AKHU_dAn9zHBVGjj1NO-uZn_mo4rALB5ks5azcHSwA%3D%3D',
      organization: 'Google',
      framework: 'Tensorflow',
      github: 'https://github.com/tensorflow/models/tree/master/research/im2txt',
      paper: 'https://arxiv.org/abs/1609.06647',
      licence: 'Apache License 2.0',
    },
    inputs: ['Image', 'Video']
  },
  {
    containerId: '00',
    tag: '',
    name: 'Detectron',
    specs: {
      cpu: false,
      gpu: true,
    },
    size: '1.02GB',
    options: {
      image: '123123',
      Tty: false,
      Detach: true,
      ExposedPorts: { '33000/tcp': {} },
      HostConfig: {
        AutoRemove: true,
        PortBindings: {
          '33000/tcp': [{
            HostIP: '0.0.0.0',
            HostPort: '33000'
          }],
        },
      }
    },
    shortDescription: 'Detectron is Facebook AI Researchs software system that implements state-of-the-art object detection algorithms, including Mask R-CNN. It is written in Python and powered by the Caffe2 deep learning framework.',
    description: 'Detectron is Facebook AI Researchs software system that implements state-of-the-art object detection algorithms, including Mask R-CNN. It is written in Python and powered by the Caffe2 deep learning framework.',
    developer: 'Chris Shallue',
    company: 'Google',
    framework: 'Tensorflow',
    docker: '',
    github: '',
    url: '',
    inputs: ['Image', 'Video', 'Pixels']
  },
  {
    containerId: '123123',
    tag: '',
    name: 'pix2pixHD',
    specs: {
      cpu: false,
      gpu: true,
    },
    size: '1.02GB',
    options: {
      image: '47556328a93993',
      Tty: false,
      Detach: true,
      ExposedPorts: { '33000/tcp': {} },
      HostConfig: {
        AutoRemove: true,
        PortBindings: {
          '33000/tcp': [{
            HostIP: '0.0.0.0',
            HostPort: '33000'
          }],
        },
      }
    },
    shortDescription: 'Detectron is Facebook AI Researchs software system that implements state-of-the-art object detection algorithms, including Mask R-CNN. It is written in Python and powered by the Caffe2 deep learning framework.',
    description: 'Detectron is Facebook AI Researchs software system that implements state-of-the-art object detection algorithms, including Mask R-CNN. It is written in Python and powered by the Caffe2 deep learning framework.',
    developer: 'Chris Shallue',
    company: 'Google',
    framework: 'Tensorflow',
    docker: '',
    github: '',
    url: '',
    inputs: ['Image', 'Video', 'Pixels']
  },
  {
    containerId: '1233123',
    tag: '',
    name: 'DeepSpeech',
    specs: {
      cpu: false,
      gpu: true,
    },
    size: '1.02GB',
    options: {
      image: '47556128a93993',
      Tty: false,
      Detach: true,
      ExposedPorts: { '33000/tcp': {} },
      HostConfig: {
        AutoRemove: true,
        PortBindings: {
          '33000/tcp': [{
            HostIP: '0.0.0.0',
            HostPort: '33000'
          }],
        },
      }
    },
    shortDescription: 'Project DeepSpeech is an open source Speech-To-Text engine, using a model trained by machine learning techniques, based on Baidus Deep Speech research paper. Project DeepSpeech uses Googles TensorFlow project to make the implementation easier.',
    description: 'Project DeepSpeech is an open source Speech-To-Text engine, using a model trained by machine learning techniques, based on Baidus Deep Speech research paper. Project DeepSpeech uses Googles TensorFlow project to make the implementation easier.',
    developer: 'Chris Shallue',
    company: 'Google',
    framework: 'Tensorflow',
    docker: '',
    github: '',
    url: '',
    inputs: ['Image', 'Video', 'Pixels']
  },
];
