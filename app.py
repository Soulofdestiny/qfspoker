#!/usr/bin/python3
from bottle import route, run, template, jinja2_view
@route('/')
def index():
    return '<b>Nothing to see here</b>!'

@route("/test")
@jinja2_view("test.tpl", template_lookup=["assets"])
def foobar():
    return { "text" : "test-template" }

run(host='0.0.0.0', port=8080)
