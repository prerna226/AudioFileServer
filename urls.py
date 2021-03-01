from flask import Blueprint
from flask_restful import Api
from main.services.hello_services import Hello
from main.services.audio_services import AudioResource

api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Route
api.add_resource(Hello, '/Hello')
api.add_resource(AudioResource, '/audio/<audioType>/<int:audioFileId>')
