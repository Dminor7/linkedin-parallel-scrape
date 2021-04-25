import re
from datetime import datetime

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.expected_conditions import _find_element
from typing import List

headless_options = Options()
headless_options.headless = True
HEADLESS_OPTIONS = headless_options

headful_options = Options()
headful_options.headless = False
HEADFUL_OPTIONS = headful_options

def flatten_list(l:List[List]) -> List:
    return [item for sublist in l for item in sublist]


def split_lists(lst: List, num: int) -> List[List]:
    k, m = divmod(len(lst), num)
    return [lst[i * k + min(i, m): (i+1) * k + min(i + 1, m)] for i in range(num)]


class TextChanged(object):
    def __init__(self, locator, text):
        self.locator = locator
        self.text = text

    def __call__(self, driver):
        actual_text = _find_element(driver, self.locator).text
        return actual_text != self.text


class AnyEC(object):
    def __init__(self, *args):
        self.ecs = args

    def __call__(self, driver):
        for fn in self.ecs:
            try:
                if fn(driver):
                    return True
            except:
                pass
        return False