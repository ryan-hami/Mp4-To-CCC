from PIL import Image
import cv2

def convert(file):
    cam = cv2.VideoCapture(file)

    frames = []

    while True:
        ret, frame = cam.read()
        if not ret: break
        frames.append(frame)

    cam.release()

    return [Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)) for frame in frames]
