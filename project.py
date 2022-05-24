import cv2 as cv
import numpy as np


class Camera:
    def __init__(self, camera_id=0):
        self.img = 'donut-1024x768.jpeg'
        self.camera_id = camera_id
        self.cap = cv.VideoCapture(camera_id)
        if not self.cap.isOpened():
            raise f'Cannot capture camera'

    def color_model(self, img):
        hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)  # меняем цветовую модель с BGR на HSV
        return hsv

    def color_filter(self, hsv, hsv_min, hsv_max):
        thresh = cv.inRange(hsv, hsv_min, hsv_max)  # применяем цветовой фильтр
        return thresh

    def trackbar_for_photo(self):
        if __name__ == '__main__':
            def nothing(*arg):
                pass

        cv.namedWindow("result")  # создаем главное окно
        cv.namedWindow("settings")  # создаем окно настроек

        img = cv.imread(self.img)

        # создаем 6 бегунков для настройки начального и конечного цвета фильтра
        cv.createTrackbar('h1', 'settings', 0, 255, nothing)
        cv.createTrackbar('s1', 'settings', 0, 255, nothing)
        cv.createTrackbar('v1', 'settings', 0, 255, nothing)
        cv.createTrackbar('h2', 'settings', 255, 255, nothing)
        cv.createTrackbar('s2', 'settings', 255, 255, nothing)
        cv.createTrackbar('v2', 'settings', 255, 255, nothing)

        while True:
            hsv = Camera.color_model(self, img)

            # считываем значения бегунков
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
            thresh = Camera.color_filter(self, hsv, h_min, h_max)

            ch = cv.waitKey(5)
            if ch == 27:
                break

            cv.imshow('result', thresh)

        cv.destroyAllWindows()

        return h1, s1, v1, h2, s2, v2

    def trackbar_for_video(self):
        if __name__ == '__main__':
            def nothing(*arg):
                pass

        cv.namedWindow("result")
        cv.namedWindow("settings")

        cap = cv.VideoCapture(0)

        cv.createTrackbar('h1', 'settings', 0, 255, nothing)
        cv.createTrackbar('s1', 'settings', 0, 255, nothing)
        cv.createTrackbar('v1', 'settings', 0, 255, nothing)
        cv.createTrackbar('h2', 'settings', 255, 255, nothing)
        cv.createTrackbar('s2', 'settings', 255, 255, nothing)
        cv.createTrackbar('v2', 'settings', 255, 255, nothing)

        while True:
            flag, img = cap.read()
            hsv = Camera.color_model(self, img)

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
            thresh = Camera.color_filter(self, hsv, h_min, h_max)

            cv.imshow('result', thresh)

            ch = cv.waitKey(5)
            if ch == 27:
                break

        cv.imwrite('cam.png', img)

        cap.release()
        cv.destroyAllWindows()

        return h1, s1, v1, h2, s2, v2

    def svg(self):
        pass


class Photo(Camera):
    def contours_1(self):
        img = cv.imread(self.img)

        print('Сейчас Вам предстоит ввести значения для фильтра')
        h1 = input('Введите значение для h1')
        s1 = input('Введите значение для s1')
        v1 = input('Введите значение для v1')
        h2 = input('Введите значение для h2')
        s2 = input('Введите значение для s2')
        v2 = input('Введите значение для v2')

        hsv = Camera.color_model(self, img)
        hsv_min = np.array((h1, s1, v1), np.uint8)
        hsv_max = np.array((h2, s2, v2), np.uint8)

        new_img = Camera.color_filter(self, hsv, hsv_min, hsv_max)  # применяем цветовой фильтр
        # ищем контуры и складируем их в переменную contours
        contours, hierarchy = cv.findContours(new_img.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        index = 0
        layer = 0

        cv.drawContours(img, contours, index, (255, 0, 0), 2, cv.LINE_AA, hierarchy, layer)
        cv.imshow('contours', img)

        cv.waitKey()
        cv.destroyAllWindows()

    def contours_2(self):
        pass


class Video(Camera):
    def contours_3(self):
        pass
