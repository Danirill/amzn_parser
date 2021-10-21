from .. import settings
from ..scraper import scrape


def get_product_data_by_asin(e, asin):
    url = f"{settings.ROOT_URL}/dp/{asin}"
    data = scrape(e, url)
    if data:
        return data
    else:
        return None