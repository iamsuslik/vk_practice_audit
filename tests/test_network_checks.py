import pytest
from unittest.mock import patch, MagicMock
from modules.network_checks import check_network


@pytest.fixture
def mock_config():
    return {
        "ntp_server": "pool.ntp.org",
        "smtp_server": "smtp.example.com",
        "smtp_port": 587
    }


def test_ntp_success(mock_config):
    with patch('ntplib.NTPClient') as mock_ntp:
        mock_response = MagicMock()
        mock_response.offset = 0.5
        mock_ntp.return_value.request.return_value = mock_response

        result = check_network()
        assert result["ntp"] is True


def test_smtp_success(mock_config):
    with patch('smtplib.SMTP') as mock_smtp:
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server

        result = check_network()
        assert result["smtp"] is True