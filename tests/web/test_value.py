#!/usr/bin/env python

try:
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

from circuits.web import Controller
from circuits import Event, Component

class Hello(Event):
    """Hello Event"""

class Test(Component):

    def hello(self):
        return "Hello World!"

class Root(Controller):

    def index(self):
        return self.push(Hello())

def test(webapp):
    Test().register(webapp)

    f = urlopen(webapp.server.base)
    s = f.read()
    assert s == b"Hello World!"
