from flask import Blueprint, render_template, request, redirect, flash, abort, url_for
from app.models import Avis, QrCode, Question, Reponse, Chambre
from flask_mail import Message
from app import mail
from app import db
from datetime import datetime
from flask import Blueprint, request, jsonify, session


client = Blueprint('client', __name__)

@client.route("/resident/<code_uuid>", methods=["GET", "POST"])
def formulaire_resident(code_uuid):
    qr = QrCode.query.filter_by(uuid=code_uuid).first_or_404()
    questions = Question.query.filter_by(groupe="Resident").all()
    chambres = Chambre.query.all()

    if request.method == "POST":
        note = request.form.get("note")
        commentaire = request.form.get("commentaire", "").strip()
        chambre_id = request.form.get("chambre_id")

        if not note:
            flash("La note est obligatoire", "error")
        else:
            try:
                avis = Avis(
                    qr_id=qr.id,
                    groupe="Resident",
                    note=int(note),
                    commentaire=commentaire,
                    chambre_id=int(chambre_id) if chambre_id else None,
                    date=datetime.now()
                )
                db.session.add(avis)
                db.session.flush()

                reponses_count = 0
                contact_ok = False

                for question in questions:
                    valeur = request.form.get(f"reponses[{question.id}]") or request.form.get(f"question_{question.id}")
                    if valeur is not None:
                        valeur = str(valeur).strip()
                        if valeur and valeur != "0":
                            reponse = Reponse(
                                avis_id=avis.id,
                                question_id=question.id,
                                valeur=valeur
                            )
                            db.session.add(reponse)
                            reponses_count += 1

                            if "Pouvons-nous vous écrire" in question.texte and valeur == "Oui":
                                contact_ok = True

                if reponses_count == 0:
                    flash("Veuillez répondre à au moins une question", "error")
                    db.session.rollback()
                    return render_template("form.html", qr_identifiant=qr.uuid, questions=questions, chambres=chambres)

                # 🔔 Traitement des infos contact
                client_email = request.form.get("client_email", "").strip()
                client_nom = request.form.get("client_nom", "").strip()
                client_tel = request.form.get("client_tel", "").strip()

                # 🔔 Envoi de l'e-mail si autorisé
                if contact_ok and client_email:
                    try:
                        msg = Message(
                            subject="Merci pour votre retour",
                            recipients=[client_email],
                            body=f"""Bonjour {client_nom or "cher client"},

Cher Monsieur, Madame,

Nous vous remercions pour la note/le commentaire que vous avez laissé sur notre hôtel. 

Nous sommes ravis que vous ayez apprécié nos services et espérons vous accueillir à nouveau très prochainement. 

Recevez, Monsieur, nos distinguées salutations.

Service Relation client

Cordialement,  
L’équipe Azalaï
"""
                        )
                        mail.send(msg)
                        flash("Un message de remerciement a été envoyé à l’adresse fournie.", "info")
                    except Exception as e:
                        flash("L’avis a été enregistré, mais le message de remerciement n’a pas pu être envoyé.", "warning")
                        print(f"[ERREUR ENVOI MAIL] {e}")

                db.session.commit()
                flash(f"Merci pour votre avis ! ({reponses_count} réponses enregistrées)", "success")
                return redirect(url_for('client.formulaire_resident', code_uuid=code_uuid))


            except ValueError as e:
                db.session.rollback()
                flash("La note doit être un nombre valide", "error")
                print(f"[ERREUR DE VALEUR] {e}")
            except Exception as e:
                db.session.rollback()
                flash("Une erreur est survenue lors de l'enregistrement", "error")
                print(f"[ERREUR ENREGISTREMENT] {e}")
                print(f"Form data: {dict(request.form)}")

    return render_template("form.html", qr_identifiant=qr.uuid, questions=questions, chambres=chambres)
#--------------------------route event-------------------------------------
@client.route("/event/<code_uuid>", methods=["GET", "POST"])
def formulaire_event(code_uuid):
    qr = QrCode.query.filter_by(uuid=code_uuid).first_or_404()
    questions = Question.query.filter_by(groupe="Event").all()

    if request.method == "POST":
        nom = request.form.get("nom", "").strip()
        #prenom = request.form.get("prenom", "").strip()
        numero = request.form.get("numero", "").strip()
        entreprise = request.form.get("entreprise", "").strip()
        note = request.form.get("note")
        commentaire = request.form.get("commentaire", "").strip()

        if not note:
            flash("La note est obligatoire", "error")
        else:
            try:
                avis = Avis(
                    qr_id=qr.id,
                    groupe="Event",  # Important si ce champ est NOT NULL
                    note=int(note),
                    commentaire=commentaire,
                    date=datetime.now(),
                    nom=nom,
#prenom=prenom,
                    numero=numero,
                    entreprise=entreprise
                )
                db.session.add(avis)
                db.session.flush()

                reponses_count = 0
                for question in questions:
                    valeur = request.form.get(f"reponses[{question.id}]") or request.form.get(f"question_{question.id}")
                    if valeur is not None:
                        valeur = str(valeur).strip()
                        if valeur and valeur != "0":
                            reponse = Reponse(
                                avis_id=avis.id,
                                question_id=question.id,
                                valeur=valeur
                            )
                            db.session.add(reponse)
                            reponses_count += 1
                            print(f"Réponse enregistrée - Question {question.id}: {valeur}")

                if reponses_count == 0:
                    flash("Veuillez répondre à au moins une question", "error")
                    db.session.rollback()
                    return render_template("form 2.html", qr_identifiant=qr.uuid, questions=questions)

                db.session.commit()
                flash(f"Merci pour votre avis ! ({reponses_count} réponses enregistrées)", "success")
                return redirect(url_for('client.formulaire_event', code_uuid=code_uuid))


            except ValueError as e:
                db.session.rollback()
                flash("La note doit être un nombre valide", "error")
                print(f"Erreur de valeur: {e}")
            except Exception as e:
                db.session.rollback()
                flash("Une erreur est survenue lors de l'enregistrement", "error")
                print(f"Erreur lors de l'enregistrement: {e}")
                print(f"Form data: {dict(request.form)}")

    return render_template("form 2.html", qr_identifiant=qr.uuid, questions=questions)






@client.route("/choix/<code_uuid>")
def page_boutons(code_uuid):
    return render_template("choix.html", code_uuid=code_uuid)


#************************                             route         dasboard                 **********************************
@client.route("/statistiques")
def statistiques():
    """Route pour afficher les statistiques avec moyennes par catégorie"""
    
    # Calculer les moyennes par catégorie
    stats_hebergement = db.session.query(
        func.avg(Reponse.valeur.cast(db.Float)).label('moyenne'),
        func.count(Reponse.id).label('total_reponses')
    ).join(Question).filter(
        Question.categorie == 'hébergement',
        Reponse.valeur.regexp_match('^[1-5]$')  # Seulement les notes de 1 à 5
    ).first()
    
    stats_restauration = db.session.query(
        func.avg(Reponse.valeur.cast(db.Float)).label('moyenne'),
        func.count(Reponse.id).label('total_reponses')
    ).join(Question).filter(
        Question.categorie == 'restauration',
        Reponse.valeur.regexp_match('^[1-5]$')  # Seulement les notes de 1 à 5
    ).first()
    
    # Statistiques détaillées par question pour hébergement
    details_hebergement = db.session.query(
        Question.texte,
        func.avg(Reponse.valeur.cast(db.Float)).label('moyenne'),
        func.count(Reponse.id).label('total')
    ).join(Reponse).filter(
        Question.categorie == 'hébergement',
        Reponse.valeur.regexp_match('^[1-5]$')
    ).group_by(Question.id, Question.texte).all()
    
    # Statistiques détaillées par question pour restauration
    details_restauration = db.session.query(
        Question.texte,
        func.avg(Reponse.valeur.cast(db.Float)).label('moyenne'),
        func.count(Reponse.id).label('total')
    ).join(Reponse).filter(
        Question.categorie == 'restauration',
        Reponse.valeur.regexp_match('^[1-5]$')
    ).group_by(Question.id, Question.texte).all()
    
    # Évolution des notes dans le temps (derniers 30 jours)
    from datetime import datetime, timedelta
    date_limite = datetime.now() - timedelta(days=30)
    
    evolution = db.session.query(
        func.date(Avis.date).label('date'),
        Question.categorie,
        func.avg(Reponse.valeur.cast(db.Float)).label('moyenne')
    ).join(Reponse, Avis.id == Reponse.avis_id)\
     .join(Question, Reponse.question_id == Question.id)\
     .filter(
         Avis.date >= date_limite,
         Reponse.valeur.regexp_match('^[1-5]$')
     ).group_by(func.date(Avis.date), Question.categorie)\
     .order_by(func.date(Avis.date)).all()
    
    # Préparer les données pour les graphiques
    data = {
        'moyennes_generales': {
            'hebergement': round(stats_hebergement.moyenne or 0, 2),
            'restauration': round(stats_restauration.moyenne or 0, 2),
            'total_hebergement': stats_hebergement.total_reponses or 0,
            'total_restauration': stats_restauration.total_reponses or 0
        },
        'details_hebergement': [
            {
                'question': d.texte,
                'moyenne': round(d.moyenne, 2),
                'total': d.total
            } for d in details_hebergement
        ],
        'details_restauration': [
            {
                'question': d.texte,
                'moyenne': round(d.moyenne, 2),
                'total': d.total
            } for d in details_restauration
        ],
        'evolution': [
            {
                'date': e.date.strftime('%Y-%m-%d'),
                'categorie': e.categorie,
                'moyenne': round(e.moyenne, 2)
            } for e in evolution
        ]
    }
    
    return render_template("statistiques.html", data=data)

#nouvelle route 
def translate_questions_list(questions, language):
    """Convertit une liste d’objets Question SQLAlchemy en dictionnaire avec traduction"""
    return [
        {
            'id': q.id,
            'texte': q.texte_en if language == 'en' else q.texte_fr,
            'type': q.type,
            'categorie': q.categorie,
            'groupe': q.groupe
        }
        for q in questions
    ]

# Route pour changer de langue (AJAX)
@client.route('/set_language', methods=['POST'])
def set_language():
    """
    Change la langue actuelle (stockée en session) et renvoie les questions traduites.
    Cette route est appelée par JavaScript quand l'utilisateur clique sur "FR" ou "EN".
    """
    data = request.get_json()
    language = data.get('language', 'fr')

    if language not in ['fr', 'en']:
        return jsonify({'success': False, 'error': 'Invalid language'})

    # Sauvegarde la langue choisie dans la session
    session['language'] = language

    # Récupère toutes les questions de la base de données
    questions = Question.query.all()

    # Traduit les questions selon la langue choisie
    translated_questions = [
        {
            "id": q.id,
            "texte": q.texte_en if language == 'en' else q.texte_fr,
            "type": q.type,
            "categorie": q.categorie,
            "groupe": q.groupe
        }
        for q in questions
    ]

    # Renvoie les questions traduites
    return jsonify({
        'success': True,
        'questions': translated_questions
    })

# Votre route principale 1(modifiée)
@client.route('/')
def index():
    current_language = session.get('language', 'fr')

    # On ne récupère que les questions du groupe "Resident"
    questions = Question.query.filter_by(groupe='Resident').all()

    translated_questions = translate_questions_list(questions, current_language)

    return render_template('form.html',
                           questions=translated_questions,
                           current_language=current_language)



# Votre route principale 1(modifiée)
@client.route('/Event')
def form_visiteur():
    current_language = session.get('language', 'fr')

    # On ne récupère que les questions du groupe "Visiteur"
    questions = Question.query.filter_by(groupe='Event').all()

    translated_questions = translate_questions_list(questions, current_language)

    return render_template('form 2.html',
                           questions=translated_questions,
                           current_language=current_language)



 # Route pour obtenir les questions traduites (AJAX)
@client.route('/get_translated_questions')
def get_translated_questions():
    """Route pour récupérer les questions traduites via AJAX"""
    language = request.args.get('language', 'fr')
    
    questions = Question.query.all()
    translated_questions = translate_questions_list(questions, language)
    
    return jsonify({
        'questions': translated_questions
    })