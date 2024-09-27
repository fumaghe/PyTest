import pytest
import requests
from unittest.mock import patch
from io import BytesIO
from mymodule import extract_first_status_link, get_pdf_for_ingredient

# Test per estrarre il primo link
@patch('mymodule.requests.Session.get')
def test_extract_first_status_link(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.text = "<table><a href='../file.pdf'></a></table>"
    session = requests.Session()
    url = "https://example.com"
    link = extract_first_status_link(session, url)
    assert link == "https://cir-reports.cir-safety.org/file.pdf"

# Test per ottenere il PDF
@patch('mymodule.requests.Session.get')
def test_get_pdf_for_ingredient(mock_get):
    mock_response = mock_get.return_value
    mock_response.status_code = 200
    mock_response.content = b'%PDF-1.4'
    session = requests.Session()
    ingredient_id = '12345'
    pdf = get_pdf_for_ingredient(session, ingredient_id)
    assert isinstance(pdf, BytesIO)
