from .. import settings
from ..scraper import scrape


def get_reviews_by_asin(e, asin):
    url = f"{settings.ROOT_URL}/product-reviews/{asin}/?ie=UTF8&reviewerType=all_reviews"
    data = scrape(e, url)
    if data:
        return data
    else:
        return None
