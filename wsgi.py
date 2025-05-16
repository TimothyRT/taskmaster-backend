from app import app
from dotenv import load_dotenv
from extensions import db  # Now imports from extensions.py
import os

load_dotenv()

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{username}:{password}@{host}/{db_name}'.format(
    username=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    host=os.getenv('MYSQL_HOST'),
    db_name=os.getenv('MYSQL_DB')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)

db.init_app(app)  # Important: bind db to the app
application = app


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    