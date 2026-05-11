from __future__ import annotations

import argparse

from server.auth.token_service import TokenService
from server.config import settings


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate/verify JWT token for MCP tools")
    sub = parser.add_subparsers(dest="command", required=True)

    gen = sub.add_parser("generate", help="Generate a JWT token")
    gen.add_argument("--subject", default="dev-user", help="Token subject (default: dev-user)")
    gen.add_argument(
        "--scopes",
        default="read",
        help="Comma-separated scopes, e.g. read,profile:read (default: read)",
    )
    gen.add_argument(
        "--ttl-seconds",
        type=int,
        default=settings.default_ttl_seconds,
        help=f"Token TTL in seconds (default: {settings.default_ttl_seconds})",
    )

    verify = sub.add_parser("verify", help="Verify a JWT token")
    verify.add_argument("--token", required=True, help="JWT token string")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    service = TokenService(
        secret_key=settings.secret_key,
        issuer=settings.issuer,
        audience=settings.audience,
        algorithm=settings.algorithm,
    )

    if args.command == "generate":
        scopes = [s.strip() for s in args.scopes.split(",") if s.strip()]
        token = service.create_token(
            subject=args.subject,
            scopes=scopes or ["read"],
            ttl_seconds=args.ttl_seconds,
        )
        print(token)
        return

    if args.command == "verify":
        claims = service.verify_token(args.token)
        print({
            "sub": claims.sub,
            "scopes": list(claims.scopes),
            "iat": claims.iat,
            "exp": claims.exp,
            "iss": claims.iss,
            "aud": claims.aud,
        })
        return


if __name__ == "__main__":
    main()
