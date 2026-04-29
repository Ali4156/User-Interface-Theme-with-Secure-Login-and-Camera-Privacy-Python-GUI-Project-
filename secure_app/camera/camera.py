import cv2
from security.logger import Logger
from .face_blur import FaceBlur


class CameraHandler:
    def __init__(self, logger: Logger = None):
        self.logger = logger or Logger()
        self.capture = None
        self.running = False
        self.blur_faces = True
        self.face_blur = FaceBlur()

    def start_camera(self) -> None:
        if self.running:
            return
        self.capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        if not self.capture.isOpened():
            self.logger.log("CAMERA", "Camera open failed")
            raise RuntimeError("Unable to access the camera.")
        self.running = True
        self.logger.log("CAMERA", "Camera started")

    def stop_camera(self) -> None:
        if self.capture is not None:
            self.capture.release()
        self.capture = None
        self.running = False
        self.logger.log("CAMERA", "Camera stopped")

    def get_frame(self):
        if not self.running or self.capture is None:
            return None
        success, frame = self.capture.read()
        if not success:
            return None
        frame = cv2.flip(frame, 1)
        processed = self.face_blur.blur_faces(frame, enable=self.blur_faces)
        return cv2.cvtColor(processed, cv2.COLOR_BGR2RGB)
