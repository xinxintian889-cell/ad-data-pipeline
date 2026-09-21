from app import create_app,db
app=create_app()

with app.app_context():
	db.create_all()

if _name_ == '_main_':
	app.run(debug=Ture)
