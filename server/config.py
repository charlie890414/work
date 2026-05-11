from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("MCP_APP_NAME", "skill-mcp-server")
    secret_key: str = os.getenv("MCP_SECRET_KEY", "change-me-in-production")
    issuer: str = os.getenv("MCP_TOKEN_ISSUER", "skill-auth")
    audience: str = os.getenv("MCP_TOKEN_AUDIENCE", "skill-clients")
    algorithm: str = os.getenv("MCP_TOKEN_ALGORITHM", "HS256")
    default_ttl_seconds: int = int(os.getenv("MCP_TOKEN_DEFAULT_TTL", "3600"))


settings = Settings()
