import cv2


class FaceBlur:
    def __init__(self):
        cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        self.face_cascade = cv2.CascadeClassifier(cascade_path)

    def blur_faces(self, frame, enable: bool = True):
        if not enable:
            return frame

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=3,  # Reduced from 5 to detect more faces
            minSize=(30, 30),  # Reduced from 60x60 to detect smaller faces
        )

        for (x, y, w, h) in faces:
            face_region = frame[y : y + h, x : x + w]
            if face_region.size == 0:
                continue
            # Use a larger blur kernel for better visibility
            blurred = cv2.GaussianBlur(face_region, (51, 51), 20)
            frame[y : y + h, x : x + w] = blurred

        return frame
