import time
import numpy as np

def current_time():
    return int(round(time.time() * 1000))

def crop_image(img, crop):
    return img[crop[1]:crop[1]+crop[3],crop[0]:crop[0]+crop[2],:] 


def lerp(a, b, percentage):
    return a + (b-a)*percentage

def length(a, b):
    return ((b[0] - b[1])**2  + (a[0] - a[1])**2) ** (1/2.)

def smooth_outputs(outputs, frame_time, previous_outputs, previous_frame_time):
    if previous_frame_time is None:
        return outputs

    smoothed_outputs = []
    for i, output in enumerate(outputs):
        #  print(i, ' num previous', len(previous_outputs))
        if output is not None and i < len(previous_outputs) and previous_outputs[i] is not None:
            frame_diff = min(frame_time - previous_frame_time, 500)
            percentage = frame_diff / 500.
            
            smoothed_output = np.array((2, 1), dtype=np.float32)
            previous_output = previous_outputs[i]

            if (length(previous_output, output) < 5):
                smoothed_output = previous_output
            else:
                smoothed_output[0] = lerp(previous_output[0], output[0], percentage)
                smoothed_output[1] = lerp(previous_output[1], output[1], percentage)

            smoothed_outputs.append(smoothed_output)
        else:
            smoothed_outputs.append(output)

    return smoothed_outputs

def to_int_list(numpy_list):
    return map(lambda x: int(x), numpy_list)

def to_face_json(face):
    if face is None:
        return None

    return to_int_list(face)

def to_eye_json(eyes, index):
    if eyes is None:
        return None
    if (len(eyes) < index + 1):
        return None
    return to_int_list(eyes[index])

def to_gaze_json(gaze):
    if gaze is None:
        return None

    return gaze.tolist()

def to_output_json(faces, face_features, gazes):
    results = []
    for i, face in enumerate(faces):
        eyes, face_grid = face_features[i]
        result = {
            'face': to_face_json(face),
            'eye_left': to_eye_json(eyes, 0),
            'eye_right': to_eye_json(eyes, 1),
            'gaze': to_gaze_json(gazes[i])
        }
        results.append(result)

    print(results)
    return results

