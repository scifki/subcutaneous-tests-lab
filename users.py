import hashlib


class UserAlreadyExists(Exception):
    """Пользователь с таким email уже зарегистрирован."""


def hash_password(password):
    """Возвращает SHA-256 хеш пароля."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


class InMemoryUserRepository:
    """Хранилище пользователей в памяти (вместо базы данных)."""

    def __init__(self):
        self._users = {}

    def add(self, user):
        self._users[user["email"]] = user

    def get(self, email):
        return self._users.get(email)

    def count(self):
        return len(self._users)


class UserService:
    """Сервисный слой: сценарий «зарегистрировать пользователя»."""

    def __init__(self, repository, mailer):
        self.repository = repository
        self.mailer = mailer

    def register(self, email, password):
        if "@" not in email:
            raise ValueError("invalid email")
        if len(password) < 8:
            raise ValueError("password too short")
        if self.repository.get(email) is not None:
            raise UserAlreadyExists(email)
        user = {"email": email, "password_hash": hash_password(password)}
        self.repository.add(user)
        self.mailer.send(email, "Добро пожаловать!")
        return user
