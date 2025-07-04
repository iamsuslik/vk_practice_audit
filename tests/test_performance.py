import pytest
from unittest.mock import patch
from modules.performance_test import run_disk_test, run_network_test

def test_disk_test():
    with patch('subprocess.run') as mock_run:
        mock_run.return_value.stderr = "1048576 bytes copied, 0.123 s, 8.5 MB/s"
        result = run_disk_test()
        assert "8.5 MB/s" in result

def test_network_test():
    with patch('ping3.ping', return_value=50):
        result = run_network_test()
        assert result == "50.00 ms"