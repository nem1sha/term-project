import cv2 as cv
import numpy as np
from PIL import Image
import os
import base64
import struct
import imghdr


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

    def format_svg(self, img):
        def get_image_size(fname):
            with open(fname, 'rb') as fhandle:
                head = fhandle.read(24)
                if len(head) != 24:
                    return
                if imghdr.what(fname) == 'png':
                    check = struct.unpack('>i', head[4:8])[0]
                    if check != 0x0d0a1a0a:
                        return
                    width, height = struct.unpack('>ii', head[16:24])
                elif imghdr.what(fname) == 'gif':
                    width, height = struct.unpack('<HH', head[6:10])
                elif imghdr.what(fname) == 'jpeg':
                    try:
                        fhandle.seek(0)
                        size = 2
                        ftype = 0
                        while not 0xc0 <= ftype <= 0xcf:
                            fhandle.seek(size, 1)
                            byte = fhandle.read(1)
                            while ord(byte) == 0xff:
                                byte = fhandle.read(1)
                            ftype = ord(byte)
                            size = struct.unpack('>H', fhandle.read(2))[0] - 2
                        fhandle.seek(1, 1)
                        height, width = struct.unpack('>HH', fhandle.read(4))
                    except Exception:
                        return
                else:
                    return
                return width, height

        start_svg_tag = """<?xml version="1.0" encoding="UTF-8" standalone="no"?>
        <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
        "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
        <svg version="1.1"
        xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink"
        """

        end_svg_tag = """</svg>"""
        for img in os.listdir("."):
            if img.endswith(".jpg") or img.endswith(".png") or img.endswith(".gif"):
                width, height = get_image_size(img)
                img_file = open(img, 'rb')
                base64data = base64.b64encode(img_file.read())
                base64String = f'<image xlink:href="data:image/png;base64,{base64data.decode("utf-8")}" width="{width}" height="{height}" x="0" y="0" />'
                svg_size = f'width="{width}px" height="{height}px" viewBox="0 0 {width} {height}">'
                f = open(os.path.splitext(img)[0] + ".svg", 'w')
                f.write(start_svg_tag + svg_size + base64String + end_svg_tag)
                print('Converted ' + img + ' to ' + os.path.splitext(img)[0] + ".svg")

    def white_background(self, img):
        fn = Image.open(img)
        new_img = Image.new('RGB', fn.size, 'white')
        new_img.save('white.png')
        return 'white.png'


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

        fn = Camera.white_background(self, self.img)
        vis = cv.imread(fn)
        cv.drawContours(vis, contours, index, (255, 0, 0), 2, cv.LINE_AA, hierarchy, layer)
        cv.imwrite('contours.png', vis)

        cv.waitKey()
        cv.destroyAllWindows()

        return 'contours.png'

    def contours_2(self):
        img = cv.imread(self.img)

        h1, s1, v1, h2, s2, v2 = Camera.trackbar_for_photo(self)
        hsv = Camera.color_model(self, img)
        h_min = np.array((h1, s1, v1), np.uint8)
        h_max = np.array((h2, s2, v2), np.uint8)

        new_img = Camera.color_filter(self, hsv, h_min, h_max)  # применяем цветовой фильтр
        # ищем контуры и складируем их в переменную contours
        contours, hierarchy = cv.findContours(new_img.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        # отображаем контуры поверх изображения
        index = 0
        layer = 0

        fn = Camera.white_background(self, self.img)
        vis = cv.imread(fn)
        cv.drawContours(vis, contours, index, (255, 0, 0), 2, cv.LINE_AA, hierarchy, layer)
        cv.imwrite('contours.png', vis)

        cv.waitKey()
        cv.destroyAllWindows()

        return 'contours.png'


class Video(Camera):
    def contours_3(self):
        h1, s1, v1, h2, s2, v2 = Camera.trackbar_for_video(self)
        img = cv.imread('cam.png')

        hsv = Camera.color_model(self, img)
        h_min = np.array((h1, s1, v1), np.uint8)
        h_max = np.array((h2, s2, v2), np.uint8)

        new_img = Camera.color_filter(self, hsv, h_min, h_max)  # применяем цветовой фильтр
        # ищем контуры и складируем их в переменную contours
        contours, hierarchy = cv.findContours(new_img.copy(), cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

        # отображаем контуры поверх изображения
        index = 0
        layer = 0

        fn = Camera.white_background(self, self.img)
        vis = cv.imread(fn)
        cv.drawContours(vis, contours, index, (255, 0, 0), 2, cv.LINE_AA, hierarchy, layer)
        cv.imwrite('contours.png', vis)

        cv.waitKey()
        cv.destroyAllWindows()

        return 'contours.png'
    
    
photo = Photo()
video = Video()
print('Вы пользуетесь программой поиска контуров на картинке (с камеры) '
      'и сохранения их в вектороное изображение svg.')
print('Ознокомтесь с инструкцией по пользованию программой '
      'в файле README.md на сайте https://github.com/nem1sha/term-project')
n = int(input('Если вы ознакомились с инструкцией, введите с клавиатуры "1",  а затем ENTER'))
if n == 1:
    var = int(input('Вам предстоит выбрать вариант работы программы '
                    ' от 1 до 3 (варианты работы программы прописанны в инструкции)'))
    if var == 1:
        rez_1 = photo.contours_1()
        photo.format_svg(rez_1)
    elif var == 2:
        rez_2 = photo.contours_2()
        photo.format_svg(rez_2)
    elif var == 3:
        rez_3 = video.contours_3()
        video.format_svg(rez_3)
    elif var != 1 and var != 2 and var != 3:
        print('Такого варианта нет, попробуйте заново.')
