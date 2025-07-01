import qrcode
import uuid
import os
from app import db
from app.models import QrCode
from flask import url_for

def generer_qr_code():
    code_uuid = str(uuid.uuid4())

    # Générer l’URL vers la page à 3 boutons AVANT d’enregistrer l’objet
    qr_url = url_for('client.page_boutons', code_uuid=code_uuid, _external=True)

    # Générer l’image du QR code
    qr_img = qrcode.make(qr_url)

    # Chemins
    rel_folder = os.path.join('static', 'qr_codes')
    abs_folder = os.path.join('app', rel_folder)
    os.makedirs(abs_folder, exist_ok=True)

    filename = f"hotel_{code_uuid}.png"
    abs_path = os.path.join(abs_folder, filename)
    qr_img.save(abs_path)

    # Enregistrement dans la base
    qr = QrCode(uuid=code_uuid)
    db.session.add(qr)
    db.session.commit()

    # Retourne le chemin relatif (pour HTML) + l’URL encodée
    rel_path = f"/{rel_folder}/{filename}"
    return rel_path, qr_url
