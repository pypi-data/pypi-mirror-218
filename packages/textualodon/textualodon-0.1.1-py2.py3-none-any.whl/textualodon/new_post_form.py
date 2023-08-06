from textual import on  # type: ignore[attr-defined]
from textual.app import ComposeResult
from textual.containers import Container, Horizontal, ScrollableContainer
from textual.screen import Screen
from textual.widgets import (
    Button,
    Checkbox,
    Footer,
    Header,
    Input,
    Label,
    Select,
    Static,
)

try:
    from api import MastoAPI
    from constants import poll_expiration_time, post_languages
    from post_details import PostDetails
except ImportError:
    from .api import MastoAPI
    from .constants import poll_expiration_time, post_languages
    from .post_details import PostDetails


class NewPostForm(Screen):
    BINDINGS = [
        ("b", "go_back", "Go back"),
    ]

    def __init__(self) -> None:
        self.masto_api = MastoAPI()
        super().__init__()

    def compose(self) -> ComposeResult:
        yield ScrollableContainer(
            Header(),
            Static("Add new post", id="title"),
            Input(id="post_content"),
            Static("Text can't be blank!", id="post_content_empty"),
            Static(
                '[i]Hint: to add a new line, use "\\n"[/]',
                id="hint",
            ),
            Horizontal(
                Label("Visibility", classes="horizontal_label"),
                Select(
                    options=[
                        [val, val]
                        for val in ["public", "unlisted", "private", "direct"]
                    ],
                    allow_blank=False,
                    value="public",
                    id="visibility",
                ),
                Checkbox("CW", id="cw_checkbox"),
                Checkbox("Poll", id="poll_checkbox"),
                Label("Language", classes="horizontal_label"),
                Select(
                    options=[[key, val] for key, val in post_languages.items()],
                    allow_blank=False,
                    value="en",
                    id="post_language",
                ),
            ),
            Container(
                Label("Content Warning", classes="label"),
                Input(id="cw_content"),
                id="cw_container",
            ),
            Container(
                Horizontal(
                    Checkbox("Allow multiple choices", id="multiple_choice"),
                    Checkbox("Hide total votes", id="hide_total"),
                ),
                Horizontal(
                    Label("Choice 1", classes="horizontal_label"),
                    Input(id="choice_1"),
                ),
                Horizontal(
                    Label("Choice 2", classes="horizontal_label"),
                    Input(id="choice_2"),
                ),
                Horizontal(
                    Label("Choice 3", classes="horizontal_label"),
                    Input(id="choice_3"),
                ),
                Horizontal(
                    Label("Choice 4", classes="horizontal_label"),
                    Input(id="choice_4"),
                ),
                Static(
                    "Polls have to have at least two options",
                    id="poll_not_enough_options",
                ),
                Horizontal(
                    Label("Expiration date", classes="horizontal_label"),
                    Select(
                        options=[
                            [key, val] for key, val in poll_expiration_time.items()
                        ],
                        allow_blank=False,
                        value=300,
                        id="poll_expiration",
                    ),
                ),
                id="poll_container",
            ),
            Button("Submit", id="submit"),
            Footer(),
        )

    def action_go_back(self) -> None:
        self.app.pop_screen()

    @on(Button.Pressed, "#submit")
    def submit(self) -> None:
        post_content = self.query_one("#post_content").value
        if not post_content:
            self.query_one("#post_content_empty").styles.display = "block"
            return
        else:
            self.query_one("#post_content_empty").styles.display = "none"
        visibility = self.query_one("#visibility").value
        multiple_choice = self.query_one("#multiple_choice").value
        hide_total = self.query_one("#hide_total").value
        content_warning = None
        poll_options = None
        sensitive = False
        poll_expiration = 300
        if self.query_one("#cw_checkbox").value:
            sensitive = True
            content_warning = self.query_one("#cw_content").value
        if self.query_one("#poll_checkbox").value:
            poll_expiration = self.query_one("#poll_expiration").value
            poll_options = [
                self.query_one("#choice_1").value,
                self.query_one("#choice_2").value,
                self.query_one("#choice_3").value,
                self.query_one("#choice_4").value,
            ]
            for i in range(len(poll_options) - 1, 0, -1):
                if not poll_options[i]:
                    del poll_options[i]
            if len(poll_options) < 2:
                self.query_one("#poll_not_enough_options").styles.display = "block"
                return
            else:
                self.query_one("#poll_not_enough_options").styles.display = "none"
        status_code, result = self.masto_api.add_post(
            post_content=post_content,
            sensitive=sensitive,
            visibility=visibility,
            content_warning=content_warning,
            poll_options=poll_options,
            multiple_choice=multiple_choice,
            hide_total=hide_total,
            poll_expiration=poll_expiration,
        )
        if status_code == 200:
            self.app.push_screen(PostDetails(post_id=result["id"]))

    @on(Checkbox.Changed, "#cw_checkbox")
    def change_cw(self) -> None:
        if self.query_one("#cw_checkbox").value:
            self.query_one("#cw_container").styles.display = "block"
        else:
            self.query_one("#cw_container").styles.display = "none"

    @on(Checkbox.Changed, "#poll_checkbox")
    def change_poll(self) -> None:
        if self.query_one("#poll_checkbox").value:
            self.query_one("#poll_container").styles.display = "block"
        else:
            self.query_one("#poll_container").styles.display = "none"
