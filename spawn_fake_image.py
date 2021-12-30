import time

from PIL import Image, ImageDraw, ImageFont
import datetime
import os
import glob
import sys


class spawn_fake_image(object):
    def __init__(self):
        self.YY = datetime.datetime.now().year
        self.MM = datetime.datetime.now().month
        self.DD = datetime.datetime.now().day
        self.hh = datetime.datetime.now().hour
        self.mm = datetime.datetime.now().minute
        self.ss = datetime.datetime.now().second
        self.formated_time = datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S')
        self.data_img_seed = Image.open("resource/data_code_seed.jpg")
        self.health_img_seed = Image.open("resource/health_code_seed.jpg")
        self.helth_font1 = ImageFont.truetype('resource/myfont.ttf', size=90)
        self.helth_font2 = ImageFont.truetype('resource/myfont.ttf', size=200)
        self.data_font = ImageFont.truetype('resource/myfont.ttf', size=44)
        self.black = 'rgb(0,0,0)'
        self.gray = 'rgb(180,180,180)'

    def draw(self):
        data_draw = ImageDraw.Draw(self.data_img_seed)
        health_draw = ImageDraw.Draw(self.health_img_seed)
        (dx, dy) = (428, 606)
        (hx, hy) = (325, 280)
        data_draw.text((dx, dy), self.formated_time, fill=self.gray, font=self.data_font)
        health_draw.text((hx, hy + 14), str(self.MM), fill=self.black, font=self.helth_font1)
        health_draw.text((hx + 225, hy + 14), str(self.DD), fill=self.black, font=self.helth_font1)
        health_draw.text((hx - 210, hy + 135), str(self.hh).zfill(2), fill=self.black, font=self.helth_font2)
        health_draw.text((hx + 100, hy + 135), str(self.mm).zfill(2), fill=self.black, font=self.helth_font2)
        health_draw.text((hx + 390, hy + 135), str(self.ss).zfill(2), fill=self.black, font=self.helth_font2)

    def spawn(self):
        self.data_img_seed.save("/tmp/data_code.jpg")
        self.health_img_seed.save("/tmp/health_code.jpg")
        self.data_img_seed.close()
        self.health_img_seed.close()

    def __del__(self):
        py_files = glob.glob('/tmp/*.jpg')
        for py_file in py_files:
            try:
                os.remove(py_file)
            except OSError as e:
                print(f"Error:{e.strerror}")

    def print_time(self):
        print(self.YY, self.MM, self.DD, self.hh, self.mm, self.ss)


if __name__ == "__main__":
    x = spawn_fake_image()
    x.draw()
    x.spawn()
    h = input()
    del (x)