import pytest

from users import InMemoryUserRepository, UserAlreadyExists, UserService, hash_password


class FakeMailer:
    """Заглушка вместо настоящей почты: запоминает отправленные письма."""

    def __init__(self):
        self.sent = []

    def send(self, to, text):
        self.sent.append((to, text))


@pytest.fixture
def repository():
    return InMemoryUserRepository()


@pytest.fixture
def mailer():
    return FakeMailer()


@pytest.fixture
def service(repository, mailer):
    return UserService(repository, mailer)


# --- unit-тест: проверяет одну маленькую функцию ---
def test_hash_password_is_not_plain_text():
    assert hash_password("secret123") != "secret123"


# --- подкожный тест: весь сценарий регистрации под слоем UI ---
def test_register_saves_user_and_sends_welcome_email(service, repository, mailer):
    service.register("anna@example.com", "secret123")
    saved = repository.get("anna@example.com")
    assert saved is not None
    assert saved["password_hash"] != "secret123"
    assert mailer.sent == [("anna@example.com", "Добро пожаловать!")]


# --- подкожные тесты на остальные сценарии регистрации ---


def test_register_rejects_invalid_email(service, repository, mailer):
    with pytest.raises(ValueError, match="invalid email"):
        service.register("anna.example.com", "secret123")
    assert repository.count() == 0
    assert mailer.sent == []


def test_register_rejects_short_password(service, repository, mailer):
    with pytest.raises(ValueError, match="password too short"):
        service.register("anna@example.com", "secret")
    assert repository.count() == 0
    assert mailer.sent == []


def test_register_rejects_duplicate_email(service, repository, mailer):
    service.register("anna@example.com", "secret123")
    with pytest.raises(UserAlreadyExists):
        service.register("anna@example.com", "another123")
    assert repository.count() == 1
    assert mailer.sent == [("anna@example.com", "Добро пожаловать!")]

