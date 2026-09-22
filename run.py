from app import create_app, db

app = create_app()

# 自动创建数据库表（第一次运行时）
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, port=5000)

