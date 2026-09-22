from app import db
from datetime import datetime


class DataTask(db.Model):
    """数据处理任务模型"""
    _tablename_ = 'data_task'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    file_path = db.Column(db.String(255), nullable=False)  # 数据文件路径
    # 任务状态：PENDING,SUCCESS,FAILED
    status = db.Column(db.String(50), default='PENDING')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'file_path': self.file_path,
            'status': self.status,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
