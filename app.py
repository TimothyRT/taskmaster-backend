from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from enum import Enum
import uuid

from extensions import db


app = Flask(__name__)


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


# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route('/')
def index():
    return "Hello world!"


# API Routes
@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    
    try:
        new_task = Task(
            title=data['title'],
            description=data.get('description'),
            category=data.get('category', TaskCategory.REGULAR),
            status=TaskStatus.ACTIVE
        )
        
        db.session.add(new_task)
        db.session.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return {
        'id': new_task.id,
        'title': new_task.title,
        'description': new_task.description,
        'category': new_task.category.value,
        'status': new_task.status.value,
        'last_updated': new_task.last_updated.isoformat(),
        'created_at': new_task.created_at.isoformat()
    }, 201


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')