#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import os.path
import re
import requests

class HuabanCrawler():

   def __init__(self):
        self.home_url = "http://huaban.com/boards/19365690/"
        self.images = []
        if not os.path.exists('D:/images'):
            os.mkdir('D:/images')

   def load_homepage(self):
        return requests.get(url = self.home_url).content

   def make_ajax_url(self, no):
        return self.home_url + "?iops3bru&max=" + no + "&limit=20&wfl=1"

   def load_more(self, max_no):
        return requests.get(url = self.make_ajax_url(max_no)).content

   def process_data(self, html_page):
        prog = re.compile(r'"pins":.*')
        app_pins = prog.findall(html_page.decode('utf-8'))
        null = None
        true = True
        false = False
        if app_pins == []:
            return None
        result = eval(app_pins[0][7:-2])
        for i in result:
            info = {}
            info['id'] = str(i['pin_id'])
            info['url'] = "http://hbimg.b0.upaiyun.com/" + i["file"]["key"] + "_fw658"
            if 'image' == i["file"]["type"][:5]:
                info['type'] = i["file"]["type"][6:]
            else:
                info['type'] = 'NoName'
            self.images.append(info)

   def save_image(self, image_name, content):
        with open(image_name, 'wb') as fp:
            fp.write(content)

   def get_image_info(self, num=20):
        self.process_data(self.load_homepage())
        for i in range((num-1)//20):
            self.process_data(self.load_more(self.images[-1]['id']))
        return self.images

   def download_images(self):
        print("{} images will be downloaded".format(len(self.images)))
        for key, image in enumerate(self.images):
            print('downloading {0} ...'.format(key))
            try:
                req = requests.get(image["url"])
            except :
                print('error')
            image_fullname = os.path.join("D:/images", image["id"] + "." + image["type"])
            self.save_image(image_fullname, req.content)

if __name__ == '__main__':
    hc = HuabanCrawler()
    hc.get_image_info(500)
    hc.download_images()
