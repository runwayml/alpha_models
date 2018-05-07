import numpy as np
import cv2
import os
from lib import current_time

# print(os.environ['OPENCV_DATA'])

cascades_path = os.environ['OPENCV_DATA']
face_cascade = cv2.CascadeClassifier(cascades_path + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cascades_path + 'haarcascade_eye.xml')

print(cascades_path + 'haarcascade_frontalface_default.xml', cascades_path + 'haarcascade_eye.xml')

# This code is converted from https://github.com/CSAILVision/GazeCapture/blob/master/code/faceGridFromFaceRect.m

# Given face detection data, generate face grid data.
#
# Input Parameters:
# - frameW/H: The frame in which the detections exist
# - gridW/H: The size of the grid (typically same aspect ratio as the
#     frame, but much smaller)
# - labelFaceX/Y/W/H: The face detection (x and y are 0-based image
#     coordinates)
# - parameterized: Whether to actually output the grid or just the
#     [x y w h] of the 1s square within the gridW x gridH grid.

def faceGridFromFaceRect(frameW, frameH, gridW, gridH, labelFaceX, labelFaceY, labelFaceW, labelFaceH, parameterized):

    scaleX = gridW / frameW
    scaleY = gridH / frameH

    if parameterized:
      labelFaceGrid = np.zeros(4)
    else:
      labelFaceGrid = np.zeros(gridW * gridH)

    grid = np.zeros((gridH, gridW))

    # Use one-based image coordinates.
    xLo = round(labelFaceX * scaleX)
    yLo = round(labelFaceY * scaleY)
    w = round(labelFaceW * scaleX)
    h = round(labelFaceH * scaleY)

    if parameterized:
        labelFaceGrid = [xLo, yLo, w, h]
    else:
        xHi = xLo + w
        yHi = yLo + h

        # Clamp the values in the range.
        xLo = int(min(gridW, max(0, xLo)))
        xHi = int(min(gridW, max(0, xHi)))
        yLo = int(min(gridH, max(0, yLo)))
        yHi = int(min(gridH, max(0, yHi)))

        faceLocation = np.ones((yHi - yLo, xHi - xLo))
        grid[yLo:yHi, xLo:xHi] = faceLocation

        # Flatten the grid.
        grid = np.transpose(grid)
        labelFaceGrid = grid.flatten()

    return labelFaceGrid

def detect_eyes(face, img, gray):
    [x,y,w,h] = face
    roi_gray = gray[y:y+h, x:x+w]

    eyes = eye_cascade.detectMultiScale(roi_gray)
    eyes_sorted_by_size = sorted(eyes, key=lambda x: -x[2])
    largest_eyes = eyes_sorted_by_size[:2]
    # sort by x position
    largest_eyes.sort(key=lambda x: x[0])
    # offset by face start
    return list(map(lambda eye: [face[0] + eye[0], face[1] + eye[1], eye[2], eye[3]], largest_eyes))

def get_face_grid(face, frameW, frameH, gridSize):
    faceX,faceY,faceW,faceH = face

    return faceGridFromFaceRect(frameW, frameH, gridSize, gridSize, faceX, faceY, faceW, faceH, False)

def extract_image_features(img):
    start_ms = current_time()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_detections = face_cascade.detectMultiScale(gray, 1.3, 5)
    #  print('face detection took ' + str((current_time() - start_ms) / 1000.))

    left_to_right_face_detections = sorted(face_detections, key=lambda detection: detection[0])

    faces = []
    face_features = []
    for [x,y,w,h] in left_to_right_face_detections:
        face = [x, y, w, h]
        #  start_eyes = current_time()
        eyes = detect_eyes(face, img, gray)
        #  print('eye extraction '  + str((current_time() - start_eyes) / 1000.))
        face_grid = get_face_grid(face, img.shape[1], img.shape[0], 25)

        faces.append(face)
        face_features.append([eyes, face_grid])

    duration_ms = current_time() - start_ms
    #  print("Face and eye extraction took: ", str(duration_ms / 1000) + "s")

    return img, faces, face_features

def draw_detected_features(img, faces, face_features):
    # eye_images = []
    # for (ex,ey,ew,eh) in eyes:
    #     eye_images.append(np.copy(img[y+ey:y+ey+eh,x+ex:x+ex+ew]))
    for i, face in enumerate(faces):
        [x, y, w, h] = face
        eyes, face_grid = face_features[i]

        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

        for [ex,ey,ew,eh] in eyes:
            cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)


gridSize = 25
