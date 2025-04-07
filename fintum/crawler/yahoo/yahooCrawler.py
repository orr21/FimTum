import yfinance as yf
import pandas as pd
from ..crawler import Crawler

from typing import Optional

class YahooCrawler(Crawler):
    def __init__(self):
        super().__init__()
    
    def get_data(self,ticker: str, start: Optional[str] = None, end: Optional[str] = None, period: Optional[str] = 'max') -> pd.DataFrame:
        """Returns historical data from Yahoo Finance for a given ticker

        :Parameters:
            ticker : str
                Ticker of the stock
            period : str
                Valid periods: 1d,5d,1mo,3mo,6mo,1y,2y,5y,10y,ytd,max
                Either Use period parameter or use start and end
            start: str
                Download start date string (YYYY-MM-DD) or _datetime, inclusive.
                Default is 99 years ago
                E.g. for start="2020-01-01", the first data point will be on "2020-01-01"
            end: str
                Download end date string (YYYY-MM-DD) or _datetime, exclusive.
                Default is now
                E.g. for end="2023-01-01", the last data point will be on "2022-12-31"

        Returns:
        pd.DataFrame: DataFrame with the historical data

        Example:
        >>> FinTum.get_yahoo_data("AAPL", "2024-01-01", "2024-01-10")
        >>> FinTum.get_yahoo_data("AAPL", "2024-01-01", "2024-01-10", period="1d")
        """
        if ticker is None:
            raise ValueError("The 'ticker' parameter is required.")
        if not isinstance(ticker, str):
            raise ValueError("The 'ticker' parameter must be a string.")
        if  ticker.strip() == "":
            raise ValueError("The 'ticker' parameter is required.")
        

        try:
            df = yf.Ticker(ticker).history(ticker, start=start, end=end, period=period, raise_errors=True)
            if not df.empty:
                df['Ticker'] = ticker
                return df
            else:
                print(f"No data found for {ticker} in the specified date range.")
                return pd.DataFrame()
        except Exception as e:
            print(f"Error downloading data for {ticker}: {e}")
            return pd.DataFrame()