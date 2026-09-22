import os

class Config:
	# 数据库连接字符串： mysql+pymysql://用户名:密码@主机:端口/数据库名
	SQLALCHEMY_DATABASE_URI='mysql+pymysql://root:123456@localhost:3306/ad_data_db'
	#关闭SQLAlchemy的对象修改追踪，介绍内存
	SQLALCHEMY_TRACK_MODOFICATIONS=False
