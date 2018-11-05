import cv2
import urllib.request as urllib
import numpy as np
import cv2.aruco as aruco

def getImageFromShotUri(url):
    imgResp = urllib.urlopen(url)
    imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img = cv2.imdecode(imgNp,-1)
    return img

def draw(img, center, imgpts):
    center = tuple(center)
    img = cv2.line(img, center, tuple(imgpts[0]), (255,0,0), 5)
    img = cv2.line(img, center, tuple(imgpts[1]), (0,255,0), 5)
    img = cv2.line(img, center, tuple(imgpts[2]), (0,0,255), 5)
    return img

def calculate(corners):    
    center = [50, 50]
    imgpts = [
        [90, 50],
        [50, 90],
        [40, 40]
    ]
    return center, imgpts

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

    '''    detectMarkers(...)
        detectMarkers(image, dictionary[, corners[, ids[, parameters[, rejectedI
        mgPoints]]]]) -> corners, ids, rejectedImgPoints
        '''
        #lists of ids and the corners beloning to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    
    
    #corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
    
    ## Find the rotation and translation vectors.
    #rvecs, tvecs, inliers = cv2.solvePnPRansac(objp, corners2, mtx, dist)

    ## project 3D points to image plane
    #imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
    
    center, imgpts = calculate(corners)
    
    cameraMatrix = [
        [1,0,1],
        [0,1,0],
        [0,0,1]
        ]
    
    imgPoints = [
        [1,1,1,1],
        [1,1,1,1]
        ]
    
    ret, rvec, tvec = cv2.solvePnP(np.array(corners), np.array(imgPoints), np.array(cameraMatrix), np.array([]))
    
    print("rvec")
    print(rvec)
    
    print("tvec")
    print(tvec)
    
    orig = draw(orig, center, imgpts)
    
    
    print(corners)

    #It's working.
    # my problem was that the cellphone put black all around it. The alrogithm
    # depends very much upon finding rectangular black blobs

    orig = aruco.drawDetectedMarkers(orig, corners)

    print("IDS")
    print(ids)


    # Display the resulting frame
    cv2.imshow('frame', orig)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
        # break
    cv2.waitKey()
    break
