# -*- coding: utf-8 -*-

import requests
from PIL import Image
from qt4w import XPath
from qt4w.webcontrols import WebPage

from . import bypass, image


class TencentCaptchaPage(WebPage):

    ui_map = {
        "背景图片": XPath('//img[@id="slideBg"]'),
        "滑块图片": XPath('//img[@id="slideBlock"]'),
        "滑块": XPath('//div[@id="tcaptcha_drag_thumb"]'),
        "刷新1": XPath('//div[@id="reload"]'),
        "刷新2": XPath('//div[@id="e_reload"]'),
    }

    def validate(self):
        bg_url = self.control("背景图片").src
        response = requests.get(bg_url)
        save_path = "bg.jpg"
        with open(save_path, "wb") as fp:
            fp.write(response.content)
        img = Image.open(save_path)
        img = image.binarize(img)
        img = image.remove_discrete_points(img)
        left, top = image.locate_shadow_area(img)
        if left <= 0 or top <= 0:
            if self.control('刷新1').visible:
                self.control("刷新1").click()
            else:
                self.control("刷新2").click()
            return self.validate()

        rect1 = self.control("背景图片").rect
        rect2 = self.control("滑块图片").rect
        print(rect1, rect2, left, top)
        print(img.size, left, top)
        rect = self.control("滑块").rect
        bypass.smart_drag(
            self._webview,
            rect[0] + rect[2] / 2,
            rect[1] + rect[3] / 2,
            rect[0] + rect[2] / 2 + left - (rect2[0] - rect1[0]) - 30,
            rect[1] + rect[3] / 2,
        )
