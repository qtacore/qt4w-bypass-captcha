# -*- coding: utf-8 -*-

import time

from qt4w import XPath
from qt4w.browser import Browser
from qt4w.webcontrols import WebPage, FrameElement
from qt4w_captcha.tencent import TencentCaptchaPage


class TencentCaptchaFrameElement(FrameElement):
    webpage_class = TencentCaptchaPage


class QQ007WebPage(WebPage):

    ui_map = {
        "体验用户": XPath('//a[text()="体验用户"]'),
        "可疑用户": XPath('//a[text()="可疑用户"]'),
        "恶意用户": XPath('//a[text()="恶意用户"]'),
        "体验验证码": XPath('//button[@id="code"]'),
        "验证码IFrame": {
            "type": TencentCaptchaFrameElement,
            "locator": XPath('//iframe[@id="tcaptcha_iframe"]'),
        },
    }


def test_captcha():
    Browser.register_browser("chrome", "chrome_headless.browser.ChromeHeadlessBrowser")
    browser = Browser()
    page = browser.find_by_url("https://007.qq.com/online.html", QQ007WebPage)
    page.control("可疑用户").click()
    page.control("体验验证码").click()
    time.sleep(1)
    page.control("验证码IFrame").framepage.validate()


if __name__ == "__main__":
    test_captcha()
