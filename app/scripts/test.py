from app import create_app, db
from app.models import Question

app = create_app()


questions = [
    # Resident - Hébergement
    {"texte": "Accueil à la réception", "type": "etoiles", "categorie": "Hébergement", "groupe": "Resident"},
    {"texte": "Procédures d'enregistrement", "type": "etoiles", "categorie": "Hébergement", "groupe": "Resident"},
    {"texte": "Confort de la chambre", "type": "etoiles", "categorie": "Hébergement", "groupe": "Resident"},
    {"texte": "Propreté de la chambre", "type": "etoiles", "categorie": "Hébergement", "groupe": "Resident"},
    {"texte": "Service de portier-bagagiste", "type": "etoiles", "categorie": "Hébergement", "groupe": "Resident"},
    {"texte": "Service de la piscine", "type": "etoiles", "categorie": "Hébergement", "groupe": "Resident"},

    # Resident - Restauration
    {"texte": "Service en salle à manger", "type": "etoiles", "categorie": "Restauration", "groupe": "Resident"},
    {"texte": "Service au bar", "type": "etoiles", "categorie": "Restauration", "groupe": "Resident"},
    {"texte": "Service au Room Service", "type": "etoiles", "categorie": "Restauration", "groupe": "Resident"},
    {"texte": "Service en salle de conférence", "type": "etoiles", "categorie": "Restauration", "groupe": "Resident"},
    {"texte": "Ambiance", "type": "etoiles", "categorie": "Restauration", "groupe": "Resident"},
    {"texte": "Qualité de la nourriture", "type": "etoiles", "categorie": "Restauration", "groupe": "Resident"},
    {"texte": "Choix de menus", "type": "etoiles", "categorie": "Restauration", "groupe": "Resident"},
    {"texte": "Rapport Qualité/Prix", "type": "etoiles", "categorie": "Restauration", "groupe": "Resident"},

    # Resident - Général
    {"texte": "Qu'aurions-nous pu faire de plus pour rendre votre séjour encore plus agréable ?", "type": "texte", "categorie": "Général", "groupe": "Resident"},
    {"texte": "Pouvons-nous vous écrire afin de répondre à vos commentaires ?", "type": "oui_non", "categorie": "Général", "groupe": "Resident"},
 # Event - Réunion
    {"texte": "Avez-vous été bien accueilli par le service commercial ?", "type": "etoiles", "categorie": "reunion", "groupe": "Event"},
    {"texte": "Réactivité du service commercial dans l’organisation de votre réunion", "type": "etoiles", "categorie": "reunion", "groupe": "Event"},
    {"texte": "La salle de réunion était-elle bien équipée et confortable ?", "type": "etoiles", "categorie": "reunion", "groupe": "Event"},
    {"texte": "Avez-vous rencontré des problèmes techniques lors du séminaire ?", "type": "oui_non", "categorie": "reunion", "groupe": "Event"},
    {"texte": "Comment avez-vous trouvé le service en salle de réunion ?", "type": "etoiles", "categorie": "reunion", "groupe": "Event"},

    # Event - Restauration
    {"texte": "Comment avez-vous trouvé le service au restaurant ?", "type": "etoiles", "categorie": "restauration", "groupe": "Event"},
    {"texte": "Avez-vous été servi à temps ?", "type": "etoiles", "categorie": "restauration", "groupe": "Event"},
    {"texte": "Comment avez-vous trouvé la qualité des plats servis lors de votre séminaire ?", "type": "etoiles", "categorie": "restauration", "groupe": "Event"},
    {"texte": "Comment avez-vous trouvé la qualité des pauses café ?", "type": "etoiles", "categorie": "restauration", "groupe": "Event"},
    {"texte": "Souhaitez-vous revenir pour un autre séminaire ?", "type": "oui_non", "categorie": "restauration", "groupe": "Event"},

    # Event - Général
    {"texte": "Au cours de votre séminaire avez-vous rencontré d’autres difficultés non signalées ?", "type": "texte", "categorie": "general", "groupe": "Event"},
    {"texte": "Pour améliorer la qualité de notre service avez-vous des suggestions ?", "type": "texte", "categorie": "general", "groupe": "Event"},

    # Visiteur
    {"texte": "Pourquoi êtes-vous venu ?", "type": "texte", "categorie": "Motif", "groupe": "Visiteur"},
    {"texte": "Avez-vous été satisfait ?", "type": "oui_non", "categorie": "Satisfaction", "groupe": "Visiteur"},
    {"texte": "Donnez une note globale", "type": "etoiles", "categorie": "Note", "groupe": "Visiteur"},
]

# Supprimer les anciennes questions si nécessaire
def insert_questions():
    with app.app_context():
        Question.query.delete()
        db.session.commit()

        for q in questions:
            question = Question(**q)
            db.session.add(question)

        db.session.commit()
        print("✅ Questions insérées avec succès.")

# Ce bloc empêche l’exécution automatique lors d’un import
if __name__ == "__main__":
    insert_questions()