import re
import json
from typing import Tuple
import requests
from .base_checker import ProductPageStatus, BaseChecker


class PiShopChecker(BaseChecker):

    def check_stock(self, product_page: ProductPageStatus) -> Tuple[bool, int]:
        """
        Based on the JSON data in the HTML file, that looks like:
        var BCData = {"csrf_token":"5b7b17ad3270e5a0739f442987f6a4c69c0b8425dfc8605f89d900bab839a0f1","product_attributes":{"sku":"1182","upc":null,"mpn":null,"gtin":null,"weight":null,"base":true,"image":null,"price":{"without_tax":{"formatted":"$21.90","value":21.9,"currency":"USD"},"tax_label":"Tax"},"out_of_stock_behavior":"label_option","out_of_stock_message":"Out of stock","available_modifier_values":[],"in_stock_attributes":[],"stock":15,"instock":true,"stock_message":null,"purchasable":true,"purchasing_message":null}};
        var BCData = {"csrf_token":"5b7b17ad3270e5a0739f442987f6a4c69c0b8425dfc8605f89d900bab839a0f1","product_attributes":{"sku":"8GB-9006","upc":null,"mpn":null,"gtin":null,"weight":null,"base":true,"image":null,"price":{"without_tax":{"formatted":"$75.00","value":75,"currency":"USD"},"tax_label":"Tax"},"out_of_stock_behavior":"label_option","out_of_stock_message":"Out of stock","available_modifier_values":[125,136,193,159,135,137],"in_stock_attributes":[125,136,193,159,135,137],"stock":0,"instock":false,"stock_message":"Out of stock","purchasable":true,"purchasing_message":"The selected product combination is currently unavailable."}};
        :param product_page: the ProductPageStatus that will be updated based on what the website says
        :return: nothing
        """
        response = requests.get(product_page.url)
        match = re.search('var BCData = (.*}});', response.text)
        quantity = 0
        available = match is not None
        if available:
            stock_data = json.loads(match.group(1))
            available = stock_data['product_attributes']['instock']
            quantity = int(stock_data['product_attributes']['stock'])
        return available, quantity
