from __future__ import annotations

from fastmcp import FastMCP

from server.auth.guards import require_token
from server.auth.token_service import TokenService
from server.config import settings


def register_function_tools(app: FastMCP, token_service: TokenService) -> None:
    @app.tool(name="auth.generate_token")
    def generate_token(subject: str, scopes: list[str] | None = None, ttl_seconds: int | None = None) -> dict:
        token = token_service.create_token(
            subject=subject,
            scopes=scopes or ["read"],
            ttl_seconds=ttl_seconds or settings.default_ttl_seconds,
        )
        return {"token": token}

    @app.tool(name="auth.verify_token")
    def verify_token(token: str) -> dict:
        claims = token_service.verify_token(token)
        return {
            "sub": claims.sub,
            "scopes": list(claims.scopes),
            "iat": claims.iat,
            "exp": claims.exp,
            "iss": claims.iss,
            "aud": claims.aud,
        }

    @app.tool(name="protected.echo")
    @require_token(token_service, required_scopes=("read",))
    def protected_echo(message: str, *, claims, token: str) -> dict:
        return {"message": message, "by": claims.sub, "scopes": list(claims.scopes)}
