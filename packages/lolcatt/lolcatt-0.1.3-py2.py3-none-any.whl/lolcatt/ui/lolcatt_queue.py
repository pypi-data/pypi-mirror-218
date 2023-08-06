#!/usr/bin/env python3

from textual import on
from textual.containers import Container
from textual.widgets import Static, Button, ListView
from lolcatt.ui.lolcatt_url_input import LolCattUrlInput


class LolCattQueue(Static):
    """LolCattQueue widget."""

    def __init__(self, *args, **kwargs):
        """Initialize."""
        super().__init__(*args, **kwargs)
        self._queue = ListView(id='queue_list')
        self._url_input = LolCattUrlInput()
        self._add_button = Button('Add', id='add_to_queue_btn')
        self._prepend_button = Button('Prepend', id='prepend_to_queue_btn')
        self._close_button = Button('X', id='close_queue_btn')

    def compose(self):
        yield self._queue
        yield self._url_input
        with Container(id='queue_buttons'):
            yield self._add_button
            yield self._prepend_button

    @on(Button.Pressed, '#add_to_queue_btn')
    def add_to_queue(self):
        """Add url to queue."""
        self._queue.append(self._url_input.value)
        self._url_input.value = ''

    @on(Button.Pressed, '#prepend_to_queue_btn')
    def prepend_to_queue(self):
        """Prepend url to queue."""
        self._queue.insert(0, self._url_input.value)
        self._url_input.value = ''

    @on(Button.Pressed, '#close_queue_btn')
    def _close_queue(self):
        """Close queue."""
        self.app.pop_screen('queue')


