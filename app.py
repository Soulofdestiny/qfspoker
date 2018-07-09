#!/usr/bin/python3
from bottle import route, run, template
@route('/')
def index():
    return '<b>Nothing to see here</b>!'

run(host='localhost', port=8080)
