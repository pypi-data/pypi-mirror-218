from __future__ import annotations
import os
from pathlib import Path

from pydantic import BaseModel, ValidationError, validator
import toml
import arc


class UISupportsConfig(BaseModel):
    pango: bool = False


class UiConfig(BaseModel):
    exec: str
    seperator: str = "\n"
    format: str = "{name}"
    response_format: str | None = None
    supports: UISupportsConfig = UISupportsConfig()


class CacheConfig(BaseModel):
    enabled: bool = True


class ProfileShowConfig(BaseModel):
    hidden: bool = False
    files: bool = True
    directories: bool = True
    quicklaunch: bool = True


class ProfileConfig(BaseModel):
    paths: list[Path]
    exec: str
    exclude: list[str] = []
    show: ProfileShowConfig = ProfileShowConfig()
    ui: UiConfig | None = None


class BrowseConfig(BaseModel):
    ui: UiConfig | None = None
    profiles: dict[str, ProfileConfig] = {}

    @validator("profiles")
    def check_ui_existance(cls, value: dict[str, ProfileConfig], values):
        if values["ui"]:
            return value

        if not all(p.ui for p in value.values()):
            raise ValueError(
                "No UI configuration found. "
                "Please define a default configuration "
                "or add a configuration for every profile"
            )

        return value


class QuickLaunchEntryConfig(BaseModel):
    name: str
    path: str = ""
    exec: str | None = None
    format: str | None = None
    icon: str = ""
    details: str = ""


class QuickLaunchConfig(BaseModel):
    exec: str | None = None
    entries: list[QuickLaunchEntryConfig]
    ui: UiConfig

    @validator("entries")
    def check_exec_existance(cls, value: list[QuickLaunchEntryConfig], values):

        if values["exec"]:
            return value

        if not all(e.exec for e in value):
            raise ValueError(
                "Missing exec command. Please define "
                "a default quicklaunch exec command or "
                "one for reach entry"
            )

        return value


class Config(BaseModel):
    cache: CacheConfig = CacheConfig()
    browse: BrowseConfig = BrowseConfig()
    quicklaunch: QuickLaunchConfig | None = None

    @classmethod
    def load(cls, filepath: os.PathLike):
        if not os.path.exists(filepath):
            raise arc.errors.ExecutionError(f"Config file not found: {filepath}")

        try:
            return cls(**toml.load(filepath))
        except ValidationError as e:
            raise arc.errors.ExecutionError(
                f"Config file is incorrectly formed:\n{str(e)}"
            ) from e
