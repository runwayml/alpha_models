import pydarknet
from pydarknet import Detector, Image
import cv2
import os

if __name__ == "__main__":
    print('1')
    net = Detector(bytes("cfg/yolov2-tiny.cfg", encoding="utf-8"), bytes("weights/yolov2-tiny.weights", encoding="utf-8"), 0, bytes("cfg/coco.data",encoding="utf-8"))
    print('2')
    img = cv2.imread(os.path.join("data", 'dog.jpg'))

    print('3')
    img2 = Image(img)
    print('4')
    results = net.detect(img2)
    print('5')
    print(results)
    # for cat, score, bounds in results:
    #     x, y, w, h = bounds
    #     cv2.rectangle(img, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)),(255, 0, 0), thickness=2)
    #     cv2.putText(img,str(cat.decode("utf-8")),(int(x),int(y)),cv2.FONT_HERSHEY_DUPLEX,4,(00,255), thickness=2)
    # cv2.imwrite(os.path.join("output",file_name), img)
