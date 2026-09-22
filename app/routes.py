
from flask import Blueprint, jsonify, request
from app import db
from app.models import DataTask

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.route('/tasks', methods=['POST'])
def create_task():
    """创建数据处理任务"""
    # 1.获取请求体中的JSON数据
    data = request.get_json()
    # 2.参数校验
    if not data or 'file_path' not in data:
        return jsonify({'error': 'Missing required field: file_path'}), 400
    # 3.创建任务对象并保存数据库
    new_task = DataTask(file_path=data['file_path'])
    
    #使用try/except，回滾
    try:
        db.session.add(new_task)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}),500
    # 4.返回结果，201表示资源创建成功
    return jsonify([{'message': 'Task created', 'task': new_task.to_dict()}]), 201


@bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """根据ID查询任务状态"""
    # 1.查询数据库
    task = DataTask.query.get(task_id)

    # 2.如果任务不存在，返回404
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    # 3.返回任务信息
    return jsonify(task.to_dict()), 200
