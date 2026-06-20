from unittest.mock import Mock, patch

from app.nbp_api import get_currency_rate


def test_get_currency_rate_with_mocked_api():
    get_currency_rate.cache_clear()

    fake_response = Mock()
    fake_response.raise_for_status.return_value = None
    fake_response.json.return_value = {"rates": [{"mid": 4.25}]}

    with patch("app.nbp_api.requests.get", return_value=fake_response):
        result = get_currency_rate("EUR")

    assert result == 4.25
