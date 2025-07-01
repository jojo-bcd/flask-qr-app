from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
migrate = Migrate()
mail = Mail()  # ← On initialise l’objet mail sans le lier

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Configurations personnalisées (peuvent aussi être mises dans Config)
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'jjaures077@gmail.com'
    app.config['MAIL_PASSWORD'] = 'mqhfgtmjhazsssxu'
    app.config['MAIL_DEFAULT_SENDER'] = ('Hôtel Azalaï', 'jjaures077@gmail.com')

    # Initialiser les extensions avec l'app
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)  # ← c'est ici qu'on connecte mail à app

    # Importer les modèles dans le contexte de l'app
    with app.app_context():
        from app import models

    # Enregistrement des blueprints
    from app.routes.main import main
    from app.routes.client import client
    from app.routes.admin import admin

    app.register_blueprint(admin)
    app.register_blueprint(main)
    app.register_blueprint(client)

    return app
