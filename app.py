#!/usr/bin/env python3
from sqlalchemy import create_engine, Column, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base
from bottle import route, run, template, jinja2_view, get, post, request, redirect, install, response, static_file
from bottle.ext import sqlalchemy
import bottle_session
import uuid
from redminelib import Redmine
from os.path import join
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

@post('/get_redmine_issue')
def import_story():
    redmine = Redmine('https://progress.opensuse.org', key=config['redmine']['api_key'])
    story_id = request.forms.get('import_story')
    print(story_id)
    return (redmine.issue.get(story_id).description)
    #import pdb; pdb.set_trace()

@route("/assets/<filetype>/<filename>")
def get_static_files(filetype, filename):
    return static_file(filename, root=join('assets/', filetype))

@route("/test")
@jinja2_view("test.tpl", template_lookup=template_lookup)
def foobar():
    return { "text" : "test-template" }

run(host=config['DEFAULT']['bind_address'], port=config['DEFAULT']['port'], debug=True)

