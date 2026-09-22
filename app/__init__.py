from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config

# 全局初始化SQLAlchemy对象，此时还没有绑定到具体的app
db = SQLAlchemy()


def create_app():
    """应用工厂函数：用于创建flask应用实例"""
    app = Flask(__name__)

    # 加载配置
    app.config.from_object(Config)

    # 将db与当前app绑定
    db.init_app(app)

    # 注册蓝图（路由）
    from app.routes import bp
    app.register_blueprint(bp)
    return app
