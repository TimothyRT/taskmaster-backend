from flask import Blueprint, jsonify, request

from .. import db
from ..models import Task


api_bp = Blueprint('api', __name__)


@api_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()

    try:
        assert data["category"] in ("Important", "Urgent", "Regular")
    except AssertionError:
        return jsonify({'error': 'Invalid category'}), 400
    
    try:
        new_task = Task(
            title=data['title'],
            description=data['description'],
            category=data['category']
        )
        
        db.session.add(new_task)
        db.session.commit()
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify(new_task.to_dict()), 201


@api_bp.route('/tasks/<string:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    
    try:
        task = Task.update_task(task_id, data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify(task.to_dict()), 200


@api_bp.route('/tasks/<string:task_id>', methods=['DELETE'])
def delete_task(task_id):   
    try:
        task = Task.delete_task(task_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify(task.to_dict()), 200


@api_bp.route('/tasks/<string:task_id>/done', methods=['PUT'])
def mark_task_as_done(task_id):   
    try:
        task = Task.mark_task_as_done(task_id)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
    return jsonify(task.to_dict()), 200


@api_bp.route('/tasks/<string:category>', methods=['GET'])
def get_tasks_by_category(category):
    category = category.capitalize()
    
    try:
        assert category in ("Important", "Urgent", "Regular")
    except AssertionError:
        return jsonify({'error': 'Invalid category'}), 400
    
    tasks = Task.get_tasks_by_category(category)
    return jsonify([task.to_dict() for task in tasks]), 200


@api_bp.route('/tasks', methods=['GET'])
def get_tasks():    
    tasks = Task.get_tasks()
    return jsonify([task.to_dict() for task in tasks]), 200
