
/********************************JS  FORM*****************************************/
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
}

function highlightStars(rating) {
    stars.forEach((star, index) => {
        if (index < rating) {
            star.style.color = '#f39c12';
        } else {
            star.style.color = '#ddd';
        }
    });
}

function resetStars() {
    stars.forEach(star => {
        star.style.color = '#ddd';
        star.classList.remove('active');
    });
}

// === BARRES DE NOTATION AVEC COULEURS ===
function updateRatingValue(slider) {
    const valueSpan = slider.nextElementSibling;
    valueSpan.textContent = slider.value + '/10';
    
    // Calcul de la couleur dynamique
    const percentage = (slider.value - 1) / 9; // Normalisation 0-1
    const hue = percentage * 120; // De rouge (0) à vert (120)
    
    // Application de la couleur avec saturation et luminosité optimisées
    const color = `hsl(${hue}, 70%, 50%)`;
    valueSpan.style.background = color;
    
    // Animation de changement pour la note
    valueSpan.classList.add('changed');
    setTimeout(() => {
        valueSpan.classList.remove('changed');
    }, 300);
    
    // Mise à jour de la couleur de la barre elle-même avec dégradé dynamique
    const gradientColor = `hsl(${hue}, 60%, 60%)`;
    const trackColor = '#e9ecef';
    slider.style.background = `linear-gradient(to right, ${gradientColor} 0%, ${gradientColor} ${percentage * 100}%, ${trackColor} ${percentage * 100}%, ${trackColor} 100%)`;
    
    // Mise à jour de la couleur du curseur pour Chrome/Safari
    slider.style.setProperty('--webkit-slider-thumb-background', color);
    
    // Animation de la barre (même effet que la note)
    slider.classList.add('slider-changed');
    setTimeout(() => {
        slider.classList.remove('slider-changed');
    }, 300);
    
  
}




// Initialisation des couleurs au chargement
document.addEventListener('DOMContentLoaded', function() {
    // Initialiser les barres de notation
    const sliders = document.querySelectorAll('.rating-slider');
    sliders.forEach(slider => {
        updateRatingValue(slider);
    });
    
    // Animation d'entrée des cartes
    setTimeout(() => {
        document.querySelectorAll('.section-card').forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'all 0.5s ease';
            
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 150);
        });
    }, 100);
    

});

// === EFFETS VISUELS ADDITIONNELS ===
// Effet de survol sur les barres
document.querySelectorAll('.rating-slider').forEach(slider => {
    slider.addEventListener('mouseenter', function() {
        this.style.transform = 'scaleY(1.2)';
        this.style.transition = 'transform 0.2s ease';
    });
    
    slider.addEventListener('mouseleave', function() {
        this.style.transform = 'scaleY(1)';
    });
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

// Gestion de traduction améliorée
let currentLanguage = 'fr';

// Déclaration complète avec clé title
const translations = {
    fr: {
        title: "Votre Avis Compte"
    },
    en: {
        title: "Your Feedback Matters"
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
    document.getElementById('btn-fr')?.classList.remove('active');
    document.getElementById('btn-en')?.classList.remove('active');
    document.getElementById('btn-' + lang)?.classList.add('active');

    // Mettre à jour la langue HTML et le titre
    document.documentElement.lang = lang;
    const titleElement = document.getElementById('page-title');
    if (titleElement && translations[lang] && translations[lang].title) {
        titleElement.textContent = translations[lang].title;
    }

    // Mettre à jour la langue actuelle
    currentLanguage = lang;

    // Traduire les questions de la base de données
    translateDatabaseQuestions(lang);

    // Animation de transition
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

    // Notifier le changement de langue pour d'autres scripts
    if (typeof window.onLanguageChange === 'function') {
        window.onLanguageChange(lang);
    }
}

// Traduire les questions de la base de données
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

// Mettre à jour les questions dans le DOM
function updateQuestionsInDOM(translatedQuestions) {
    translatedQuestions.forEach(question => {
        const labelElement = document.querySelector(`label[data-question-id="${question.id}"]`);
        if (labelElement) {
            labelElement.textContent = question.texte;
        } else {
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

// Initialiser au chargement
document.addEventListener('DOMContentLoaded', function() {
    // Initialiser les placeholders
    const placeholderElements = document.querySelectorAll('[data-placeholder-fr]');
    placeholderElements.forEach(element => {
        const placeholder = element.getAttribute('data-placeholder-fr');
        if (placeholder) {
            element.setAttribute('placeholder', placeholder);
        }
    });

    // Marquer les labels pour traduction
    const questionLabels = document.querySelectorAll('label.form-label');
    questionLabels.forEach(label => {
        label.setAttribute('data-original-text', label.textContent);
    });

    // Animation
    document.body.style.transition = 'opacity 0.2s ease';

    // Initialiser la langue par défaut (facultatif)
    switchLanguage('fr');
});

// Débogage manuel
window.debugTranslations = function() {
    console.log('Langue actuelle:', currentLanguage);
    console.log('Questions avec data-question-id:', document.querySelectorAll('[data-question-id]').length);
    console.log('Labels de questions:', document.querySelectorAll('label.form-label').length);
};



//bouton fr et en 
 document.addEventListener('DOMContentLoaded', function () {
    // Connecte les boutons une fois que le JS est bien chargé
    document.getElementById('btn-fr').addEventListener('click', () => switchLanguage('fr'));
    document.getElementById('btn-en').addEventListener('click', () => switchLanguage('en'));
  });