import socket
import time
import json

import numpy as np
import cv2
import base64

camera = cv2.VideoCapture(0)
'''
camera.set(3,320)
camera.set(4,160)
'''
retval, image = camera.read()

# Initialize client socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = 'localhost'
port = 5555

# Connect to server
s.connect((server, port))

while True :
    result =  s.recv(25).decode('utf-8')
    data_loaded = json.loads(result)

    retval, image = camera.read()   

    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 50]
    retval, buffer = cv2.imencode('.jpg', image, encode_param)
    jpg_as_text = base64.b64encode(buffer)

    s.sendall(jpg_as_text)
    
    print(data_loaded)