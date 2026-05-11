from __future__ import annotations

from fastmcp import FastMCP

from server.config import settings
from server.auth.token_service import TokenService
from server.tools.function_tools import register_function_tools
from server.tools.group_tools import register_group_tools


def create_app() -> FastMCP:
    app = FastMCP(name=settings.app_name)
    token_service = TokenService(
        secret_key=settings.secret_key,
        issuer=settings.issuer,
        audience=settings.audience,
        algorithm=settings.algorithm,
    )

    register_function_tools(app, token_service)
    register_group_tools(app, token_service)
    return app


app = create_app()


if __name__ == "__main__":
    app.run()
