import os

class Config:
	SECRET_KEY=os.environ.get('SECRET_KET') or 'you-will-never-guess'
	SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(os.path.abspath(os.getcwd()), 'app.db')

	SQLALCHEMY_TRACK_MODOFICATIONS=False
