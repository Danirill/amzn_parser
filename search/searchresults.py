import csv
import errno
import os
import sys
import json
import settings

from selectorlib import Extractor
from products.amazon import get_product_data_by_asin
from reviews.reviews import get_reviews_by_asin
from scraper import scrape
from utils import lookahead

e = Extractor.from_yaml_file('search_results.yml')
reviews_e = Extractor.from_yaml_file('../reviews/selectors.yml')
product_e = Extractor.from_yaml_file('../products/selectors.yml')


# def main():
#     with open("search_urls.txt", 'r') as urllist, open('search_results_output.json', 'w') as outfile:
#         outfile.write("{\"data\": [\n")
#         for url in urllist.read().splitlines():
#             success = False
#             attempts = 0
#             while not success and attempts < settings.RETRIES_AFTER_FAIL:
#                 attempts += 1
#                 try:
#                     success = True
#                     data = scrape(e, url)
#                     if data:
#                         for product, has_more in lookahead(data['products']):
#                             # product['search_url'] = url
#                             asin = product['asin']
#                             product['reviews_data'] = get_reviews_by_asin(reviews_e, asin)
#                             product['product_data'] = get_product_data_by_asin(product_e, asin)
#                             print("Saving Product: %s" % product['title'])
#                             json.dump(product, outfile)
#                             if has_more:
#                                 outfile.write(",\n")
#                 except Exception as err:
#                     with open('logs.txt', 'a') as logfile:
#                         logfile.write(str(err))
#                     success = False
#
#         outfile.write("}]\n")

def new_main():
    counter = {}
    with open("search_urls.csv", 'r') as urllist:
        spamreader = csv.reader(urllist)
        for row in spamreader:
            url = row[0]
            category = row[1]
            query = row[2]
            success = False
            attempts = 0
            if (category, query) not in counter:
                counter[(category, query)] = 0
            while not success and \
                    attempts < settings.RETRIES_AFTER_FAIL and \
                    counter[(category, query)] < settings.MAX_PRODUCTS_BY_CATEGORY:
                attempts += 1
                try:
                    path = f"../output/{category}/{query}/outfile.json"
                    if not os.path.exists(os.path.dirname(path)):
                        try:
                            os.makedirs(os.path.dirname(path))
                        except OSError as exc:  # Guard against race condition
                            if exc.errno != errno.EEXIST:
                                raise
                    mode = 'a' if os.path.exists(path) else 'w'
                    with open(path, mode) as outfile:
                        success = True
                        data = scrape(e, url)
                        if data:
                            for product, has_more in lookahead(data['products']):
                                # product['search_url'] = url
                                asin = product['asin']
                                product['reviews_data'] = get_reviews_by_asin(reviews_e, asin)
                                product['product_data'] = get_product_data_by_asin(product_e, asin)
                                print("Saving Product: %s" % product['title'])
                                counter[(category, query)] += 1
                                json.dump(product, outfile)
                                if has_more:
                                    outfile.write(",\n")
                except Exception as err:
                    with open('logs.txt', 'a') as logfile:
                        logfile.write(str(err) + "\n")
                    success = False

if __name__ == '__main__':
    try:
        new_main()
    except KeyboardInterrupt:
        print('Interrupted')
        with open('search_results_output.json', 'a') as outfile:
            outfile.write("]}\n")
        sys.exit(0)
