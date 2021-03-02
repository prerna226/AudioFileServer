from flask import Blueprint
from flask_restful import Api
from main.services.audio_services import AudioDetail,AddAudio,UpdateAudio,AudioList

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(AudioDetail, '/audio/<audioType>/<int:audioFileId>')
api.add_resource(AddAudio, '/audio')
api.add_resource(UpdateAudio,'/audio/<audioType>/<int:audioFileId>')
api.add_resource(AudioList, '/audio/list')

