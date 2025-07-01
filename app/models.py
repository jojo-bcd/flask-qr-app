from datetime import datetime
from app import db
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    texte_fr = db.Column(db.String(255), nullable=False)   # Texte français
    texte_en = db.Column(db.String(255), nullable=True)    # Texte anglais

    type = db.Column(db.String(20), nullable=False)        # 'etoiles', 'oui_non', 'texte'
    categorie = db.Column(db.String(50), nullable=False)   # ex: 'reunion', 'restauration', 'general'
    groupe = db.Column(db.String(50), nullable=False)      # ex: 'Guest', 'Resident', 'Visiteur'
    
    reponses = db.relationship('Reponse', back_populates='question', cascade='all, delete-orphan')

    @property
    def texte(self):
        from flask import session
        lang = session.get('lang', 'fr')
        return self.texte_en if lang == 'en' and self.texte_en else self.texte_fr

    def __repr__(self):
        return f"<Question {self.texte_fr}>"


class QrCode(db.Model):
    __tablename__ = 'qr_code'
    
    id = db.Column(db.Integer, primary_key=True)
    uuid = db.Column(db.String(100), unique=True, nullable=False)
    type = db.Column(db.String(50), nullable=False, default='general')  # ex : 'event', 'hotel'
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    avis = db.relationship('Avis', back_populates='qr', cascade='all, delete-orphan')

class Avis(db.Model):
    __tablename__ = 'avis'
    
    id = db.Column(db.Integer, primary_key=True)
    qr_id = db.Column(db.Integer, db.ForeignKey('qr_code.id'), nullable=False)
    groupe = db.Column(db.String(50), nullable=False)  # Pour savoir à quel formulaire ça correspond
    note = db.Column(db.Integer)  # Note via étoiles (1 à 5)
    commentaire = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    nom = db.Column(db.String(100))
    numero = db.Column(db.String(50))
    entreprise = db.Column(db.String(100))
    chambre_id = db.Column(db.Integer, db.ForeignKey('chambres.id'), nullable=True)

    qr = db.relationship('QrCode', back_populates='avis')
    reponses = db.relationship('Reponse', back_populates='avis', cascade='all, delete-orphan')

    @property
    def note_globale(self):
        """Utilise uniquement la note étoile comme note globale."""
        return float(self.note) if self.note is not None else None


class Reponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    avis_id = db.Column(db.Integer, db.ForeignKey('avis.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    valeur = db.Column(db.String(255), nullable=False)

    avis = db.relationship('Avis', back_populates='reponses', overlaps="reponses")
    question = db.relationship('Question', back_populates='reponses', overlaps="reponses")

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    mot_de_passe = db.Column(db.String(255))
    

class Chambre(db.Model):
    __tablename__ = 'chambres'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)

    avis = db.relationship('Avis', backref='chambre', lazy=True)
