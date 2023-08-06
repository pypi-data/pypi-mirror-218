from textual.app import ComposeResult
from textual.widgets import Static


class AppLogo(Static):
    def compose(self) -> ComposeResult:
        yield Static("Textualodon - Mastodon in your terminal", id="logo")
