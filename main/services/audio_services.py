import json
import flask
from flask import request
from cerberus import Validator
from flask_restful import Resource
from main.models.audio_models import db
from config_constants.messages import Messages
from utility.sql_query_builder import SqlQueryBuilder
from main.models.audio_models import Audio,PodcastParticipants,PodcastSeries,Users

class AddAudio(Resource):

    # add audio
    def post(self):
        request_data = request.get_json()
        try:
            # validate schema
            schema = {
                "audioType": {'type': 'string','required': True,'allowed':['song','audiobook','podcast']},
                "audioFileMetadata": {'type': 'dict', 'schema': {
                            "title": {'type': 'string', 'required': True},
                            "duration": {'type': 'string', 'required': True},
                            "host": {'type': 'string', 'required': False},
                            "narrator": {'type': 'string', 'required': False},
                            "author": {'type': 'string', 'required': False},
                "participants": {
                    'type': 'list','maxlength':10,
                    'schema': {'type': 'dict', 'schema': {
                            "name": {'type': 'string', 'required': False},
                            "email": {'type': 'string', 'required': False}}}},
                "podcastSeries": {
                    'type': 'list',
                    'schema': {'type': 'dict', 'schema': {
                            "name": {'type': 'string', 'required': False},
                            "duration": {'type': 'string', 'required': False}}}}
            }}}
            v = Validator()
            if not v.validate(request_data, schema):
                return { 'error': v.errors }, 400
        except Exception as e:
            return { 'error': str(e) }, 400
        try:
            audioType = request_data['audioType']
            title = request_data['audioFileMetadata']['title']
            duration = request_data['audioFileMetadata']['duration']
            host = request_data['audioFileMetadata']['host']
            narrator = request_data['audioFileMetadata']['narrator']
            author = request_data['audioFileMetadata']['author']
            participants = request_data['audioFileMetadata']['participants']
            podcastSeries = request_data['audioFileMetadata']['podcastSeries']

            # add song
            if audioType == 'song':
                
                # if song not exist
                exists = Audio.query.filter_by(title=title,duration=duration,audio_type=audioType).first()
                if not exists:
                    audio= Audio(title=title,duration=duration,audio_type=audioType)
                    db.session.add(audio)
                    db.session.commit()
                    return {'message': Messages.DATA_ADDED }, 201
                else:
                    return {'message': Messages.SONG_ALREADY_EXIST }, 409
            
            # add audiobook
            elif audioType == 'audiobook':
                
                # if audiobook not exist
                exists = Audio.query.filter_by(title=title,duration=duration,narrator=narrator,author=author,audio_type=audioType).first()
                if not exists:
                    audio= Audio(title=title,duration=duration,narrator=narrator,author=author,audio_type=audioType)
                    db.session.add(audio)
                    db.session.commit()
                    return {'message': Messages.DATA_ADDED }, 201
                else:
                    return {'message': Messages.AUDIOBOOK_ALREADY_EXIST }, 409
            
            # add podcast
            else:
                exists = Audio.query.filter_by(title=title,duration=duration,host=host,audio_type=audioType).first()
                if not exists:
                    audio = Audio(title=title,duration=duration,host=host,audio_type=audioType)
                    db.session.add(audio)
                    db.session.commit()
                    audioId = audio.id
                else:
                    return {'message': Messages.PODCAST_ALREADY_EXIST }, 409
                
                # add podcast episodes
                if len(podcastSeries) > 0:
                    for s in podcastSeries:

                        # if podcast not exist
                        exists = PodcastSeries.query.filter_by(duration=s['duration'],name=s['name']).first()
                        if not exists:
                            ser= PodcastSeries(audio_id=audioId,duration=s['duration'],name=s['name'])
                            db.session.add(ser)
                        else:
                            return {'message': Messages.EACH_PODCAST_SERIES_MUST_BE_UNIQUE }, 409
                
                # add participants
                if len(participants)> 0:
                    for p in participants:
                        # if user email is unique
                        exists = Users.query.filter_by(email=p['email']).first()
                        if not exists:
                            users = Users(name=p['name'],email=p['email'])
                            db.session.add(users)
                            db.session.commit()
                        else:
                            return {'message': Messages.EMAIL_ALREADY_EXIST }, 409
                        userId = users.id
                        par = PodcastParticipants(audio_id=audioId,user_id=userId)
                        db.session.add(par)
                        
                db.session.commit()
                return {'message': Messages.DATA_ADDED }, 201
        except Exception as e:
            print(str(e))
            db.session.rollback()
            return {'error':Messages.INTERNAL_SERVER_ERROR }, 500

class UpdateAudio(Resource):    
    # update audio
    def put(self,audioType,audioFileId):
        request_data = request.get_json()
        try:
            # validate schema
            schema = {
                "audioFileMetadata": {'type': 'dict', 'schema': {
                            "title": {'type': 'string', 'required': True},
                            "duration": {'type': 'string', 'required': True},
                            "host": {'type': 'string', 'required': False},
                            "narrator": {'type': 'string', 'required': False},
                            "author": {'type': 'string', 'required': False},
                "participants": {
                    'type': 'list','maxlength':10,
                    'schema': {'type': 'dict', 'schema': {
                            "name": {'type': 'string', 'required': False},
                            "email": {'type': 'string', 'required': False}}}},
                "podcastSeries": {
                    'type': 'list',
                    'schema': {'type': 'dict', 'schema': {
                            "name": {'type': 'string', 'required': False},
                            "duration": {'type': 'string', 'required': False}}}}
            }}}
            v = Validator()
            if not v.validate(request_data, schema):
                return { 'error': v.errors }, 400
        except Exception as e:
            return { 'error': str(e) }, 400
        try:
            title = request_data['audioFileMetadata']['title']
            duration = request_data['audioFileMetadata']['duration']
            host = request_data['audioFileMetadata']['host']
            narrator = request_data['audioFileMetadata']['narrator']
            author = request_data['audioFileMetadata']['author']
            participants = request_data['audioFileMetadata']['participants']
            podcastSeries = request_data['audioFileMetadata']['podcastSeries']

            exists = Audio.query.filter_by(id=audioFileId,audio_type=audioType).first()
            if exists:
                audio = Audio.query.filter_by(id=audioFileId,audio_type=audioType).first()

                if audioType == 'song':
                    audio.title = title
                    audio.duration = duration
                    db.session.commit()

                elif audioType == 'audiobook':
                    audio.title = title
                    audio.duration = duration
                    audioType.author = author
                    audioType.narrator = narrator
                    db.session.commit()

                else:
                    audio.title = title
                    audio.duration = duration
                    audio.host = host
                    PodcastSeries.query.filter_by(audio_id=audioFileId).delete()
                    pod = PodcastParticipants.query.filter_by(audio_id=audioFileId).all()
                    PodcastParticipants.query.filter_by(audio_id=audioFileId).delete()

                    # add podcast episodes
                    if len(podcastSeries) > 0:
                        for s in podcastSeries:

                            # if podcast not exist
                            exists = PodcastSeries.query.filter_by(duration=s['duration'],name=s['name']).first()
                            if not exists:
                                ser= PodcastSeries(audio_id=audioFileId,duration=s['duration'],name=s['name'])
                                db.session.add(ser)
                            else:
                                return {'message': Messages.EACH_PODCAST_SERIES_MUST_BE_UNIQUE }, 409
                    for row in pod:
                        Users.query.filter_by(id=row.user_id).delete()
                    
                    # add participants
                    if len(participants)> 0:
                        for p in participants:
                            # if user email is unique
                            exists = Users.query.filter_by(email=p['email']).first()
                            if not exists:
                                users = Users(name=p['name'],email=p['email'])
                                db.session.add(users)
                                db.session.commit()
                            else:
                                return {'message': Messages.EMAIL_ALREADY_EXIST }, 409
                            userId = users.id
                            par = PodcastParticipants(audio_id=audioFileId,user_id=userId)
                            db.session.add(par)
                            
                    db.session.commit()
                    return {'message': Messages.DATA_UPDATED_SUCCESSFULLY }, 201
            else:
                return {'message': Messages.AUDIO_DOES_NOT_EXIST }, 201
        except Exception as e:
            print(str(e))
            db.session.rollback()
            print(str(e))
            return {'error':Messages.INTERNAL_SERVER_ERROR }, 500

class AudioList(Resource):
    # get different audio types list
    def get(self):
        try:
            request.pageOffset = int(request.args.get("pageOffset")) if request.args.get("pageOffset") else 1
            request.pageLimit = int(request.args.get("pageLimit")) if request.args.get("pageLimit") else 100
            
            # validate schema
            schema = {
                "audioType": {'type': 'string', 'required': True, 'nullable': False,'allowed':['song','audiobook','podcast']},
                "pageLimit": {'type': 'integer', 'required': True},
                "pageOffset": {'type': 'integer', 'required': True}
            }
            instance = {
                "audioType": request.args.get('audioType'),
                "pageLimit": request.pageLimit,
                "pageOffset": request.pageOffset
            }
            v = Validator()
            if not v.validate(instance, schema):
                return { 'error': v.errors }, 400
        except Exception as e:
            return { 'error': str(e) }, 400
        try:
            audioType = request.args.get('audioType')
            pageLimit = request.pageLimit
            pageOffset = request.pageOffset
            sqlDb = SqlQueryBuilder()
            audRes = []
            audioResult = sqlDb.readProcedureJson("spAudioList",[audioType,pageLimit,pageOffset])
            if len(audioResult):
                for res in audioResult:
                    if res['participants']:
                        res['participants'] = json.loads(res['participants'])
                    else:
                        res['participants'] = []
                    if res['series']:
                        res['series'] = json.loads(res['series'])
                    else:
                        res['series'] = []
                    fetchResult = {
                        "audioId":res["audioId"],
                        "title":res["title"],
                        "duration":res["duration"],
                        "podcastHost":res["podcastHost"],
                        "narrator":res["narrator"],
                        "uploadedTime":res["uploadedTime"],
                        "audioType":res["audioType"],
                        "participants":res['participants'],
                        "podcastSeries":res['series']
                    }
                    audRes.append(fetchResult)
                
                return {'message': audRes}, 201
            else:
                return {'error': Messages.RECORD_NOT_FOUND}, 404
        except Exception as e:
            print(str(e))
            return {'error': Messages.INTERNAL_SERVER_ERROR }, 500


class AudioDetail(Resource):

    # get audio detail by id
    def get(self,audioType,audioFileId):
        try:
            # validate schema
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
            sqlDb = SqlQueryBuilder()
            audioResult = sqlDb.readProcedureJson("spAudioById",[audioType,audioFileId])
            if len(audioResult):
                aud = audioResult[0]
                if aud['participants']:
                    aud['participants'] = json.loads(aud['participants'])
                else:
                    aud['participants'] = []
                if aud['series']:
                    aud['series'] = json.loads(aud['series'])
                else:
                    aud['series'] = []
                fetchResult = {
                    "audioId":aud["audioId"],
                    "title":aud["title"],
                    "duration":aud["duration"],
                    "podcastHost":aud["podcastHost"],
                    "narrator":aud["narrator"],
                    "uploadedTime":aud["uploadedTime"],
                    "audioType":aud["audioType"],
                    "participants":aud['participants'],
                    "podcastSeries":aud['series']
                }
                return {'message': fetchResult }, 201
            else:
                return {'error': Messages.RECORD_NOT_FOUND}, 404
        except Exception as e:
            return {'error': Messages.INTERNAL_SERVER_ERROR }, 500

    # delete audio
    def delete(self,audioType,audioFileId):
        try:
            # validate schema
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
            # if audio exist
            exists = Audio.query.filter_by(id=audioFileId,audio_type=audioType,is_deleted=0).first() is not None
            if exists:
                Audio.query.filter_by(id=audioFileId,audio_type=audioType).update(dict(is_deleted=1))
                db.session.commit()
                return {'message': Messages.AUDIO_DELETED }, 201
            else:
                return {'error': Messages.AUDIO_DOES_NOT_EXIST }, 404
        except Exception as e:
            return {'error': Messages.INTERNAL_SERVER_ERROR }, 500



