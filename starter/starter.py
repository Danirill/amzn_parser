import sys
sys.path.append("..")

import csv
from selectorlib import Extractor

import settings

from scraper import scrape

e = Extractor.from_yaml_file('selectors.yml')

with open("categories.txt", 'r') as categories_list, \
        open("queries.txt", 'r') as queries_list, \
        open('../search/search_urls.txt', 'w') as outfile, \
        open('../search/search_urls.csv', 'w') as csvfile:
    csv_urls = csv.writer(csvfile)
    for category_name in categories_list.read().splitlines():
        url = f"{settings.ROOT_URL}/s?i={category_name}"
        for query in queries_list.read().splitlines():
            accurate_url = f"{url}&k={query}"
            data = scrape(e, accurate_url)
            if data:
                try:
                    arr = data['disabled']
                    max_page = int(arr[-1])
                    for i in range(1, max_page + 1):
                        new_url = accurate_url + f"&page={i}"
                        print(new_url, file=outfile)
                        csv_urls.writerow([new_url, category_name, query])
                except Exception as err:
                    print(err)
                    print(accurate_url, file=outfile)
