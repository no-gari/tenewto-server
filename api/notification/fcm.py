"""Firebase Cloud Messaging helper module."""

from __future__ import annotations

import os
from typing import Optional, Dict

import firebase_admin
from firebase_admin import credentials, messaging
from django.conf import settings


_default_app: Optional[firebase_admin.App] = None


def _initialize() -> firebase_admin.App:
    """Initialise firebase application once."""
    global _default_app
    if _default_app is not None:
        return _default_app

    cred_path = getattr(settings, "FIREBASE_CREDENTIALS", None) or os.environ.get(
        "FIREBASE_CREDENTIALS"
    )
    if cred_path and os.path.exists(cred_path):
        cred = credentials.Certificate(cred_path)
        _default_app = firebase_admin.initialize_app(cred)
    else:
        _default_app = firebase_admin.initialize_app()
    return _default_app


def send_push(token: str, title: str, body: str, data: Optional[Dict[str, str]] = None) -> None:
    """Send a push notification to a single device token."""

    if not token:
        return

    _initialize()

    message = messaging.Message(
        token=token,
        notification=messaging.Notification(title=title, body=body),
        data=data or {},
    )

    try:
        messaging.send(message)
    except Exception:
        # Fail silently; push failures shouldn't break main flow
        pass

