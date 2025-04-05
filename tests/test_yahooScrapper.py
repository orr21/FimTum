import pytest
from unittest.mock import Mock
import pandas as pd
import yfinance as yf
from fintum.scrappers.yahoo.yahooScrapper import YahooScrapper

@pytest.fixture
def mock_yfinance(monkeypatch):
    """Fixture to mock yfinance and its responses"""
    mock_ticker = Mock()
    mock_history = Mock()
    
    mock_ticker.return_value.history = mock_history
    monkeypatch.setattr(yf, "Ticker", mock_ticker)
    
    return mock_ticker, mock_history

def test_valid_ticker(mock_yfinance, capsys):
    mock_ticker, mock_history = mock_yfinance
    test_data = pd.DataFrame({
        'Open': [100, 101],
        'Close': [102, 103],
        'Volume': [1000, 2000]
    }, index=pd.date_range("2024-01-01", periods=2))
    mock_history.return_value = test_data.copy()

    scrapper = YahooScrapper()
    result = scrapper.get_data("AAPL")

    assert not result.empty, "The DataFrame should not be empty for a valid ticker."
    assert 'Ticker' in result.columns, "The DataFrame should include the 'Ticker' column."
    assert result['Ticker'].isin(['AAPL']).all(), "All records should have the ticker 'AAPL'."
    assert len(result) == 2, "The DataFrame should have 2 rows."
    captured = capsys.readouterr()
    assert "Error" not in captured.out, "There should be no error messages printed."

def test_invalid_ticker():
    with pytest.raises(ValueError, match="The 'ticker' parameter must be a string."):
        YahooScrapper().get_data(123)
    with pytest.raises(ValueError, match="The 'ticker' parameter is required."):
        YahooScrapper().get_data("")
    with pytest.raises(ValueError, match="The 'ticker' parameter is required."):
        YahooScrapper().get_data(None)

def test_no_data_found(mock_yfinance, capsys):
    mock_ticker, mock_history = mock_yfinance
    mock_history.return_value = pd.DataFrame()  
    
    scrapper = YahooScrapper()
    result = scrapper.get_data("INVALID")
    
    assert result.empty, "The returned DataFrame should be empty when no data is found."
    captured = capsys.readouterr()
    assert "No data found for INVALID" in captured.out, "It should print a message indicating no data was found for INVALID."

def test_network_error(mock_yfinance, capsys):
    mock_ticker, mock_history = mock_yfinance
    mock_history.side_effect = ConnectionError("API Error")
    
    scrapper = YahooScrapper()
    result = scrapper.get_data("AAPL")
    
    assert result.empty, "The returned DataFrame should be empty when a network error occurs."
    captured = capsys.readouterr()
    assert "Error downloading data for AAPL: API Error" in captured.out, "It should print an error message for AAPL."

def test_different_parameters(mock_yfinance):
    mock_ticker, mock_history = mock_yfinance
    test_data = pd.DataFrame({'Close': [150]}, index=[pd.Timestamp("2024-01-01")])
    mock_history.return_value = test_data
    
    scrapper = YahooScrapper()
    
    result = scrapper.get_data("MSFT", start="2024-01-01", end="2024-01-02")
    assert len(result) == 1, "There should be exactly one row for MSFT with the given date range."
    
    result = scrapper.get_data("GOOG", period="1mo")
    assert not result.empty, "The result for GOOG with period='1mo' should not be empty."