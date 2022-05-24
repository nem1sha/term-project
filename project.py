import cv2 as cv


class Camera:
    def __init__(self, camera_id=0):
        self.img = 'donut-1024x768.jpeg'
        self.camera_id = camera_id
        self.cap = cv.VideoCapture(camera_id)
        if not self.cap.isOpened():
            raise f'Cannot capture camera'

    def color_model(self):
        pass

    def color_filter(self):
        pass

    def trackbar(self):
        pass

    def svg(self):
        pass

class Photo(Camera):
    def contours_1(self):
        pass
    
    def contours_2(self):
        pass


class Video(Camera):
    def contours_3(self):
        pass
