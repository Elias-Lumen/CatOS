"""Make the CatOS service functions available from one place."""

from .auth import (
    login_user,
    register_user,
)


__all__ = [
    "login_user",
    "register_user",
]
