from flask import Blueprint, render_template
from app.models import Avis, Reponse  # ✅ Assure-toi d'importer Reponse
from app import db
from sqlalchemy.orm import joinedload

admin = Blueprint("admin", __name__)

@admin.route("/2")
def dashboard():
    avis = (
        db.session.query(Avis)
        .options(
            joinedload(Avis.qr),  # charge la chambre
            joinedload(Avis.reponses).joinedload(Reponse.question)  # ✅ on utilise l'attribut, pas une chaîne
        )
        .order_by(Avis.date.desc())
        .all()
    )

    return render_template("dashboard.html", avis=avis)
