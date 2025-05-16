import os
from dotenv import load_dotenv


load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{username}:{password}@{host}/{db_name}'.format(
        username=os.getenv('MYSQL_USER', 'taskmaster'),
        password=os.getenv('MYSQL_PASSWORD', '))8bbjGV9Sw7K2+xH3'),
        host=os.getenv('MYSQL_HOST', 'sgp.domcloud.co'),
        db_name=os.getenv('MYSQL_NAME', 'taskmaster_db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
