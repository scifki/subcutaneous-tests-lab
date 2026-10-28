from users import UserAlreadyExists


def register_endpoint(service, payload):
    """Тонкий слой над сервисом: запрос → вызов, результат → ответ.

    Возвращает пару (HTTP-код, тело ответа).
    """
    try:
        user = service.register(payload.get("email", ""), payload.get("password", ""))
    except UserAlreadyExists:
        return 409, {"error": "user already exists"}
    except ValueError as error:
        return 400, {"error": str(error)}
    return 201, {"email": user["email"]}
