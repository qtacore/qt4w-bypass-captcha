# -*- coding: utf-8 -*-

import time


def smart_drag(webview, x1, y1, x2, y2):
    step = 10
    step_count = int(((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 // step) + 1
    step_x = (x2 - x1) / step_count
    step_y = (y2 - y1) / step_count
    webview.drag(x1, y1, x1, y1, step=0, fire_release_event=False)
    for i in range(step_count):
        webview.drag(
            x1 + step_x * i,
            y1 + step_y * i,
            x1 + step_x * (i + 1),
            y1 + step_y * (i + 1),
            step=0,
            fire_press_event=False,
            fire_release_event=False,
        )
        time.sleep(0.01)
    webview.drag(x2, y2, x2, y2, step=0, fire_press_event=False)
