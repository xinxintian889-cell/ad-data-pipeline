from flask import Blueprint, request, jsonify
from app import db
from app.models import DataTask

# 引入Redis和Kafka工具
import redis
from app.kafka_producer import send_task_to_kafka

bp = Blueprint('api', __name__, url_prefix='/api')

# 初始化Redis连接
r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

@bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'file_path' not in data:
        return jsonify({'error': 'Missing required field: file_path'}), 400
    
    file_path = data['file_path']
    
    # 【核心逻辑】Redis去重：用file_path作为key，设置过期时间为1小时
    # 如果这个文件已经提交过，直接返回提示
    if r.exists(f"task_lock:{file_path}"):
        return jsonify({'message': 'Task already submitted recently', 'status': 'IGNORED'}), 200
    
    # 在Redis里打个标记
    r.setex(f"task_lock:{file_path}", 3600, "1") # 3600秒过期
    
    # 1. 创建数据库记录（暂不提交）
    new_task = DataTask(file_path=file_path)
    db.session.add(new_task)
    db.session.commit() # 提交后才能拿到自增ID
    
    # 2. 发送Kafka消息
    task_data = {
        'task_id': new_task.id,
        'file_path': file_path,
        'action': 'process_data'
    }
    try:
        send_task_to_kafka(task_data)
    except Exception as e:
        # 如果Kafka发送失败，删除数据库记录并回滚
        
        print("\n================ KAFKA 报错开始 ================")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误详情: {e}")
        print("================ KAFKA 报错结束 ================\n")

        db.session.delete(new_task)
        db.session.commit()
        return jsonify({'error': 'Failed to send task to queue', 'detail': str(e)}), 500
    
    return jsonify({'message': 'Task created and queued', 'task': new_task.to_dict()}), 201

# GET接口不用改，继续从MySQL查状态

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
