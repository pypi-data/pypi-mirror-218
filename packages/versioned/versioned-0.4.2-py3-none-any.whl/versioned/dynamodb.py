# -*- coding: utf-8 -*-

"""
Tje dynamodb backend to store metadata of artifacts, versions and aliases.
"""

import typing as T
from datetime import datetime, timezone

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from pynamodb.attributes import NumberAttribute
from pynamodb.attributes import BooleanAttribute
from pynamodb.attributes import UTCDateTimeAttribute

from .constants import LATEST_VERSION, VERSION_ZFILL


def get_utc_now() -> datetime:
    return datetime.utcnow().replace(tzinfo=timezone.utc)


def encode_version(version: T.Union[int, str]) -> str:
    return str(version).zfill(VERSION_ZFILL)

def encode_alias_key(name: str) -> str:
    return f"__{name}-alias"


class Base(Model):
    pk: T.Union[str, UnicodeAttribute] = UnicodeAttribute(hash_key=True)
    sk: T.Union[str, UnicodeAttribute] = UnicodeAttribute(
        range_key=True,
        default=LATEST_VERSION,
    )


class Artifact(Base):
    """
    Todo: docstring
    """
    update_at: T.Union[datetime, UTCDateTimeAttribute] = UTCDateTimeAttribute(
        default=get_utc_now,
    )
    is_deleted: T.Union[bool, BooleanAttribute] = BooleanAttribute(
        default=False,
    )
    sha256: T.Union[str, UnicodeAttribute] = UnicodeAttribute()

    @classmethod
    def new(
        cls,
        name: str,
        version: T.Optional[T.Union[int, str]] = None,
    ) -> "Artifact":
        if version is None:
            return cls(pk=name)
        else:
            return cls(pk=name, sk=encode_version(version))

    @property
    def name(self) -> str:
        return self.pk

    @property
    def version(self) -> str:
        return self.sk.lstrip("0")

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "version": self.version,
            "update_at": self.update_at,
            "sha256": self.sha256,
        }


class Alias(Base):
    """
    Todo: docstring
    """
    version: T.Union[str, UnicodeAttribute] = UnicodeAttribute()
    secondary_version: T.Optional[T.Union[str, UnicodeAttribute]] = UnicodeAttribute(
        null=True,
    )
    secondary_version_weight: T.Optional[
        T.Union[int, NumberAttribute]
    ] = NumberAttribute(
        null=True,
    )

    @classmethod
    def new(
        cls,
        name: str,
        alias: str,
        version: T.Optional[T.Union[int, str]] = None,
        secondary_version: T.Optional[T.Union[int, str]] = None,
        secondary_version_weight: T.Optional[int] = None,
    ):
        if version is None:
            version = LATEST_VERSION
        version = encode_version(version)
        if secondary_version is not None:
            secondary_version = encode_version(secondary_version)
            if version == secondary_version:
                raise ValueError

        return cls(
            pk=encode_alias_key(name),
            sk=alias,
            version=version,
            secondary_version=secondary_version,
            secondary_version_weight=secondary_version_weight,
        )

    @property
    def name(self) -> str:
        return "-".join(self.pk.split("-")[:-1])[2:]

    @property
    def alias(self) -> str:
        return self.sk

    def to_dict(self) -> dict:
        if self.secondary_version is None:
            secondary_version = None
        else:
            secondary_version = self.secondary_version.lstrip("0")
        return {
            "name": self.name,
            "alias": self.alias,
            "version": self.version.lstrip("0"),
            "secondary_version": secondary_version,
            "secondary_version_weight": self.secondary_version_weight,
        }
