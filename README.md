# Linkedin Scraper 
## Supports 
- SearchScraper
---
- ## Run Sequentially
```python
from linkedin_scrape import SearchScraper, HEADLESS_OPTIONS, HEADFUL_OPTIONS
import pandas as pd

# Login to linkedin and copy paste the li_at cookie value below
li_at = ''

Query = SearchScraper.args()

# List the search queries below
search_queries = [
    Query(company='spotify', keywords='data analyst')
]

search_data = []

with SearchScraper(driver_options=HEADFUL_OPTIONS, cookie=li_at) as scraper:
    # Get each search query employee data, add to search_data list
    for query in search_queries:
        employees = scraper.scrape(query=query).search_employees
        for employee in employees:
            employee['company'] = query.company
            employee['title'] = query.keywords
            search_data.append(employee)

# Turn into dataframe
df = pd.DataFrame(search_data)
df.to_csv('output.csv', index=False)

```
- ## Run Parallely
```python
from linkedin_scrape import scrape_in_parallel, SearchScraper

# Login to linkedin and copy paste the li_at cookie value below
li_at = ''

Query = SearchScraper.args()

# List the search queries below
search_queries = [
    Query(company='spotify', keywords='data analyst'),
    Query(company='facebook', keywords='data analyst'),
    Query(company='google', keywords='data analyst'),
    Query(company='netflix', keywords='data analyst'),
]


## Scrape each search query employee data, create 'searches.json' file, use 4 browser instances
scrape_in_parallel(
    scraper_type=SearchScraper,
    items=search_queries,
    output_file="searches.json",
    num_instances=4,
    cookie=li_at
)
```