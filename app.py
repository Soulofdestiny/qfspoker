#!/usr/bin/env python3
from sqlalchemy import create_engine, Column, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base
from bottle import route, run, template, jinja2_view, get, post, request, redirect, install, response
from bottle.ext import sqlalchemy
import bottle_session
import uuid
import configparser

template_lookup=["assets"]
config = configparser.ConfigParser()
config.read('config.ini')
Base = declarative_base()
engine = create_engine('sqlite:///:memory:', echo=True)

plugin = sqlalchemy.Plugin(
    engine,
    Base.metadata,
    keyword='db',
    create= True,
    commit=True,
    use_kwargs=False,
)

install(plugin)

class DBSession(Base):
    __tablename__ = 'poker_sessions'
    id = Column(Integer, Sequence('id_seq'), primary_key=True)
    name = Column(String(100))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "<DBSession('{}', '{}')>".format(self.id, self.name)

@get('/')
@jinja2_view("main.tpl", template_lookup=template_lookup)
def index():
    template_data = {}
    username = request.get_cookie('username')
    if username:
        print("recover username from cookie: {}".format(username))
        template_data.update({"username":username})
    else:
        template_data = {}

    return template_data

@post('/create_session')
def create_session(db):
    username = request.forms.get('user_name')
    response.set_cookie('username', str(username))
    session_name = request.forms.get('session_name')
    dbsession = DBSession(session_name)
    db.add(dbsession)
    db.flush()
    session_id = dbsession.id
    redirect('/sessions/{}'.format(session_id))

@get('/sessions/<session_id>')
@jinja2_view("session.tpl", template_lookup=template_lookup)
def show_session(session_id, db):
    username = request.get_cookie('username')
    session = db.query(DBSession).filter_by(id=session_id).first()
    data = {
        'name' : username,
        'session' : session.name,
        'user_story' : '',
        'users' : ['foo', 'bar'],
    }
    return data

@route("/test")
@jinja2_view("test.tpl", template_lookup=template_lookup)
def foobar():
    return { "text" : "test-template" }

run(host=config['DEFAULT']['bind_address'], port=config['DEFAULT']['port'], debug=True)

