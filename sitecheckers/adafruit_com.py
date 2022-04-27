import re
import requests
from typing import Tuple
from .base_checker import ProductPageStatus, BaseChecker


class AdaFruitChecker(BaseChecker):

    def check_stock(self, product_page: ProductPageStatus) -> Tuple[bool, int]:
        """
        The AdaFruit website will tell us the quantity along with availability.
        :param product_page: the ProductPageStatus that will be updated based on what the website says
        :return: nothing
        """
        response = requests.get(product_page.url)
        match = re.search('>in stock</span>', response.text, re.IGNORECASE)
        available = match is not None
        if available:
            return True, 1
        else:
            return False, 0
