import re
import requests
from zipfile import ZipFile
from typing import Set, List
from datetime import datetime

from ..urlBuilder import UrlBuilder

class UrlSec(UrlBuilder):
    BASE_URL = "https://www.sec.gov"
    HEADERS = {
        "User-Agent": "MyDataScraper/1.0 (oscar.rico101@alu.ulpgc.es)"
    }

    quarter_to_months = {
        1: ["01", "02", "03"],
        2: ["04", "05", "06"],
        3: ["07", "08", "09"],
        4: ["10", "11", "12"],
    }

    def __init__(self, url: str):
        super().__init__(url)
        self._valid_urls = self.select_valid_urls()

    def get_url(self, quarter: int, year: int) -> List[str]:
        """Returns a list of URLs for the specified quarter and year.

        :Parameters:
            quarter : int
                Quarter of the filings
            year : int
                Year of the filings

        Returns:
            List[str]: List of URLs for the specified quarter and year.

        Example:
        >>> FinTum.get_url(quarter=1, year=2024)
        """
        urls = set()

        if not isinstance(quarter, int) or not isinstance(year, int):
            raise ValueError("Quarter and year must be integers.")
        if year < 2009:
            raise ValueError("Invalid year. Must be an integer greater than 2009.")
        if year > datetime.now().year:
            raise ValueError("Invalid year. Must be an integer less than the current year.")
        if quarter not in self.quarter_to_months:
            raise ValueError("Invalid quarter. Must be an integer between 1 and 4.")

        quarter_tag = f"{year}q{quarter}"
        urls.update(url for url in self._valid_urls if quarter_tag in url)

        if len(urls) == 0:
            for month in self.quarter_to_months[quarter]:
                month_tag = f"{year}_{month}"
                urls.update(url for url in self._valid_urls if month_tag in url)

        if len(urls) == 0:
            raise ValueError("No valid URLs found for the specified quarter and year.")
    
        return list(urls)

    def get_zip(self, quarter: int, year: int) -> List[tuple[str, ZipFile]]:
        """Downloads zip files from the SEC website for the specified quarter and year.
        
        :Parameters:
            quarter : int
                Quarter of the filings
            year : int
                Year of the filings

        Returns:
            List[tuple[str, ZipFile]]: List of tuples containing the name of the zip file and the zip file itself.

        Example:
        >>> FinTum.get_zip(quarter=1, year=2024)
        """
        urls = self.get_url(quarter, year)
        zip_results = []

        for url in urls:
            try:
                response = requests.get(url, headers=self.HEADERS)
                response.raise_for_status()
                zip_name = url.split("/")[-1]
                zip_results.append((zip_name, response.content))
            except Exception as e:
                raise Exception(f"Error downloading from {url}: {e}")

        return zip_results

    def select_valid_urls(self) -> Set[str]:
        """Selects valid URLs from the SEC website.
        Returns:
            Set[str]: Set of valid URLs.
        
            Example:
            >>> FinTum.select_valid_urls()
        """
        response = requests.get(self.url, headers=self.HEADERS)
        response.raise_for_status()
        html = response.text
        links = self.get_links(html)
        return {
            self.BASE_URL + link for link in links
            if link.endswith('.zip') and "financial-statement" in link
        }

    @staticmethod
    def get_links(html: str) -> Set[str]:
        """Extracts links from the HTML content.
        :Parameters:
            html : str
                HTML content of the page
                
        Returns:
            Set[str]: Set of links.

        Example:
        >>> FinTum.get_links(html)
        """
        return set(re.findall(r'href="([^"]+)"', html))