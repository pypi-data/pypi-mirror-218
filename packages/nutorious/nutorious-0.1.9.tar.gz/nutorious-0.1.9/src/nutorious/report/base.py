from __future__ import annotations

from typing import Callable

from attrs import define
from rich.console import Console
from rich.live import Live
from watchfiles import watch
from watchfiles.filters import DefaultFilter

from nutorious.config import load_config
from nutorious.context import Context
from nutorious.journal import load_journal


@define
class BaseOptions:
    journal_path: str
    watch: bool


class YmlFilesFilter(DefaultFilter):
    def __call__(self, change: "Change", path: str) -> bool:
        return path.endswith(".yml") and super().__call__(change, path)


def display_report(options: BaseOptions, build_report_table_fn: Callable[[Context], Table]):
    def build_table_or_error():
        try:
            context = __load_context(options)
            return build_report_table_fn(context)
        except ValueError as e:
            return f"[red]Error: {e}![/red]"

    if options.watch:
        with Live(build_table_or_error(), auto_refresh=False) as live:
            for changes in watch(options.journal_path, watch_filter=YmlFilesFilter()):
                live.update(build_table_or_error(), refresh=True)
    else:
        console = Console()
        console.print(build_table_or_error())


def __load_context(options: BaseOptions) -> Context:
    config = load_config(options.journal_path)
    journal = load_journal(config, options.journal_path)

    return Context(config, journal, options)
