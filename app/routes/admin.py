from flask import Blueprint, render_template, request, jsonify  # request doit être importé ici
from app import db
from app.models import Admin, Avis, Reponse
from sqlalchemy.orm import joinedload, load_only  # Assure-toi que load_only est bien importé
from datetime import datetime, timedelta
import logging
from functools import wraps
from flask import session, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from app.models import Chambre  # assure-toi que le modèle est bien importé



# Configuration du logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

admin = Blueprint('admin', __name__)



@admin.route("/final")
def jojo():
    return render_template("base.html")

@admin.route("/admin")
def dashboard():
    avis = (
        db.session.query(Avis)
        .options(
            joinedload(Avis.qr),
            joinedload(Avis.reponses).joinedload(Reponse.question)
        )
        .order_by(Avis.date.desc())
        .all()
    )

    chambres = db.session.query(Chambre).all()  # Ajout ici

    return render_template("dashboard.html", avis=avis, chambres=chambres)

# route api avis groupe resident 

@admin.route("/api/avis")
def api_avis():
    try:
        # Paramètres de requête
        start_date = request.args.get('start')
        end_date = request.args.get('end')
        period = request.args.get('period', 'day')
        chambre_nom = request.args.get('chambre')

        # Requête de base avec chargement anticipé + champ note forcé
        query = db.session.query(Avis).options(
            load_only(Avis.note, Avis.date, Avis.commentaire),  # 👈 important pour charger "note"
            joinedload(Avis.qr),
            joinedload(Avis.reponses).joinedload(Reponse.question),
            joinedload(Avis.chambre)  # Pour le .chambre.nom dans le JSON
        ).order_by(Avis.date.desc())

        # Filtrage par dates spécifiques
        if start_date and end_date:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d')
                end = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
                query = query.filter(Avis.date.between(start, end))
            except ValueError as e:
                logger.error(f"Erreur de conversion de date: {e}")
                return jsonify({"error": "Format de date invalide. Utilisez YYYY-MM-DD"}), 400

        # Filtrage par période prédéfinie
        elif period:
            now = datetime.now()

            if period == 'day':
                start_date_val = now - timedelta(days=1)
            elif period == 'week':
                start_date_val = now - timedelta(weeks=1)
            elif period == 'month':
                start_date_val = now - timedelta(days=30)
            else:
                return jsonify({"error": "Période invalide. Options: day, week, month"}), 400

            query = query.filter(Avis.date >= start_date_val)

        # Filtrage par nom de chambre
        if chambre_nom:
            query = query.join(Avis.chambre).filter(Chambre.nom == chambre_nom)

        avis = query.all()

        avis_data = []
        for avi in avis:
            # 🔍 Debug temporaire pour voir les vraies valeurs
            print("DEBUG → ID:", avi.id, "note:", avi.note, "note_globale:", avi.note_globale)

            avi_dict = {
                'id': avi.id,
                'date': avi.date.isoformat(),
                'note_globale': avi.note_globale,
                'commentaire': avi.commentaire,
                'chambre': avi.chambre.nom if avi.chambre else None,
                'reponses': []
            }

            for rep in avi.reponses:
                if rep.question and rep.question.groupe == "Resident":
                    rep_dict = {
                        'question_id': rep.question.id,
                        'question': {
                            'id': rep.question.id,
                            'text': rep.question.texte
                        },
                        'reponse': rep.valeur
                    }
                    avi_dict['reponses'].append(rep_dict)

            avis_data.append(avi_dict)

        return jsonify(avis_data)

    except Exception as e:
        logger.exception("Erreur critique dans l'API avis")
        return jsonify({"error": "Erreur interne du serveur", "details": str(e)}), 500


#*****************************************route avis groupe Event ********************************************




@admin.route("/event")
def dashboard_event():
    # On charge uniquement les avis ayant des réponses du groupe "Event"
    avis = (
        db.session.query(Avis)
        .options(
            joinedload(Avis.reponses).joinedload(Reponse.question)
        )
        .order_by(Avis.date.desc())
        .all()
    )

    # On filtre uniquement les avis qui ont au moins une réponse du groupe "Event"
    avis_event = []
    for a in avis:
        if any(r.question and r.question.groupe == "Event" for r in a.reponses):
            avis_event.append(a)

    return render_template("dasboardevent.html", avis=avis_event, active_page="event")



@admin.route("/api/avis_event")
def api_avis_event():
    try:
        # Paramètres de requête
        start_date = request.args.get('start')
        end_date = request.args.get('end')
        period = request.args.get('period', 'day')

        # Requête de base (pas de chambre ici)
        query = db.session.query(Avis).options(
            load_only(Avis.note, Avis.date, Avis.commentaire),
            joinedload(Avis.reponses).joinedload(Reponse.question)
        ).order_by(Avis.date.desc())

        # Filtrage par dates
        if start_date and end_date:
            try:
                start = datetime.strptime(start_date, '%Y-%m-%d')
                end = datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1)
                query = query.filter(Avis.date.between(start, end))
            except ValueError as e:
                logger.error(f"Erreur date: {e}")
                return jsonify({"error": "Format de date invalide. Utilisez YYYY-MM-DD"}), 400
        elif period:
            now = datetime.now()
            if period == 'day':
                start_val = now - timedelta(days=1)
            elif period == 'week':
                start_val = now - timedelta(weeks=1)
            elif period == 'month':
                start_val = now - timedelta(days=30)
            else:
                return jsonify({"error": "Période invalide. Options: day, week, month"}), 400
            query = query.filter(Avis.date >= start_val)

        avis = query.all()
        avis_data = []

        for avi in avis:
            avi_dict = {
                'id': avi.id,
                'date': avi.date.isoformat(),
                'note_globale': avi.note_globale,
                'commentaire': avi.commentaire,
                'reponses': {
                    'reunion': [],
                    'restauration': [],
                    'general': []
                }
            }

            for rep in avi.reponses:
                if rep.question and rep.question.groupe == "Event":
                    categorie = rep.question.categorie  # reunion, restauration, general
                    if categorie in avi_dict['reponses']:
                        avi_dict['reponses'][categorie].append({
                            'question_id': rep.question.id,
                            'question': rep.question.texte,
                            'reponse': rep.valeur
                        })

            # On ne garde que les avis contenant au moins une réponse Event
            if any(avi_dict['reponses'][cat] for cat in avi_dict['reponses']):
                avis_data.append(avi_dict)

        return jsonify(avis_data)

    except Exception as e:
        logger.exception("Erreur dans l'API /api/avis_event")
        return jsonify({"error": "Erreur interne du serveur", "details": str(e)}), 500



#route connexion 

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash("Veuillez vous connecter pour accéder à cette page", "warning")
            return redirect(url_for('admin.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        mot_de_passe = request.form['password']
        admin_user = Admin.query.filter_by(email=email).first()

        if admin_user and check_password_hash(admin_user.mot_de_passe, mot_de_passe):
            session['admin_id'] = admin_user.id
            flash('Connexion réussie', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Email ou mot de passe incorrect', 'danger')

    return render_template('login.html')

@admin.route('/logout')
def logout():
    session.pop('admin_id', None)
    flash("Déconnexion réussie", "info")
    return redirect(url_for('admin.login'))

#rote inscription 
@admin.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        mot_de_passe = request.form['password']
        confirmation = request.form['confirm_password']

        # Vérifier que les champs sont valides
        if mot_de_passe != confirmation:
            flash("Les mots de passe ne correspondent pas.", "danger")
            return redirect(url_for('admin.register'))

        # Vérifier si l'admin existe déjà
        if Admin.query.filter_by(email=email).first():
            flash("Un administrateur avec cet email existe déjà.", "warning")
            return redirect(url_for('admin.register'))

        # Créer et enregistrer le nouvel admin
        hashed_password = generate_password_hash(mot_de_passe)
        new_admin = Admin(email=email, mot_de_passe=hashed_password)
        db.session.add(new_admin)
        db.session.commit()

        flash("Administrateur créé avec succès. Vous pouvez maintenant vous connecter.", "success")
        return redirect(url_for('admin.login'))

    return render_template('register.html')


#route ajout chambre



@admin.route("/chambres", methods=["GET", "POST"])
def gestion_chambres():
    if request.method == "POST":
        nom_chambre = request.form.get("nom_chambre")
        if nom_chambre:
            nouvelle_chambre = Chambre(nom=nom_chambre.strip())
            db.session.add(nouvelle_chambre)
            db.session.commit()
            flash("Chambre ajoutée avec succès", "success")
            return redirect(url_for("admin.gestion_chambres"))
        else:
            flash("Le nom de la chambre est requis", "danger")

    chambres = Chambre.query.order_by(Chambre.id.desc()).all()
    return render_template("chambre.html", chambres=chambres)


#route pur recuperer les chambres 

@admin.route('/api/chambres')
def api_chambres():
    chambres = Chambre.query.all()
    result = [{'id': c.id, 'nom': c.nom} for c in chambres]
    return jsonify(result)
