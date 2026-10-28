from api import register_endpoint
from users import InMemoryUserRepository, UserService


class FakeMailer:
    """Заглушка почты: письма запоминаются, наружу ничего не уходит."""

    def __init__(self):
        self.sent = []

    def send(self, to, text):
        self.sent.append((to, text))


def test_register_endpoint_returns_201_and_email():
    service = UserService(InMemoryUserRepository(), FakeMailer())
    status, body = register_endpoint(
        service,
        {"email": "anna@example.com", "password": "secret123"},
    )
    assert status == 201
    assert body == {"email": "anna@example.com"}
