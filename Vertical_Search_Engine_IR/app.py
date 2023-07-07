import os
from flask import Flask

from controllers.main_controller import Home, ResultPage
from config.dbconfig import db

#create flask object
app = Flask(__name__)

#database configurations
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(os.getcwd(),'database.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


# define routes
app.add_url_rule('/', view_func = Home.as_view("index"))
app.add_url_rule("/result", view_func=ResultPage.as_view("resultpage"))

# up and run flask
if __name__ == '__main__':
    app.run(debug=True)