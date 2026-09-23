from app import create_app, db
# 必须把你的模型导入进来，否则 db.create_all() 找不到有哪些表要建！
from app import models 

# 1. 创建 Flask 应用实例
app = create_app()

# 2. 推入应用上下文
with app.app_context():
    # 3. 根据模型创建所有表
    db.create_all()
    print("✅ 数据库表创建成功！")