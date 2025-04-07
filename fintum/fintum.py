from .crawler.sec.secCrawler import SecCrawler
from .crawler.yahoo.yahooCrawler import YahooCrawler

class FinTum:
    def __init__(self):
        pass
    
    @staticmethod
    def get_sec_zip(url: str, quarter: int, year: int):
        """Returns a zip file with SEC filings for a given quarter and year
        
        Parameters:
        url (str): URL of the SEC filings
        quarter (int): Quarter of the filings
        year (int): Year of the filings
        
        Returns:
        zipfile.ZipFile: Zip file with the SEC filings

        Example:
        >>> FinTum.get_sec_zip("https://www.sec.gov/data-research/sec-markets-data/financial-statement-notes-data-sets", quarter=1, year=2024)
        """
        return SecCrawler(url).get_data(quarter, year)

    @staticmethod
    def get_yahoo_data(ticker: str, start: str, end: str, period: str = 'max'):
        """Returns historical data from Yahoo Finance for a given ticker

        :Parameters:
            ticker : str
                Ticker of the stock
            start: str
                Download start date string (YYYY-MM-DD) or _datetime, inclusive.
                Default is 99 years ago
                E.g. for start="2020-01-01", the first data point will be on "2020-01-01"
            end: str
                Download end date string (YYYY-MM-DD) or _datetime, exclusive.
                Default is now
                E.g. for end="2023-01-01", the last data point will be on "2022-12-31"
            period: str
                Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                Either Use period parameter or use start and end

        Returns:
        pd.DataFrame: DataFrame with the historical data

        Example:
        >>> FinTum.get_yahoo_data("AAPL", "2024-01-01", "2024-01-10")
        >>> FinTum.get_yahoo_data("AAPL", "2024-01-01", "2024-01-10", period="1d")
        """
        return YahooCrawler().get_data(ticker, start, end, period)