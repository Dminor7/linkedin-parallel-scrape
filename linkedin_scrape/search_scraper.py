from .scraper import Scraper
import json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from urllib.parse import urlencode
import time
from .search import Search
from .utils import AnyEC

class Query:
    def __init__(self, company, keywords):
        self.company = company
        self.keywords = keywords
    @property
    def query(self) -> str:
        return urlencode({"company":self.company,"keywords":self.keywords})
    @property
    def key(self) -> str:
        return f'{self.company} - {self.keywords}'

class SearchScraper(Scraper):
    def scrape(self, query:Query) -> Search:
        self.load_initial(query.query)
        search_html = self.get_html()
        return Search(search_html)

    def load_initial(self, query: str) -> None:
        url = 'https://www.linkedin.com/search/results/people/?{}&origin=FACETED_SEARCH'.format(query)

        self.driver.get(url)
        try:
            myElem = WebDriverWait(self.driver, self.timeout).until(AnyEC(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.search-filters-bar')),
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.search-no-results__image-container')),
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, '.search-reusables__filters-bar-grouping'))
            ))
        except TimeoutException as e:
            raise ValueError(
                """Took too long to load search results.  Common problems/solutions:
                1. Invalid LI_AT value: ensure that yours is correct (linkedin
                   update frequently)
                2. Slow Internet: increase the timeout parameter in the Scraper constructor""")

    @classmethod
    def args(cls) -> Query:
        return Query

    