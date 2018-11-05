import cv2
import urllib.request as urllib
import numpy as np
import cv2.aruco as aruco

from PoseEstimationLib import *

def getImageFromShotUri(url):
    imgResp = urllib.urlopen(url)
    imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img = cv2.imdecode(imgNp,-1)
    return img

while True:
    # frame = getImageFromShotUri("http://192.168.43.161:8080/shot.jpg")
    frame = cv2.imread("shot1.jpg")
    orig = frame.copy()
        #cv2.imshow("", image)
        # Capture frame-by-frame
    #ret, frame = cap.read()
    #print(frame.shape) #480x640
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_6X6_250)
    parameters =  aruco.DetectorParameters_create()
    
    #lists of ids and the corners beloning to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    print(corners)

    orig = aruco.drawDetectedMarkers(orig, corners)
    
    model_points = np.array([
        (0.0, 0.0, 0.0),
        (-5.0, 5.0, 0.0),
        (5.0, 5.0, 0.0),
        (5.0, -5.0, 0.0),
        (-5.0, -5.0, 0.0)
    ])
    poseProjector = PoseProjector(model_points)
    
    for i in range(len(corners)):
        input_coords = corners[i][0]
        
        center = np.array([(input_coords[0][0] + input_coords[2][0])/2, (input_coords[0][1] + input_coords[2][1])/2])
        
        tmp = [center.tolist(), input_coords[0].tolist(), input_coords[1].tolist(), input_coords[2].tolist(), input_coords[3].tolist()]
        input_coords = np.array(tmp, dtype="double")
        print(input_coords)
        result = poseProjector.ProjectPoints((0.0,0.0,5.0), frame, input_coords)
        
        print("IDS")
        print(ids)
    
        result = result[0][0]
        print(result)
        
        orig = cv2.line(orig, (int(center[0]), int(center[1])), (int(result[0]), int(result[1])), (255, 0, 0), 2)

    # Display the resulting frame
    cv2.imshow('frame', orig)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
        # break
    cv2.waitKey()
    break
