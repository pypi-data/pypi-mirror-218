import typing as t
import subprocess
from pathlib import Path

from venture.config import UiConfig


def run_ui(config: UiConfig, input: t.Iterable[str]) -> str:
    proc = subprocess.run(
        config.exec,
        input=config.seperator.join(input).encode("utf-8"),
        check=False,
        shell=True,
        capture_output=True,
    )

    return proc.stdout.decode("utf-8").strip()


def run_exec(fmt: str, path: Path) -> subprocess.Popen:
    return subprocess.Popen(
        fmt.format(path=path),
        shell=True,
        start_new_session=True,
    )
