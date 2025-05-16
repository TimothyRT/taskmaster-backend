from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import uuid
import os
from datetime import datetime
from enum import Enum
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{username}:{password}@{host}/{db_name}'.format(
    username=os.getenv('MYSQL_USER'),
    password=os.getenv('MYSQL_PASSWORD'),
    host=os.getenv('MYSQL_HOST'),
    db_name=os.getenv('MYSQL_DB')
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Base model for other database tables to inherit
class Base(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Enums for Task categories and status
class TaskCategory(str, Enum):
    IMPORTANT = "Important"
    URGENT = "Urgent"
    REGULAR = "Regular"

class TaskStatus(str, Enum):
    ACTIVE = "Active"
    DONE = "Done"
    DELETED = "Deleted"

class Task(Base):
    __tablename__ = 'tasks'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.Enum(TaskCategory), nullable=False, default=TaskCategory.REGULAR)
    last_updated = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    status = db.Column(db.Enum(TaskStatus), nullable=False, default=TaskStatus.ACTIVE)

    def __repr__(self):
        return f'<Task {self.title}>'


@app.route('/')
def index():
    return "F"


# API Routes
@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    
    new_task = Task(
        title=data['title'],
        description=data.get('description'),
        category=data.get('category', TaskCategory.REGULAR),
        status=TaskStatus.ACTIVE
    )
    
    db.session.add(new_task)
    db.session.commit()
    
    return {
        'id': new_task.id,
        'title': new_task.title,
        'description': new_task.description,
        'category': new_task.category.value,
        'status': new_task.status.value,
        'last_updated': new_task.last_updated.isoformat(),
        'created_at': new_task.created_at.isoformat()
    }, 201

# Error Handlers
# @app.errorhandler(404)
# def page_not_found(e):
#     return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')