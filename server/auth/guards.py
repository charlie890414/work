from __future__ import annotations

from functools import wraps
from typing import Callable, Any

from .token_service import TokenService


class AuthError(Exception):
    pass


def require_token(
    token_service: TokenService,
    *,
    required_scopes: tuple[str, ...] = (),
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(func)
        def wrapper(*args: Any, token: str, **kwargs: Any) -> Any:
            claims = token_service.verify_token(token)
            if required_scopes:
                token_scopes = set(claims.scopes)
                if not set(required_scopes).issubset(token_scopes):
                    raise AuthError(f"Missing required scopes: {required_scopes}")
            return func(*args, claims=claims, **kwargs)

        return wrapper

    return decorator
