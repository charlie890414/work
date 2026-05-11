from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Iterable

import jwt


@dataclass(frozen=True)
class TokenClaims:
    sub: str
    scopes: tuple[str, ...]
    exp: int
    iat: int
    iss: str
    aud: str


class TokenService:
    def __init__(self, *, secret_key: str, issuer: str, audience: str, algorithm: str = "HS256") -> None:
        self.secret_key = secret_key
        self.issuer = issuer
        self.audience = audience
        self.algorithm = algorithm

    def create_token(self, *, subject: str, scopes: Iterable[str], ttl_seconds: int) -> str:
        now = datetime.now(timezone.utc)
        exp = now + timedelta(seconds=ttl_seconds)
        payload = {
            "sub": subject,
            "scope": list(scopes),
            "iat": int(now.timestamp()),
            "exp": int(exp.timestamp()),
            "iss": self.issuer,
            "aud": self.audience,
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> TokenClaims:
        decoded = jwt.decode(
            token,
            self.secret_key,
            algorithms=[self.algorithm],
            issuer=self.issuer,
            audience=self.audience,
        )
        return TokenClaims(
            sub=str(decoded.get("sub", "")),
            scopes=tuple(decoded.get("scope", [])),
            exp=int(decoded.get("exp", 0)),
            iat=int(decoded.get("iat", 0)),
            iss=str(decoded.get("iss", "")),
            aud=str(decoded.get("aud", "")),
        )
