import socket
import time
import json
import datetime

import numpy as np
import cv2
import base64
import pygame

import csv, os

server = '192.168.1.17'
port = 5555

path = '/media/pi/VOLUME'
file = 'sessionLog.csv'
csvfile = None

loop_0 = True
run_0 = False
run_1 = False
isStop = True

p_frame = False

def main():
    # Initialize procedure
    cap, s, clock = init()

    # Connect to server
    s.connect((server, port))

    while loop_0:
        # Recive joystick data
        try:
            j_data = get_jData()
        except:
            loop_0 = False

        # Read image from camera
        retval, image = camera.read()

        # Send frame
        try:
            sendFrame(image)
        except:
            loop_0 = False

        if p_frame and not j_data[3]:
            run_1 = not run_1

        if run_1:
            path_ = init_record()
            record(image, j_data, path_)
        else:
            stopRec()
        
        p_frame = j_data[3] 

        print(data_loaded)
    
        clock.tick(15)

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

def get_jData():
    # Recieve data from server
    result =  s.recv(25).decode('utf-8')

    # Convert it into an object
    joystick_data = json.loads(result)
    return joystick_data;

def sendFrame(image, quality = 60):
    # Define encode param and encoding image into .jpg format
    encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 60]
    retval, buffer = cv2.imencode('.jpg', image, encode_param)

    #Send all data converted
    s.sendall(buffer)
    return;

def init_record():
    if run_0:
        date_ = datetime.datetime.now() 
        dir_ = path + 'dataLog:' + date[:-7].replace(' ', '_', 1)
        os.makedirs(dir_)
        os.makedirs(dir_ + 'IMGs')
        csvfile = open(file, 'w', newline='')
        run_0 = False
        isStop = False
        return 'G:\\' + dir_ + 'IMGs';
    else:
        return;
    
    
def record(image, j_data, path_):
    date = datetime.datetime.now()
    file_name = path + '\\center_' + date.replace(' ', '_', 1) + '.jpg'
    img = cv2.resize(image, (320, 196), interpolation = cv2.INTER_CUBIC)
    cv2.imwrite(file_name, img)
    csvwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow([file_name, j_data[0], j_data[1], j_data[2]])
    return;

def stopRec():
    if not isStop:
        isStop = True
        csvfile.close()
    return;

if __name__ == '__main__':
    main()