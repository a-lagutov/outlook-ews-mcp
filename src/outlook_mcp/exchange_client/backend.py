from __future__ import annotations

import truststore

from ..config import Settings
from .base import BaseEWSBackend
from .calendar import CalendarOperationsMixin
from .contacts import ContactOperationsMixin
from .email import EmailOperationsMixin
from .mailbox import MailboxSettingsMixin
from .protocol import ExchangeBackend


class EWSExchangeBackend(
    EmailOperationsMixin,
    MailboxSettingsMixin,
    CalendarOperationsMixin,
    ContactOperationsMixin,
    BaseEWSBackend,
):
    """Live EWS-backed implementation of ExchangeBackend, assembled from domain mixins."""


def build_default_backend(settings: Settings) -> ExchangeBackend:
    """Build the live EWS backend.

    By default TLS is verified against the OS trust store, so certificates the
    system already trusts work without extra setup; certifi alone misses CAs that
    are installed only locally. EXCHANGE_CA_BUNDLE overrides this with an explicit
    PEM file, and EXCHANGE_VERIFY_SSL=false turns verification off.
    """
    if settings.exchange_verify_ssl and settings.exchange_ca_bundle is None:
        truststore.inject_into_ssl()
    return EWSExchangeBackend(settings)
