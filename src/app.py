from flask import Flask

from .config import app_config
from .models import db, bcrypt
#from createtable import db

from .views.UserView import user_api as user_blueprint
from .views.PriceView import price_api as price_blueprint

env_name = 'development'


def create_app(env_name):
    """
    Create app
    """

    # app initiliazation
    app = Flask(__name__)

    app.config.from_object(app_config[env_name])

    # initializing bcrypt and db
    bcrypt.init_app(app)
    db.init_app(app)

    app.register_blueprint(user_blueprint, url_prefix='/users')
    app.register_blueprint(price_blueprint, url_prefix='/prices')
    #app.register_blueprint(user_blueprint, url_prefix='/api/v1//users')
    #app.register_blueprint(price_blueprint, url_prefix='/api/v1//prices')

    @app.route('/', methods=['GET'])
    def index():
        print("testing!")
        return 'Congratulations! Your API is working'

    @app.errorhandler(404)
    @app.route("/error404")
    def page_not_found(error):
        return app.send_static_file('404.html')


    @app.errorhandler(500)
    @app.route("/error500")
    def requests_error(error):
        return app.send_static_file('500.html')

    return app
