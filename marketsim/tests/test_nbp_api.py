from unittest.mock import Mock, patch

import pytest

from app.nbp_api import NBPApiError, get_currency_rate


def test_get_currency_rate_success():
    get_currency_rate.cache_clear()

    fake_response = Mock()
    fake_response.status_code = 200
    fake_response.json.return_value = {
        "table": "A",
        "currency": "dolar amerykański",
        "code": "USD",
        "rates": [
            {
                "no": "001/A/NBP/2026",
                "effectiveDate": "2026-01-01",
                "mid": 4.25,
            }
        ],
    }
    fake_response.raise_for_status.return_value = None

    with patch("app.nbp_api.requests.get", return_value=fake_response):
        assert get_currency_rate("usd") == 4.25


def test_get_currency_rate_404():
    get_currency_rate.cache_clear()

    fake_response = Mock()
    fake_response.status_code = 404

    with patch("app.nbp_api.requests.get", return_value=fake_response):
        with pytest.raises(NBPApiError):
            get_currency_rate("XYZ")


def test_get_currency_rate_wrong_code():
    get_currency_rate.cache_clear()

    with pytest.raises(NBPApiError):
        get_currency_rate("EURO")