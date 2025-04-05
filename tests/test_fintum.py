import pytest
import pandas as pd
import zipfile
from io import BytesIO
from unittest.mock import patch , Mock
from fintum.fintum import FinTum
from fintum.scrappers.sec.urlSec import UrlSec

def get_mock_zip():
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, mode="w") as zf:
        zf.writestr("test.txt", "contenido simulado")
    zip_buffer.seek(0)

    return zipfile.ZipFile(zip_buffer)

@patch.object(
    UrlSec, "get_links",
    return_value={"financial-statement-q1.zip"}
)
@patch.object(
    UrlSec, "get_zip",
    return_value=get_mock_zip()
)
def test_get_sec_zip(mock_get_links,mock_get_zip):
    mock_response = Mock()
    mock_response.status_code = 200
    with patch('requests.get', return_value=mock_response):
        result = FinTum.get_sec_zip("http://fake-url.com", quarter=1, year=2024)
    assert isinstance(result, zipfile.ZipFile), "Expected result to be a ZipFile"
    assert "test.txt" in result.namelist(), "Expected 'test.txt' inside the ZIP"

@patch('fintum.scrappers.yahoo.yahooScrapper.YahooScrapper.get_data')
def test_get_yahoo_data_returns_dataframe(mock_get_data):
    df_mock = pd.DataFrame({'Close': [100, 101]})
    mock_get_data.return_value = df_mock

    result = FinTum.get_yahoo_data("AAPL", "2024-01-01", "2024-01-10")

    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert 'Close' in result.columns