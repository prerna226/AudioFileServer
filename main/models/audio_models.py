from flask import Flask
from marshmallow import Schema, fields, pre_load, validate
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import datetime
import enum

ma = Marshmallow()
db = SQLAlchemy()

class AudioType(enum.Enum):
    SONG = "song"
    PODCAST = "podcast"
    AUDIOBOOK = "audiobook"


class Audio(db.Model):
    """ Audio Model for storing audio related details """
    __tablename__ = "audio"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), unique=True, nullable=False)
    duration = db.Column(db.Time, nullable=False)
    host = db.Column(db.String(100), nullable=True)
    narrator = db.Column(db.String(255), nullable=True)
    author = db.Column(db.String(255),nullable=True)
    uploaded_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    is_deleted = db.Column(db.Boolean, default=False)
    audio_type = db.Column(db.Enum(AudioType),default=AudioType.SONG,nullable=False)
        
    def __repr__(self):
        return "<Audio '{}'>".format(self.title)

class Users(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    
    
    def __repr__(self):
        return "<User '{}'>".format(self.username)

class PodcastSeries(db.Model):
    """ Podcast Series Model for storing podcast series related details """
    __tablename__ = "podcast_series"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    audio_id = db.Column(db.Integer,db.ForeignKey(Audio.__table__.c.id))
    name = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Time, nullable=False)
    is_deleted = db.Column(db.Boolean,default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    
    def __repr__(self):
        return "<Podcast series '{}'>".format(self.title)

class PodcastParticipants(db.Model):
    """ Podcast Participants Model for storing podcast series related details """
    __tablename__ = "podcast_participants"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    audio_id = db.Column(db.Integer,db.ForeignKey(Audio.__table__.c.id))
    user_id = db.Column(db.Integer,db.ForeignKey(Users.__table__.c.id))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)
    
    def __repr__(self):
        return "<Podcast Participants '{}'>".format(self.id)

