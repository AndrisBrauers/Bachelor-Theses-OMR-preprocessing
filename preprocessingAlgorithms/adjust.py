import cv2
import numpy as np
from scipy.stats import mode

# Function to detect the main angle of the text lines
def get_rotation_angle(image):
    edges = cv2.Canny(image, 50, 150, apertureSize=3)
    # Detect points that form a line using HoughLinesP
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, 100, minLineLength=100, maxLineGap=10)
    # Calculate the angle of each line
    angles = []
    for line in lines:
        x1, y1, x2, y2 = line[0]
        angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))
        angles.append(angle)

    # Get the most common angle
    most_common_angle = mode(angles)[0]
    # The angle is in the range [-90, 90], but we need to convert it to [-180, 180]
    if most_common_angle < -90:
        most_common_angle += 90
    elif most_common_angle > 90:
        most_common_angle -= 90
    return most_common_angle


# Function to rotate an image by a given angle
def rotate_image(image, angle):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    # Perform the rotation
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated


def find_largest_contour(image):
    # Find the contours in the image
    contours, _ = cv2.findContours(image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Sort the contours by area and then return the largest one
    largest_contour = max(contours, key=cv2.contourArea)
    # Approximate the contour to a polygon
    peri = cv2.arcLength(largest_contour, True)
    approx = cv2.approxPolyDP(largest_contour, 0.02 * peri, True)
    return approx


def order_points(pts):
    # Initialize a list of coordinates that will be ordered such that the first entry in the list is the top-left,
    # the second entry is the top-right, the third is the bottom-right, and the fourth is the bottom-left
    rect = np.zeros((4, 2), dtype="float32")

    # The top-left point will have the smallest sum, whereas the bottom-right point will have the largest sum
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]

    # Now, compute the difference between the points, the top-right point will have the smallest difference,
    # whereas the bottom-left will have the largest difference
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]

    # Return the ordered coordinates
    return rect

def four_point_transform(image, pts):
    # Obtain a consistent order of the points
    rect = np.array([
        pts[0], pts[1],
        pts[2], pts[3]], dtype="float32")

    # Get the top-left, top-right, bottom-right, and bottom-left points
    (tl, tr, br, bl) = rect

    # Compute the width of the new image
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))

    # Compute the height of the new image
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))

    # Construct the destination points
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    # Compute the perspective transform matrix and apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

    return warped

def correct_rotation_and_perspective(img, img_name, output_directory='output'):
    # Correct rotation

    rotation_angle = get_rotation_angle(img)

    rotated_image = rotate_image(img, rotation_angle)

    # Apply edge detection to find contours on the rotated image
    edged = cv2.Canny(rotated_image, 75, 200)
    
    # Find the largest contour which will hopefully be the outline of the sheet
    approx = find_largest_contour(edged)
    
    if approx is None or len(approx) != 4:
        print(f'Could not find four points corresponding to the document corners. \n {output_directory}/{img_name}')
        return
    
    # Obtain the four points of the contour
    pts = order_points(approx.reshape(4, 2))
    
    # Apply the four-point transform to obtain a top-down view of the image
    warped = four_point_transform(rotated_image, pts)

    cv2.imwrite(f'{output_directory}/{img_name}.jpg', warped)

    return warped

