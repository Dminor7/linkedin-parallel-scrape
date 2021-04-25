from .parse import Parse
from typing import List, Dict


class Search(Parse):
    def __init__(self, search_html):
        self.search_employee_template = {
            "name": "//div[contains(@class,'entity-result__content')]//a/span/span[1]",
            "connection": "//div[contains(@class,'entity-result__content')]//span[contains(@class,'image-text-lockup__text')]",
            "url": "//div[contains(@class,'entity-result__content')]//a/@href",
            "job_role": "div.entity-result__primary-subtitle",
            "location": "div.entity-result__secondary-subtitle",
            "info": "p.entity-result__summary"
        }
        self.search_employees_template = {
            "employees(//div[contains(@class,'entity-result__content')])": [
                {
                    "name": ".//a[@data-entity-action-source='actor']/span/span[1]",
                    "connection": ".//span[contains(@class,'image-text-lockup__text')]",
                    "url": ".//a[@data-entity-action-source='actor']/@href",
                    "job_role": " div.entity-result__primary-subtitle",
                    "location": " div.entity-result__secondary-subtitle",
                    "info": " p.entity-result__summary",
                    "related_connections": " span.entity-result__simple-insight-text"

                }
            ]
        }
        self.search_html = search_html

    @property
    def search_employee(self) -> Dict:
        return self.recursive_extract(self.search_html, self.search_employee_template)

    @property
    def search_employees(self) -> List:
        data = self.recursive_extract(
            self.search_html, self.search_employees_template)
        return data["employees"]
