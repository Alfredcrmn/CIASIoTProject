import cv2
from mtcnn.mtcnn import MTCNN
import os


def process_face(image_path):
    """
    Detect and process the face in the image. Save the processed face and return its file path.
    """
    detector = MTCNN()
    img = cv2.imread(image_path)
    faces = detector.detect_faces(img)

    if not faces:
        return None

    for face in faces:
        x1, y1, width, height = face["box"]
        x2, y2 = x1 + width, y1 + height

        face_img = cv2.resize(img[y1:y2, x1:x2], (150, 200), interpolation=cv2.INTER_CUBIC)
        processed_path = image_path.replace(".jpg", "_processed.jpg")
        cv2.imwrite(processed_path, face_img)
        return processed_path

    return None


def compare_faces(uploaded_image_path, stored_image_path):
    """
    Compare two face images and return True if they match.
    """
    orb = cv2.ORB_create()

    # Read the images
    img1 = cv2.imread(uploaded_image_path, 0)
    img2 = cv2.imread(stored_image_path, 0)

    # Detect keypoints and descriptors
    kp1, des1 = orb.detectAndCompute(img1, None)
    kp2, des2 = orb.detectAndCompute(img2, None)

    # Match features
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)

    # Calculate the similarity ratio
    similar = [m for m in matches if m.distance < 70]
    if len(matches) == 0:
        return False
    similarity = len(similar) / len(matches)
    
    # Return true if similarity is high enough
    return similarity >= 0.94
