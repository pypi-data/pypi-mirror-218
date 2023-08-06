from cherre_types import get_env


def get_bool_environmental_variable(key: str) -> bool:
    res = get_env(key)

    if not res:
        return False

    if res.lower() == "true":
        return True

    if res.lower() == "false":
        return False

    raise ValueError(f"Value {res} is not a boolean!")
