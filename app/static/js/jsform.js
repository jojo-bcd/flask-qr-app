//********************************JS  FORM*****************************************

document.addEventListener('DOMContentLoaded', () => {
  // === GESTION DES ÉTOILES ===
  const stars = document.querySelectorAll('.star-rating label');
  const starInputs = document.querySelectorAll('.star-rating input');

  stars.forEach((star, index) => {
    star.addEventListener('click', () => {
      updateStars(index + 1);
    });

    star.addEventListener('mouseover', () => {
      highlightStars(index + 1);
    });
  });

  document.querySelector('.star-rating').addEventListener('mouseleave', () => {
    const checkedStar = document.querySelector('.star-rating input:checked');
    if (checkedStar) {
      updateStars(parseInt(checkedStar.value));
    } else {
      resetStars();
    }
  });

  function updateStars(rating) {
    stars.forEach((star, index) => {
      if (index < rating) {
        star.classList.add('active');
        star.style.color = '#f39c12';
      } else {
        star.classList.remove('active');
        star.style.color = '#ddd';
      }
    });

    // ✅ Envoie la note correcte dans le formulaire
    starInputs[rating - 1].checked = true;
  }

  function highlightStars(rating) {
    stars.forEach((star, index) => {
      star.style.color = index < rating ? '#f39c12' : '#ddd';
    });
  }

  function resetStars() {
    stars.forEach(star => {
      star.style.color = '#ddd';
      star.classList.remove('active');
    });
  }
});


// Validation du formulaire avant soumission
document.getElementById('reviewForm').addEventListener('submit', function(e) {
    const requiredFields = this.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (field.type === 'radio') {
            const groupName = field.name;
            if (!this.querySelector(`[name="${groupName}"]:checked`)) {
                isValid = false;
            }
        } else if (field.value.trim() === '') {
            isValid = false;
        }
    });
    
    if (!isValid) {
        e.preventDefault();
        alert('Veuillez remplir tous les champs obligatoires.');
        return false;
    }
    
    // Animation du bouton de soumission
    const submitBtn = this.querySelector('.submit-btn');
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Envoi en cours...';
    submitBtn.disabled = true;
});


//gestion de traduction 
// Gestion de traduction améliorée
let currentLanguage = 'fr';

const translations = {
    fr: {
        title: 'Votre Avis Compte'
    },
    en: {
        title: 'Your Account Review'
    }
};

function switchLanguage(lang) {
    // Mettre à jour tous les textes avec data-attributes
    const langElements = document.querySelectorAll('.lang-text');
    langElements.forEach(element => {
        const text = element.getAttribute('data-' + lang);
        if (text) {
            element.textContent = text;
        }
    });

    // Mettre à jour les placeholders
    const placeholderElements = document.querySelectorAll('[data-placeholder-' + lang + ']');
    placeholderElements.forEach(element => {
        const placeholder = element.getAttribute('data-placeholder-' + lang);
        if (placeholder) {
            element.setAttribute('placeholder', placeholder);
        }
    });

    // Mettre à jour les boutons de langue
    document.getElementById('btn-fr').classList.remove('active');
    document.getElementById('btn-en').classList.remove('active');
    document.getElementById('btn-' + lang).classList.add('active');

    // Mettre à jour la langue HTML et le titre
    document.documentElement.lang = lang;
    document.getElementById('page-title').textContent = translations[lang].title;

    // Mettre à jour la langue actuelle
    currentLanguage = lang;

    // NOUVEAU: Traduire les questions de la base de données
    translateDatabaseQuestions(lang);

    // Animation de transition légère
    document.body.style.opacity = '0.95';
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);

    // Sauvegarder la langue dans la session
    fetch('/set_language', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ language: lang })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('Langue sauvegardée:', lang);
        }
    })
    .catch(error => {
        console.error('Erreur lors de la sauvegarde de la langue:', error);
    });

    // Notifier le changement de langue pour les scripts externes
    if (typeof window.onLanguageChange === 'function') {
        window.onLanguageChange(lang);
    }
}

// NOUVELLE FONCTION: Traduire les questions de la base de données
function translateDatabaseQuestions(lang) {
    fetch(`/get_translated_questions?language=${lang}`)
        .then(response => response.json())
        .then(data => {
            updateQuestionsInDOM(data.questions);
        })
        .catch(error => {
            console.error('Erreur lors de la récupération des questions traduites:', error);
        });
}

// NOUVELLE FONCTION: Mettre à jour les questions dans le DOM
function updateQuestionsInDOM(translatedQuestions) {
    translatedQuestions.forEach(question => {
        // Trouver l'élément label correspondant à cette question
        const labelElement = document.querySelector(`label[data-question-id="${question.id}"]`);
        if (labelElement) {
            labelElement.textContent = question.texte;
        } else {
            // Si pas de data-question-id, essayer de trouver par le texte original
            // (méthode de fallback)
            const labels = document.querySelectorAll('label.form-label');
            labels.forEach(label => {
                if (label.getAttribute('data-original-text') === question.texte_original) {
                    label.textContent = question.texte;
                }
            });
        }
    });
}

// Fonction pour exposer la langue actuelle
window.getCurrentLanguage = () => currentLanguage;

// Initialiser les placeholders et questions au chargement
document.addEventListener('DOMContentLoaded', function() {
    // Initialiser les placeholders
    const placeholderElements = document.querySelectorAll('[data-placeholder-fr]');
    placeholderElements.forEach(element => {
        const placeholder = element.getAttribute('data-placeholder-fr');
        if (placeholder) {
            element.setAttribute('placeholder', placeholder);
        }
    });

    // Ajouter des attributs pour identifier les questions
    const questionLabels = document.querySelectorAll('label.form-label');
    questionLabels.forEach((label, index) => {
        // Sauvegarder le texte original pour pouvoir le retrouver
        label.setAttribute('data-original-text', label.textContent);
    });

    // Animation d'entrée
    document.body.style.transition = 'opacity 0.2s ease';
});

// Fonction utilitaire pour déboguer
window.debugTranslations = function() {
    console.log('Langue actuelle:', currentLanguage);
    console.log('Questions avec data-question-id:', document.querySelectorAll('[data-question-id]').length);
    console.log('Labels de questions:', document.querySelectorAll('label.form-label').length);
};



// Affiche la modale de contact si on clique sur "Oui"
document.addEventListener('DOMContentLoaded', () => {
  const boutonsOui = document.querySelectorAll('.btn-check.btn-oui');
  const validerBtn = document.getElementById('validerContact');

  // Quand on clique sur "Oui", ouvrir la modale
  boutonsOui.forEach(bouton => {
    bouton.addEventListener('change', () => {
      const modalElement = document.getElementById('contactModal');
      if (modalElement) {
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
      }
    });
  });

  // Quand on clique sur "Valider", vérifier les champs
  if (validerBtn) {
    validerBtn.addEventListener('click', () => {
      const nom = document.getElementById('client_nom').value.trim();
      const email = document.getElementById('client_email').value.trim();
      const tel = document.getElementById('client_tel').value.trim();

      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

      if (!nom || !email || !tel) {
        alert("🚨 Veuillez remplir tous les champs.");
        return;
      }

      if (!emailRegex.test(email)) {
        alert("📧 L'adresse email saisie n'est pas valide.");
        return;
      }

      // Copier les données dans les champs cachés du formulaire principal
      document.getElementById('hidden_client_nom').value = nom;
      document.getElementById('hidden_client_email').value = email;
      document.getElementById('hidden_client_tel').value = tel;

      // Fermer la modale
      const modalElement = document.getElementById('contactModal');
      const modalInstance = bootstrap.Modal.getInstance(modalElement);
      modalInstance.hide();
    });
  }
});
