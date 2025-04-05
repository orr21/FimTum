from ..scrapper import Scrapper
from .urlSec import UrlSec

class SecScrapper(Scrapper):
    def __init__(self, url):
        self.url_handler = UrlSec(url)

    def get_data(self, quarter: int, year: int):
        """Returns a zip file with SEC filings for a given quarter and year

        :Parameters:
            quarter : int
                Quarter of the filings
            year : int
                Year of the filings

        Returns:
            zipfile.ZipFile: Zip file with the SEC filings

        Example:
        >>> FinTum.get_sec_zip("http://fake-url.com", quarter=1, year=2024)
        """
        zip_file = self.url_handler.get_zip(quarter, year)
        return zip_file