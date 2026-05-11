from __future__ import annotations

from fastmcp import FastMCP

from server.auth.token_service import TokenService
from server.tools.groups.skill_group import SkillGroup


def register_group_tools(app: FastMCP, token_service: TokenService) -> None:
    # 當 group 越來越多時，只需在此聚合 register，避免單一檔案過大。
    SkillGroup(app=app, token_service=token_service).register()
