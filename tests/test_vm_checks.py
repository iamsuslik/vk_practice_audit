from unittest.mock import patch, MagicMock
import pytest

from modules.vm_checks import check_resources


def test_cpu_check():
    with patch('psutil.cpu_percent', return_value=50), \
            patch('psutil.virtual_memory') as mock_mem, \
            patch('psutil.disk_usage', return_value=MagicMock(percent=60)), \
            patch('psutil.process_iter', return_value=[]):
        mock_mem.return_value.percent = 70

        config = {
            "thresholds": {
                "cpu": 80,
                "ram": 85,
                "max_vms": 10,
                "disk": 90
            }
        }

        result = check_resources(config)
        assert result["cpu"] == 50
        assert result["ram"] == 70