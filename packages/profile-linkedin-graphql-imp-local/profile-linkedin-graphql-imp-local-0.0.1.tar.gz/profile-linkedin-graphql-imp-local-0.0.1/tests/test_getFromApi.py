import sys
import os
from unittest.mock import MagicMock


import pytest

# Get the absolute path to the parent directory of the test file
current_dir = os.path.dirname(os.path.abspath(__file__))
# Get the path to the 'src' directory
src_path = os.path.join(current_dir, '../src')
# Add the 'src' directory to the Python path
sys.path.append(src_path)

# Now you should be able to import the module
from getFromApi import getProfile

# Rest of your test code

def mock_getProfiles(monkeypatch):
    expected_data = {
        "given_name": "Idan",
        "family_name": "Asis",
        "email": "idanasis86@gmail.com"
    }
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = MagicMock(**expected_data)
    monkeypatch.setattr(getProfile, "getProfiles", MagicMock(return_value=mock_response))

@pytest.mark.test
def test_getProfiles_returns_name_and_email():
    profile = getProfile()
    result = profile.getProfiles()

    assert result[0]["given_name"] == "Idan"
    assert result[0]["family_name"] == "Asis"
    assert result[0]["email"] == "idanasis86@gmail.com"
    
    
    