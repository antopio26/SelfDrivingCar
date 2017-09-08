import socket
import time
import json
import datetime

import numpy as np
import cv2
import base64
import pygame

import csv, os

server = 'localhost'
port = 5555

path = '/media/pi/VOLUME/'
path_ = ''
_path = ''
file = 'sessionLog.csv'
csvfile = None

loop_0 = True
run_0 = True
run_1 = False
isStop = True

p_frame = False


def main():
    
    global loop_0
    global server
    global port
    global run_1
    global p_frame

    # Initialize procedure
    camera, s, clock = init()

    # Connect to server
    s.connect((server, port))

    while loop_0:
        # Recive joystick data
        try:
            j_data = get_jData(s)
        except:
            loop_0 = False
            break

        # Read image from camera
        retval, image = camera.read()

        # Send frame
        try:
            sendFrame(image, s)
        except:
            loop_0 = False
            break

        if p_frame and not j_data[3]:
            run_1 = not run_1

        if run_1:
            init_record()
            record(image, j_data)
        else:
            stopRec()
        
        p_frame = j_data[3] 

        print(j_data)
    
        clock.tick(20)

    camera.release()

def init(res = (403, 247)):
    # Initialize pygame stuff
    pygame.init()
    clock = pygame.time.Clock()

    # Initialize opencv stuff
    width, height = res
    camera = cv2.VideoCapture(0)
    camera.set(3,width)
    camera.set(4,height)
    camera.set(int(cv2.CAP_PROP_FPS), 10)

    # Initialize client socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    return (camera, s, clock);

def get_jData(socket_):
    # Recieve data from server
    result = socket_.recv(25).decode('utf-8')

    # Convert it into an object
    joystick_data = json.loads(result)
    return joystick_data;

def sendFrame(image, socket_, quality = 60):
    # Define encode param and encoding image into .jpg format
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 60]
    retval, buffer = cv2.imencode('.jpg', image, encode_param)

    #Send all data converted
    socket_.sendall(buffer)
    return;

def init_record():
    global path
    global file
    global csvfile
    global run_0
    global isStop
    global path_
    global _path

    if run_0:
        date_ = str(datetime.datetime.now()) 
        dir_name = 'dataLog_' + date_[:-7].replace(' ', '_').replace(':', '-')
        dir_ = path + dir_name
        print(dir_)
        os.makedirs(dir_)
        os.makedirs(dir_ + '/IMGs')
        file_path = dir_ + '/' + file
        csvfile = open(file_path, 'w', newline='')
        run_0 = False
        isStop = False
        path_ = 'G:\\' + dir_name + '\\IMGs'
        _path = dir_+ '/IMGs'
    
    return;
    
    
def record(_image, j_data):
    global csvfile
    global path_
    global _path

    date = str(datetime.datetime.now())
    file_name = _path + '/center_' + date.replace(' ', '_').replace(':', '-') + '.jpg'
    img = cv2.resize(_image, (320, 196), interpolation = cv2.INTER_CUBIC)
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
    cv2.imwrite(file_name, img, encode_param)
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    file_dir = path_ + '\\center_' + date.replace(' ', '_') + '.jpg'
    csvwriter.writerow([file_dir, j_data[0], j_data[1], j_data[2]])
    return;

def stopRec():
    global csvfile
    global isStop
    global run_0 

    if not isStop:
        run_0 = True
        isStop = True
        csvfile.close()
    return;

if __name__ == '__main__':
    main()