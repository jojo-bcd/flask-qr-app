from flask import Blueprint, render_template
from app.utils import generer_qr_code

main = Blueprint('main', __name__)


@main.route('/generer-qr-hotel')
def generer_qr_hotel():
    filepath, url = generer_qr_code()  # Plus besoin de passer de label ni d’URL manuelle
    image = filepath.replace("app/static", "/static")  # Pour affichage dans HTML
    return f"""
        <p>QR Code général de l’hôtel généré.</p>
        <p>URL : {url}</p>
        <img src='{image}' width='300'>
    """