from __future__ import annotations

from dataclasses import dataclass

from fastmcp import FastMCP

from server.auth.token_service import TokenService


@dataclass
class BaseToolGroup:
    app: FastMCP
    token_service: TokenService

    def register(self) -> None:
        raise NotImplementedError
