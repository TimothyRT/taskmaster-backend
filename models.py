from datetime import datetime
from sqlalchemy import and_, case, not_
import uuid

from . import db


class Task(db.Model):
    __tablename__ = 'tasks'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(36), nullable=False, default="Regular")  # Important, Urgent, Regular
    last_updated = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(36), nullable=False, default="Active")  # Active, Done, Deleted

    def __repr__(self):
        return f'<Task {self.title}>'
        
    @classmethod
    def get_tasks_by_category(cls, category):
        return cls.query.filter(
            and_(
                cls.category == category,
                cls.status != "Deleted"
            )
        ).order_by(
            case(
                (cls.status == "Active", 0),
                (cls.status == "Done", 1),
                else_=2
            )
        ).all()

    @classmethod
    def get_tasks(cls):
        return cls.query.filter(not(cls.status == "Deleted")).all()

    @classmethod
    def update_task(cls, task_id, data):
        task = cls.query.get(task_id)
        if not task:
            return None
        
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'category' in data and data['category'] in ("Important", "Urgent", "Regular"):
            task.category = data['category']
        if 'status' in data and data['status'] in ("Active", "Done", "Deleted"):
            task.status = data['status']
        
        task.last_updated = datetime.utcnow().date()
        
        try:
            db.session.commit()
            return task
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Failed to update task: {str(e)}")

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'category': self.category,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None,
            'status': self.status
        }
        
    @classmethod
    def delete_task(cls, task_id):
        task = cls.query.get(task_id)
        if not task:
            return None
            
        task.status = "Deleted"
        task.last_updated = datetime.utcnow().date()
        
        try:
            db.session.commit()
            return task
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Failed to delete task: {str(e)}")

    @classmethod
    def mark_task_as_done(cls, task_id):
        task = cls.query.get(task_id)
        if not task:
            return None
            
        task.status = "Done"
        task.last_updated = datetime.utcnow().date()
        
        try:
            db.session.commit()
            return task
        except Exception as e:
            db.session.rollback()
            raise ValueError(f"Failed to mark task as done: {str(e)}")