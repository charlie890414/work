from __future__ import annotations

from dataclasses import dataclass

from fastmcp import FastMCP

from server.auth.guards import require_token
from server.auth.token_service import TokenService


@dataclass
class SkillGroup:
    """Group-based skill tools示意。"""

    app: FastMCP
    token_service: TokenService

    def register(self) -> None:
        @self.app.tool(name="skill.profile")
        @require_token(self.token_service, required_scopes=("profile:read",))
        def profile(*, claims, token: str) -> dict:
            return {
                "user": claims.sub,
                "permissions": list(claims.scopes),
                "group": "skill",
            }

        @self.app.tool(name="skill.health")
        def health() -> dict:
            return {"ok": True, "service": "skill-group"}


def register_group_tools(app: FastMCP, token_service: TokenService) -> None:
    SkillGroup(app=app, token_service=token_service).register()
