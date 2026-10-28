import requests

BASE_URL = "https://loyalty.example.com"


def get_bonus_points(user_id):
    """Возвращает бонусные баллы пользователя из внешнего сервиса лояльности."""
    response = requests.get(f"{BASE_URL}/api/users/{user_id}", timeout=5)
    response.raise_for_status()
    return response.json()["points"]
