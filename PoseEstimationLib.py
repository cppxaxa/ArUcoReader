import cv2
import numpy as np

def CalculateFocalLength(image):
    size = image.shape
    return size[1]

def CalculateCenter(image):
    size = image.shape
    return (size[1]/2, size[0]/2)

def GenerateCameraMatrix(focal_length, center):
    return np.array(
                            [[focal_length, 0, center[0]],
                            [0, focal_length, center[1]],
                            [0, 0, 1]], dtype = "double"
                            )

class PoseProjector:
    ''' Here atlease one unit in model_points should have value (0,0,0) '''
    def __init__(self, model_points):
        self.model_points = model_points
    
    def ProjectPoints(self, tansformationPoint, image, image_points):
        tansformationPoint = np.array([tansformationPoint])
        focal_length = CalculateFocalLength(image)
        center = CalculateCenter(image)
        dist_coeffs = np.zeros((4,1))
        camera_matrix = GenerateCameraMatrix(focal_length, center)
        (success, rotation_vector, translation_vector) = cv2.solvePnP(self.model_points, image_points, camera_matrix, dist_coeffs)
        (end_points_2D, jacobian) = cv2.projectPoints(tansformationPoint, rotation_vector, translation_vector, camera_matrix, dist_coeffs)
        return end_points_2D
    