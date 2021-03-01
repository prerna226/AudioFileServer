from flask import request
from flask_restful import Resource
from main.models.audio_models import db
from utility.sqlQueryBuilder import SqlQueryBuilder
from main.models.audio_models import Audio,PodcastParticipants,PodcastSeries,Users
from cerberus import Validator
from configConstants.messages import Messages

class AudioResource(Resource):

    def delete(self,audioType,audioFileId):
        try:
            schema = {
                "audioType": {'type': 'string', 'required': True, 'nullable': False,'allowed':['song','audiobook','podcast']},
                "audioFileId": {'type': 'integer', 'required': True, 'nullable': False}
            }
            instance = {
                "audioType": audioType,
                "audioFileId": int(audioFileId)
            }
            v = Validator()
            if not v.validate(instance, schema):
                return { 'error': v.errors }, 400
        except Exception as e:
            return { 'error': str(e) }, 400
        try:
            exists = Audio.query.filter_by(id=audioFileId,audio_type=audioType,is_deleted=0).first() is not None
            if exists:
                Audio.query.filter_by(id=audioFileId,audio_type=audioType).update(dict(is_deleted=1))
                db.session.commit()
                return {'message': Messages.AUDIO_DELETED }, 201
            else:
                return {'error': Messages.AUDIO_DOES_NOT_EXIST }, 404
        except Exception as e:
            return {'error': Messages.INTERNAL_SERVER_ERROR }, 500