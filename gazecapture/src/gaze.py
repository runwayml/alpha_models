import sys
import os
sys.path.append('/usr/bin/caffe')
os.environ['GLOG_minloglevel'] = '2'
import caffe
import numpy as np
from lib import current_time, crop_image
import os


#caffe.set_mode_cpu()
model_root = os.path.dirname(os.environ['MODEL_DIR'])

model_def = model_root + '/itracker_deploy.prototxt'
model_weights = model_root + '/itracker25x_iter_92000.caffemodel'

net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)     # use test mode (e.g., don't perform dropout)


# load the mean images
import scipy.io

def get_mean_image(file_name):
    image_mean = np.array(scipy.io.loadmat(model_root + '/' + file_name)['image_mean'])
    image_mean = image_mean.reshape(3, 224, 224)

    return image_mean.mean(1).mean(1)

mu_face = get_mean_image('mean_face_224.mat')
mu_left_eye = get_mean_image('mean_left_224.mat')
mu_right_eye = get_mean_image('mean_left_224.mat')

# create transformer for the input called 'data'
def create_image_transformer(layer_name, mean_image=None):
    transformer = caffe.io.Transformer({layer_name: net.blobs[layer_name].data.shape})

    transformer.set_transpose(layer_name, (2,0,1))  # move image channels to outermost dimension
    if mean_image is not None:
        transformer.set_mean(layer_name, mean_image)            # subtract the dataset-mean value in each channel
    return transformer

left_eye_transformer = create_image_transformer('image_left', mu_left_eye)
right_eye_transformer = create_image_transformer('image_right', mu_right_eye)
face_transformer = create_image_transformer('image_face', mu_face)

# face grid transformer just passes through the data
face_grid_transformer = caffe.io.Transformer({'facegrid': net.blobs['facegrid'].data.shape})


# set the batch size to 1
def set_batch_size(batch_size):
    net.blobs['image_left'].reshape(batch_size, 3, 224, 224)
    net.blobs['image_right'].reshape(batch_size, 3, 224, 224)
    net.blobs['image_face'].reshape(batch_size, 3, 224, 224)
    net.blobs['facegrid'].reshape(batch_size, 625, 1, 1)

set_batch_size(1)

#  net.forward()
if os.environ['GPU'] == 'true':
    caffe.set_device(0)  # if we have multiple GPUs, pick the first one
    caffe.set_mode_gpu()

net.forward()

def test_face(img, face, face_feature):
    eyes, face_grid = face_feature

    if len(eyes) < 2:
        return None

    start_ms = current_time()
    transformed_right_eye = right_eye_transformer.preprocess('image_right', crop_image(img, eyes[0]))
    transformed_left_eye = left_eye_transformer.preprocess('image_left', crop_image(img, eyes[1]))
    transformed_face = face_transformer.preprocess('image_face', crop_image(img, face))
    transformed_face_grid = face_grid.reshape(1, 625, 1, 1)

    net.blobs['image_left'].data[...] = transformed_left_eye
    net.blobs['image_right'].data[...] = transformed_right_eye
    net.blobs['image_face'].data[...] = transformed_face
    net.blobs['facegrid'].data[...] = transformed_face_grid

    output = net.forward()
    #  net.forward()
    print("Feeding through the network took " + str((current_time() - start_ms) * 1. / 1000) + "s")

    return np.copy(output['fc3'][0])


def test_faces(img, faces, face_features):
    outputs = []
    for i, face in enumerate(faces):
        output = test_face(img, face, face_features[i])

        outputs.append(output)

    return outputs
