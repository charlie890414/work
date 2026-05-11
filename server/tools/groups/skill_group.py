from __future__ import annotations

from server.auth.guards import require_token
from server.tools.groups.base import BaseToolGroup


class SkillGroup(BaseToolGroup):
    """Skill domain tools."""

    def register(self) -> None:
        self._register_profile()
        self._register_health()

    def _register_profile(self) -> None:
        @self.app.tool(name="skill.profile")
        @require_token(self.token_service, required_scopes=("profile:read",))
        def profile(*, claims, token: str) -> dict:
            return {
                "user": claims.sub,
                "permissions": list(claims.scopes),
                "group": "skill",
            }

    def _register_health(self) -> None:
        @self.app.tool(name="skill.health")
        def health() -> dict:
            return {"ok": True, "service": "skill-group"}
