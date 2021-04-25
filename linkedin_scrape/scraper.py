import selenium.webdriver
import time
from os import environ
from abc import abstractmethod
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager


class Scraper(object):
    """
    Wrapper for selenium Chrome driver with methods to scroll through a page and
    to scrape and parse info from a linkedin page
    Params:
        - cookie {str}: li_at session cookie required to scrape linkedin profiles
        - driver {webdriver}: driver to be used for scraping
        - scroll_pause {float}: amount of time to pause (s) while incrementally
        scrolling through the page
        - scroll_increment {int}: pixel increment for scrolling
        - timeout {float}: time to wait for page to load first batch of async content
    """

    def __init__(self, cookie=None, scraperInstance=None, driver=selenium.webdriver.Chrome, driver_options=None, scroll_pause=0.1, scroll_increment=300, timeout=10):
        if type(self) is Scraper:
            raise Exception(
                'Scraper is an abstract class and cannot be instantiated directly')

        if scraperInstance:
            self.was_passed_instance = True
            self.driver = scraperInstance.driver
            self.scroll_increment = scraperInstance.scroll_increment
            self.timeout = scraperInstance.timeout
            self.scroll_pause = scraperInstance.scroll_pause
            return

        self.was_passed_instance = False
        if driver_options:
            self.driver = driver(ChromeDriverManager(
            ).install(), chrome_options=driver_options)
        else:
            self.driver = driver(ChromeDriverManager().install())
        # self.scroll_pause = scroll_pause
        # self.scroll_increment = scroll_increment
        self.timeout = timeout
        self.driver.get('http://www.linkedin.com')
        self.driver.set_window_size(1920, 1080)

        if 'LI_EMAIL' in environ and 'LI_PASS' in environ:
            self.login(environ['LI_EMAIL'], environ['LI_PASS'])
        else:
            if not cookie and 'LI_AT' not in environ:
                raise ValueError(
                    'Must either define LI_AT environment variable, or pass a cookie string to the Scraper')
            elif not cookie:
                cookie = environ['LI_AT']
            self.driver.add_cookie({
                'name': 'li_at',
                'value': cookie,
                'domain': '.linkedin.com'
            })

    @abstractmethod
    def scrape(self):
        raise Exception('Must override abstract method scrape')

    def login(self, email, password):
        email_input = self.driver.find_element_by_css_selector(
            'input.login-email')
        password_input = self.driver.find_element_by_css_selector(
            'input.login-password')
        email_input.send_keys(email)
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)

    def get_html(self):
        try:
            return self.driver.page_source
        except:
            return ''

    def wait(self, condition):
        return WebDriverWait(self.driver, self.timeout).until(condition)

    def wait_for_el(self, selector):
        return self.wait(EC.presence_of_element_located((
            By.CSS_SELECTOR, selector
        )))

    def __enter__(self):
        return self

    def __exit__(self, *args, **kwargs):
        self.quit()

    def quit(self):
        print("Quiting Browser ...")
        if self.driver and not self.was_passed_instance:
            self.driver.quit()
