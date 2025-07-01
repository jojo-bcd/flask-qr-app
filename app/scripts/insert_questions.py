from app import create_app, db
from app.models import Question

app = create_app()

questions = [
    # Resident - Hébergement
    {"texte_fr": "Accueil à la réception", "texte_en": "Reception welcome", "type": "etoiles", "categorie": "Hébergement", "groupe": "Resident"},
    {"texte_fr": "Procédures d'enregistrement", "texte_en": "Check-in procedures", "type": "etoiles", "categorie": "Hébergement", "groupe": "Resident"},
    {"texte_fr": "Confort de la chambre", "texte_en": "Room comfort", "type": "etoiles", "categorie": "Hébergement", "groupe": "Resident"},
    {"texte_fr": "Propreté de la chambre", "texte_en": "Room cleanliness", "type": "etoiles", "categorie": "Hébergement", "groupe": "Resident"},
    {"texte_fr": "Service de portier-bagagiste", "texte_en": "Bellhop service", "type": "etoiles", "categorie": "Hébergement", "groupe": "Resident"},
    {"texte_fr": "Service de la piscine", "texte_en": "Swimming pool service", "type": "etoiles", "categorie": "Hébergement", "groupe": "Resident"},

    # Resident - Restauration
    {"texte_fr": "Service en salle à manger", "texte_en": "Dining room service", "type": "etoiles", "categorie": "Restauration", "groupe": "Resident"},
    {"texte_fr": "Service au bar", "texte_en": "Bar service", "type": "etoiles", "categorie": "Restauration", "groupe": "Resident"},
    {"texte_fr": "Service au Room Service", "texte_en": "Room service", "type": "etoiles", "categorie": "Restauration", "groupe": "Resident"},
    {"texte_fr": "Service en salle de conférence", "texte_en": "Conference room service", "type": "etoiles", "categorie": "Restauration", "groupe": "Resident"},
    {"texte_fr": "Ambiance", "texte_en": "Ambiance", "type": "etoiles", "categorie": "Restauration", "groupe": "Resident"},
    {"texte_fr": "Qualité de la nourriture", "texte_en": "Food quality", "type": "etoiles", "categorie": "Restauration", "groupe": "Resident"},
    {"texte_fr": "Choix de menus", "texte_en": "Menu choices", "type": "etoiles", "categorie": "Restauration", "groupe": "Resident"},
    {"texte_fr": "Rapport Qualité/Prix", "texte_en": "Value for money", "type": "etoiles", "categorie": "Restauration", "groupe": "Resident"},

    # Resident - Général
    {"texte_fr": "Qu'aurions-nous pu faire de plus pour rendre votre séjour encore plus agréable ?", "texte_en": "What could we have done to make your stay even more pleasant?", "type": "texte", "categorie": "Général", "groupe": "Resident"},
    {"texte_fr": "Pouvons-nous vous écrire afin de répondre à vos commentaires ?", "texte_en": "May we write to you to respond to your comments?", "type": "oui_non", "categorie": "Général", "groupe": "Resident"},

    # Event - Réunion
    {"texte_fr": "Avez-vous été bien accueilli par le service commercial ?", "texte_en": "Were you well received by the sales department?", "type": "etoiles", "categorie": "reunion", "groupe": "Event"},
    {"texte_fr": "Réactivité du service commercial dans l’organisation de votre réunion", "texte_en": "Responsiveness of the sales department in organizing your meeting", "type": "etoiles", "categorie": "reunion", "groupe": "Event"},
    {"texte_fr": "La salle de réunion était-elle bien équipée et confortable ?", "texte_en": "Was the meeting room well equipped and comfortable?", "type": "etoiles", "categorie": "reunion", "groupe": "Event"},
    {"texte_fr": "Avez-vous rencontré des problèmes techniques lors du séminaire ?", "texte_en": "Did you encounter technical problems during the seminar?", "type": "oui_non", "categorie": "reunion", "groupe": "Event"},
    {"texte_fr": "Comment avez-vous trouvé le service en salle de réunion ?", "texte_en": "How did you find the meeting room service?", "type": "etoiles", "categorie": "reunion", "groupe": "Event"},

    # Event - Restauration
    {"texte_fr": "Comment avez-vous trouvé le service au restaurant ?", "texte_en": "How did you find the restaurant service?", "type": "etoiles", "categorie": "restauration", "groupe": "Event"},
    {"texte_fr": "Avez-vous été servi à temps ?", "texte_en": "Were you served on time?", "type": "etoiles", "categorie": "restauration", "groupe": "Event"},
    {"texte_fr": "Comment avez-vous trouvé la qualité des plats servis lors de votre séminaire ?", "texte_en": "How did you find the quality of dishes served during your seminar?", "type": "etoiles", "categorie": "restauration", "groupe": "Event"},
    {"texte_fr": "Comment avez-vous trouvé la qualité des pauses café ?", "texte_en": "How did you find the quality of coffee breaks?", "type": "etoiles", "categorie": "restauration", "groupe": "Event"},
    {"texte_fr": "Souhaitez-vous revenir pour un autre séminaire ?", "texte_en": "Would you like to come back for another seminar?", "type": "oui_non", "categorie": "restauration", "groupe": "Event"},

    # Event - Général
    {"texte_fr": "Au cours de votre séminaire avez-vous rencontré d’autres difficultés non signalées ?", "texte_en": "During your seminar, did you encounter any other unreported difficulties?", "type": "texte", "categorie": "general", "groupe": "Event"},
    {"texte_fr": "Pour améliorer la qualité de notre service avez-vous des suggestions ?", "texte_en": "To improve our service quality, do you have any suggestions?", "type": "texte", "categorie": "general", "groupe": "Event"},

    # Visiteur
    {"texte_fr": "Pourquoi êtes-vous venu ?", "texte_en": "Why did you come?", "type": "texte", "categorie": "Motif", "groupe": "Visiteur"},
    {"texte_fr": "Avez-vous été satisfait ?", "texte_en": "Were you satisfied?", "type": "oui_non", "categorie": "Satisfaction", "groupe": "Visiteur"},
    {"texte_fr": "Donnez une note globale", "texte_en": "Give an overall rating", "type": "etoiles", "categorie": "Note", "groupe": "Visiteur"},
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