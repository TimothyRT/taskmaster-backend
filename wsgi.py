from app import app as application
from dotenv import load_dotenv
import os

from extensions import db

load_dotenv()

application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{username}:{password}@{host}/{db_name}'.format(
    username=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    host=os.getenv('MYSQL_HOST'),
    db_name=os.getenv('MYSQL_DB')
)
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SECRET_KEY'] = os.urandom(24)
db.init_app(app)
application = app