from __future__ import annotations

import typing as t
from fnmatch import fnmatch
import glob
from typing import TypedDict
from pathlib import Path
import functools

from arc.color import fg, colorize
from venture import pango

from venture.config import BrowseConfig, Config, ProfileConfig, UiConfig
from .icons import default, filetype_icon, Icon

GLOB = "/*"


class BrowseOption(TypedDict):
    name: str
    path: Path
    icon: Icon


class PathError(Exception):
    ...


class BrowseList:
    name_lookup: set[str]

    def __init__(self, config: BrowseConfig):
        self.config = config

    def discover(self, profile: ProfileConfig) -> t.Generator[BrowseOption, None, None]:
        self.name_lookup = set()

        for path in profile.paths:
            path = path.expanduser().resolve()
            for realized_path_str in glob.glob(str(path)):
                realized_path = Path(realized_path_str)
                parts = self.get_globbed_count(path, realized_path)
                entry = self.create_entry(profile, realized_path, parts)
                if entry:
                    yield entry

    def create_entry(
        self,
        profile: ProfileConfig,
        path: Path,
        parts: int,
    ) -> BrowseOption | None:
        if (
            (path.name.startswith(".") and not profile.show.hidden)
            or (path.is_file() and not profile.show.files)
            or (path.is_dir() and not profile.show.directories)
            or self.should_exclude_path(profile, path)
        ):
            return None

        name = self.get_unique_name(path, parts)
        icon = self.get_icon(path.suffix if path.is_file() else "directory")

        self.name_lookup.add(name)

        return {
            "name": name,
            "path": path,
            "icon": icon,
        }

    def get_globbed_count(self, globbed_path: Path, path: Path) -> int:
        """Given a path that contains some globs, and
        a real path resulting from that glob, returns
        the number of path parts that were filled in by that glob
        """
        unglobbed = globbed_path
        curr = path
        prefix = 0

        while curr != unglobbed:
            prefix += 1
            curr = curr.parent
            unglobbed = unglobbed.parent

        return prefix

    def get_unique_name(self, path: Path, required_parts: int):
        name = self.get_name(path, required_parts)

        while name in self.name_lookup:
            required_parts += 1
            if required_parts > len(path.parts):
                raise PathError(
                    "Reached the root without creating a"
                    f" unique name for path {colorize(str(path), fg.YELLOW)}"
                )

            name = self.get_name(path, required_parts)

        return name

    def get_name(self, path: Path, parts: int) -> str:
        if parts == 0:
            return path.name
        return Path(*path.parts[len(path.parts) - parts :]).as_posix()

    def should_exclude_path(self, profile: ProfileConfig, path: Path):
        name = str(path)
        return any(fnmatch(name, pattern) for pattern in profile.exclude)

    @staticmethod
    @functools.lru_cache()
    def get_icon(filetype: str) -> Icon:
        """Returns the icon associated with a specific file type"""
        return filetype_icon(filetype.lstrip(".")) or default


def format_option(fmt: str, option: BrowseOption, ui: UiConfig) -> str:
    format_args = {
        "name": option["name"],
        "path": str(option["path"]),
        "icon": pango.span(option["icon"].code, color=option["icon"].color)
        if ui.supports.pango
        else option["icon"].code,
    }

    return fmt.format(**format_args)
