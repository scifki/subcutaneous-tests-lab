import pytest
import requests
import responses

from loyalty import BASE_URL, get_bonus_points


@responses.activate
def test_get_bonus_points_returns_points_from_api():
    responses.add(responses.GET, f"{BASE_URL}/api/users/42", json={"points": 150}, status=200)
    assert get_bonus_points(42) == 150


@responses.activate
def test_get_bonus_points_raises_on_server_error():
    responses.add(responses.GET, f"{BASE_URL}/api/users/42", json={"error": "boom"}, status=500)
    with pytest.raises(requests.HTTPError):
        get_bonus_points(42)
