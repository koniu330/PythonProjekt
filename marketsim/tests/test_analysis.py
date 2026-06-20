from app.analysis import group_transactions_by_type, most_traded_assets, total_transaction_value


HISTORY = [
    {"type": "kupno_akcji", "asset": "CDR", "value": 100},
    {"type": "kupno_akcji", "asset": "CDR", "value": 120},
    {"type": "sprzedaz_akcji", "asset": "PKO", "value": 90},
]


def test_most_traded_assets():
    result = most_traded_assets(HISTORY)

    assert result[0] == ("CDR", 2)


def test_group_transactions_by_type():
    result = group_transactions_by_type(HISTORY)

    assert len(result["kupno_akcji"]) == 2
    assert len(result["sprzedaz_akcji"]) == 1


def test_total_transaction_value_all():
    assert total_transaction_value(HISTORY) == 310.0


def test_total_transaction_value_filtered():
    assert total_transaction_value(HISTORY, "kupno_akcji") == 220.0
