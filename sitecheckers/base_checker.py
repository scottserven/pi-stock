from datetime import datetime, timedelta
from typing import List, Tuple


class ProductPageStatus:

    def __init__(self, url: str, description: str, checker: "BaseChecker"):
        self.url: str = url
        self._description: str = description
        self._checker: "BaseChecker" = checker
        self._alert_allowed = True
        self._delay = 10  # minimum number of seconds between actual site checks
        self._quantity: int = 0
        self._is_available: bool = False
        self._last_available_check: datetime = datetime(1, 1, 1)

    def is_available(self) -> bool:
        """
        Check the product website for availability and update internal states as necessary
        :return: True if the product is available
        """
        last_is_available = self._is_available

        # Only check the website itself every 5 minutes, regardless of how often this method is called
        if self._last_available_check + timedelta(seconds=self._delay) < datetime.now():
            (self._is_available, self._quantity) = self._checker.check_stock(self)
            self._last_available_check = datetime.now()

        # if we were available, and are now not available, re-enable the alerts for the next time it becomes available
        if last_is_available and not self._is_available:
            self._alert_allowed = True

        return self._is_available

    def alert_allowed(self) -> bool:
        return self._alert_allowed

    def alerted(self):
        """
        If an alert was sent, don't allow another to get sent again unless it goes out of stock and comes back in
        :return:
        """
        self._alert_allowed = False

    def get_alert_message(self):
        """
        For readability, we're using an explicit method for the alert messages instead of __str__
        :return:
        """
        message = ""
        if self._quantity and self._quantity > 0:
            message = f"{self._description} - Status: {('Out of Stock', 'Available')[self._is_available]}, Qty: {self._quantity} - {self.url}"
        else:
            message = f"{self._description} - Status: {('Out of Stock', 'Available')[self._is_available]} - {self.url}"
        return message

    def __str__(self):
        return f"{self.url} - {self._description}"

class BaseChecker:

    def check_stock(self, product_page: ProductPageStatus) -> Tuple[bool, int]:
        """ Performs the check for a given site.  Should be overridden by subclasses. """
        return False, 0

