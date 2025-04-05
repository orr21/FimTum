import pytest
import requests
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime
from fintum.scrappers.sec.urlSec import UrlSec

def test_get_links():
    html = '''
    <a href="link1">Link 1</a>
    <a href="/link2">Link 2</a>
    <a href="https://sec.gov/link3.zip">Link 3</a>
    '''
    expected = {'link1', '/link2', 'https://sec.gov/link3.zip'}
    assert UrlSec.get_links(html) == expected

@pytest.fixture
def offline_url_sec():
    mock_response = MagicMock(text='<a href="/dummy.zip">Dummy</a>')
    with patch('requests.get', return_value=mock_response):
        sec = UrlSec("http://dummy.url")
        sec._valid_urls = set()
        return sec

def test_select_valid_urls():
    mock_html = '''
    <a href="/financial-statement/q1.zip">Q1</a>
    <a href="/files/financial-statement/q2.zip">Q2</a>
    <a href="/not-a-zip.txt">Text</a>
    '''
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.text = mock_html
        mock_get.return_value = mock_response
        
        url_sec = UrlSec("http://dummy.url")
        expected = {
            'https://www.sec.gov/financial-statement/q1.zip',
            'https://www.sec.gov/files/financial-statement/q2.zip',
        }
        assert url_sec._valid_urls == expected

def test_get_url_quarter_tag_exists(offline_url_sec):
    offline_url_sec._valid_urls = {
        "https://www.sec.gov/2023q1.zip",
        "https://www.sec.gov/2023_01.zip",
    }
    urls = offline_url_sec.get_url(1, 2023)
    assert urls == ["https://www.sec.gov/2023q1.zip"]

def test_get_url_month_tags(offline_url_sec):
    offline_url_sec._valid_urls = {
        "https://www.sec.gov/2023_04.zip",
        "https://www.sec.gov/2023_05.zip",
        "https://www.sec.gov/2023_06.zip",
    }
    urls = offline_url_sec.get_url(2, 2023)
    assert set(urls) == {
        "https://www.sec.gov/2023_04.zip",
        "https://www.sec.gov/2023_05.zip",
        "https://www.sec.gov/2023_06.zip",
    }

def test_get_url_invalid_year_low(offline_url_sec):
    with pytest.raises(ValueError):
        offline_url_sec.get_url(1, 2008)

def test_get_url_invalid_year_high(offline_url_sec):
    current_year = datetime.now().year
    with pytest.raises(ValueError):
        offline_url_sec.get_url(1, current_year + 1)

def test_get_url_invalid_quarter(offline_url_sec):
    with pytest.raises(ValueError):
        offline_url_sec.get_url(0, 2023)
    with pytest.raises(ValueError):
        offline_url_sec.get_url(5, 2023)

def test_get_url_not_valid_urls(offline_url_sec):
    with pytest.raises(ValueError):
        offline_url_sec.get_url(3, 2023)

def test_get_zip_success(offline_url_sec):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.content = b'fake zip content'
    with patch('requests.get', return_value=mock_response):
        offline_url_sec._valid_urls = {"https://www.sec.gov/2023q1.zip"}
        
        zip_files = offline_url_sec.get_zip(1, 2023)
        assert len(zip_files) == 1
        assert zip_files[0][0] == "2023q1.zip"
        assert zip_files[0][1] == b'fake zip content'

def test_get_zip_failure_standalone(offline_url_sec):
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("404 Not Found")

    offline_url_sec._valid_urls = {"https://www.sec.gov/2023q1.zip"}
    
    with patch('requests.get', return_value=mock_response):

        with pytest.raises(Exception) as excinfo:
            offline_url_sec.get_zip(1, 2023)

        expected_error = "Error downloading from https://www.sec.gov/2023q1.zip: 404 Not Found"
        assert expected_error in str(excinfo.value)