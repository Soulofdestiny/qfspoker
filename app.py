#!/usr/bin/python3
from bottle import route, run, template, jinja2_view, get, post, request, redirect
import bottle_session
import uuid
import configparser

template_lookup=["assets"]
config = configparser.ConfigParser()
config.read('config.ini')

@get('/')
@jinja2_view("main.tpl", template_lookup=template_lookup)
def index():
    return {}

@post('/create_session')
def create_session():
    # TODO: give user a session cookie
    session_name = request.forms.get('session_name')
    session_uuid = str(uuid.uuid4()).split('-')[0]
    print(session_uuid)
    # TODO: persist session (uuid as key)
    redirect('/sessions/{}'.format(session_uuid))

@get('/sessions/<uuid>')
@jinja2_view("session.tpl", template_lookup=template_lookup)
def show_session(uuid):
    # TODO: render planning poker template
    data = {
        'name' : '', #TODO: fill me
        'session' : uuid,
        'user_story' : '',
        'users' : ['foo', 'bar'],
    }
    return data

@route("/test")
@jinja2_view("test.tpl", template_lookup=template_lookup)
def foobar():
    return { "text" : "test-template" }

run(host=config['DEFAULT']['bind_address'], port=config['DEFAULT']['port'], debug=True)

