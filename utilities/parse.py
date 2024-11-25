__all__ = ["get_lines"]


def get_lines(raw: str) -> list[str]:
    return raw.strip().split("\n")
