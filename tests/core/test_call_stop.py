#!/usr/bin/env python
from __future__ import print_function

import pytest

from circuits import handler, Component, Event


class test(Event):
    """test Event"""

    success = True


class foo(Event):
    """foo Event"""


class App(Component):

    @handler("test", priority=1)
    def on_test(self, event):
        event.stop()
        yield

    @handler("test")
    def on_test_ignored(self):
        return "Hello World!"


@pytest.fixture
def app(request, manager, watcher):
    app = App().register(manager)
    assert watcher.wait("registered")

    def finalizer():
        app.unregister()

    request.addfinalizer(finalizer)

    return app


def test_call_stop(manager, watcher, app):
    x = manager.fire(test())
    assert watcher.wait("test_success")

    assert x.value is None
