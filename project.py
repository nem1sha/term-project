import cv2 as cv
import numpy as np


class Photo:
    def __init__(self):
        self.img = None

    def contours(self):
        hsv_min = np.array((0, 0, 0), np.uint8)
        hsv_max = np.array((0, 0, 0), np.uint8)

        img = cv.imread(self.img)

        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        new_img = cv.inRange(hsv, hsv_min, hsv_max)  # применяем цветовой фильтр
        # ищем контуры и складируем их в переменную contours
        contours, hierarchy = cv.findContours(new_img.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        # отображаем контуры поверх изображения
        cv.drawContours(img, contours, -1, (255, 0, 0), 3, cv.LINE_AA, hierarchy, 1)
        cv.imshow('contours', img)  # выводим итоговое изображение в окно

        cv.waitKey()
        cv.destroyAllWindows()

    def svg(self):
        pass


class Video:
    def __init__(self, camera_id=0):
        self.camera_id = camera_id
        self.cap = cv.VideoCapture(camera_id)
        if not self.cap.isOpened():
            raise f'Cannot capture camera'

    def window(self):
        cv.namedWindow("result")
        cv.namedWindow("settings")

    def cap(self):
        if __name__ == '__main__':
            def nothing(*arg):
                pass
        cap = cv.VideoCapture(0)
        cv.createTrackbar('h1', 'settings', 0, 255, nothing)
        cv.createTrackbar('s1', 'settings', 0, 255, nothing)
        cv.createTrackbar('v1', 'settings', 0, 255, nothing)
        cv.createTrackbar('h2', 'settings', 255, 255, nothing)
        cv.createTrackbar('s2', 'settings', 255, 255, nothing)
        cv.createTrackbar('v2', 'settings', 255, 255, nothing)
        while True:
            flag, img = cap.read()
            hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

            h1 = cv.getTrackbarPos('h1', 'settings')
            s1 = cv.getTrackbarPos('s1', 'settings')
            v1 = cv.getTrackbarPos('v1', 'settings')
            h2 = cv.getTrackbarPos('h2', 'settings')
            s2 = cv.getTrackbarPos('s2', 'settings')
            v2 = cv.getTrackbarPos('v2', 'settings')

            # формируем начальный и конечный цвет фильтра
            h_min = np.array((h1, s1, v1), np.uint8)
            h_max = np.array((h2, s2, v2), np.uint8)

            # накладываем фильтр на кадр в модели HSV
            thresh = cv.inRange(hsv, h_min, h_max)

            cv.imshow('result', thresh)

            ch = cv.waitKey(5)
            if ch == 27:
                break

        cap.release()
        cv.destroyAllWindows()

