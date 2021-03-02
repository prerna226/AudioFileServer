from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from main.models.audio_models import db
from manage import create_app

app = create_app('config')

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()