/********************************JS  DASBOARD*****************************************/

// dashboard_updated.js — version complète avec clic graphique + affichage des cartes
// Attend que le DOM soit complètement chargé


document.addEventListener('DOMContentLoaded', () => {

async function fetchRooms() {
  try {
    const response = await fetch('/api/chambres');
    if (!response.ok) throw new Error("Erreur lors du chargement des chambres");
    const rooms = await response.json();
    loadRooms(rooms);
    updateDebugInfo(`Chambres chargées: ${rooms.length}`);
  } catch (error) {
    console.error("Erreur fetch chambres :", error);
    updateDebugInfo("Erreur lors du chargement des chambres");
  }
}
  // Récupère les éléments HTML utilisés dans le script
  const elements = {
    totalAvis: document.getElementById('totalAvis'),
    highNotes: document.getElementById('highNotes'),
    midNotes: document.getElementById('midNotes'),
    lowNotes: document.getElementById('lowNotes'),
    avgHeb: document.getElementById('avgHeb'),
    avgRest: document.getElementById('avgRest'),
    generalResponses: document.getElementById('generalResponses'),
    commentaires: document.getElementById('commentaires'),
    applyFilters: document.getElementById('applyFilters'),
    useTestData: document.getElementById('useTestData'),
    startDate: document.getElementById('startDate'),
    endDate: document.getElementById('endDate'),
    //timeFilter: document.getElementById('timeFilter'),
    roomNumberFilter: document.getElementById('roomNumberFilter'),
    debugInfo: document.getElementById('debugInfo')
  };

  // Références aux graphiques (chart.js)
  let hebChart = null;
  let restChart = null;
  let avisData = [];

  // Données de test utilisées en fallback ou pour démo
  const testData = [{
    note_globale: 9,
    commentaire: "Excellent séjour",
    reponses: [
      { question_id: 29, question: { text: "Comment évaluez-vous l'hébergement ?" }, reponse: "8" },
      { question_id: 34, question: { text: "Comment évaluez-vous la restauration ?" }, reponse: "9" },
      { question_id: 100, question: { text: "Que pensez-vous de l'accueil ?" }, reponse: "Très bon accueil" }
    ]
  },
  {
    note_globale: 4,
    commentaire: "Décevant",
    reponses: [
      { question_id: 29, question: { text: "Comment évaluez-vous l'hébergement ?" }, reponse: "3" },
      { question_id: 34, question: { text: "Comment évaluez-vous la restauration ?" }, reponse: "4" }
    ]
  }];

  // Initialise la période de filtre à "1 mois"
  initDates();



  // Charge et affiche les données de test par défaut
  processData(testData);

    // 👇👇 AJOUTE CETTE LIGNE ICI 👇👇
  fetchRooms();

  updateDebugInfo("Données de test chargées");

    
  // Bouton "Appliquer les filtres"
  elements.applyFilters.addEventListener('click', fetchData);

  // Si bouton "Données de test" existe, ajouter comportement
  if (elements.useTestData) {
    elements.useTestData.addEventListener('click', () => {
      processData(testData);
      updateDebugInfo("Données de test rechargées");
    });
  }

  // Initialise les dates de filtre à la période actuelle
  function initDates() {
    const today = new Date();
    const oneMonthAgo = new Date();
    oneMonthAgo.setMonth(today.getMonth() - 1);
    elements.startDate.valueAsDate = oneMonthAgo;
    elements.endDate.valueAsDate = today;
  }

function loadRooms(rooms) {
  const roomSelect = document.getElementById('roomNumberFilter');
  if (!roomSelect) {
    console.warn("roomNumberFilter non trouvé dans le DOM");
    return;
  }

  rooms.forEach(room => {
    const option = document.createElement('option');
    option.value = room.nom; // car tu utilises chambre.nom
    option.textContent = room.nom;
    roomSelect.appendChild(option);
  });
}
  // Affiche les messages dans la section "debug"
  function updateDebugInfo(message) {
    if (elements.debugInfo) {
      elements.debugInfo.innerHTML = "<strong>Mode Debug:</strong> " + message;
    }
  }

  // Récupère les avis depuis l’API avec filtres
  async function fetchData() {
    try {
      showLoading(true);
      updateDebugInfo("Chargement depuis l'API...");
      const params = new URLSearchParams({
  start: elements.startDate.value,
  end: elements.endDate.value,
 // period: elements.timeFilter.value,
  chambre: elements.roomNumberFilter.value  // <- ligne ajoutée
});

      const response = await fetch(`/api/avis?${params}`);
      if (!response.ok) throw new Error(`Erreur HTTP: ${response.status}`);
      avisData = await response.json();
      processData(avisData);
      updateDebugInfo("Données API chargées: " + avisData.length + " avis");
    } catch (error) {
      console.error("Erreur fetch :", error);
      updateDebugInfo("Erreur API: " + error.message);
      processData(testData);  // fallback
    } finally {
      showLoading(false);
    }
  }

  // Met à jour toutes les vues à partir des données chargées
  function processData(avis) {
    avisData = avis;
    updateCards(avis);
    const { hebData, restData } = processResponses(avis);
    updateCharts(hebData, restData);
    updateTextResponses(avis);
  }

  // Met à jour les cartes statistiques (totaux, bons/mauvais avis)
  function updateCards(avis) {
    const total = avis.length;
    let high = 0, mid = 0, low = 0;
    avis.forEach(a => {
  if (a.note_globale >= 4) high++;       // 4 ou 5 = élevé
  else if (a.note_globale === 3) mid++;  // 3 = moyen
  else low++;                            // 1 ou 2 = faible
});

    
    elements.totalAvis.textContent = total;
    elements.highNotes.textContent = high;
    elements.midNotes.textContent = mid;
    elements.lowNotes.textContent = low;
  }

  // Sépare les réponses hébergement et restauration + prépare stats
  function processResponses(avis) {
    const hebNotes = [], restNotes = [];
    const hebIds = [108, 109, 110, 111, 112, 113];  // ID des questions hébergement
    const restIds = [114, 115, 116, 117, 118, 119, 120, 121];  // ID des questions restauration

    avis.forEach(a => {
      a.reponses.forEach(r => {
        const note = parseFloat(r.reponse);
        if (isNaN(note)) return;
        if (hebIds.includes(r.question_id)) hebNotes.push(note);
        else if (restIds.includes(r.question_id)) restNotes.push(note);
      });
    });

    return {
      hebData: calculateStats(hebNotes),
      restData: calculateStats(restNotes)
    };
  }

  // Calcule les moyennes et répartitions pour les notes
  function calculateStats(notes) {
    const counts = [0, 0, 0];
    let total = 0;
    notes.forEach(n => {
  total += n;
  if (n <= 2) counts[0]++;    // Faible (1-2)
  else if (n === 3) counts[1]++;  // Moyen (3)
  else counts[2]++;            // Élevé (4-5)
});

    return {
      counts: counts,
      average: notes.length ? (total / notes.length).toFixed(1) : 0
    };
  }

  // Met à jour les graphiques donuts avec Chart.js
  function updateCharts(hebData, restData) {
    elements.avgHeb.textContent = hebData.average;
    elements.avgRest.textContent = restData.average;
    if (hebChart) hebChart.destroy();
    if (restChart) restChart.destroy();

    const chartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: 'bottom' } }
    };
    const doughnutLabels = ['Faible (1-2)', 'Moyen (3)', 'Élevé (4-5)'];


    const ctxHeb = document.getElementById('hebergementChart');
    if (ctxHeb) {
      hebChart = new Chart(ctxHeb, {
        type: 'doughnut',
        data: { labels: doughnutLabels, datasets: [{ data: hebData.counts, backgroundColor: ['#ff4d4d', '#ffcc00', '#4CAF50'] }] },
        options: {
          ...chartOptions,
          onClick: (evt, el) => {
            if (el.length) afficherDetailsParNote('hebergement', el[0].index, doughnutLabels[el[0].index]);
          }
        }
      });
    }

    const ctxRest = document.getElementById('restaurationChart');
    if (ctxRest) {
      restChart = new Chart(ctxRest, {
        type: 'doughnut',
        data: { labels: doughnutLabels, datasets: [{ data: restData.counts, backgroundColor: ['#ff4d4d', '#ffcc00', '#4CAF50'] }] },
        options: {
          ...chartOptions,
          onClick: (evt, el) => {
            if (el.length) afficherDetailsParNote('restauration', el[0].index, doughnutLabels[el[0].index]);
          }
        }
      });
    }
  }

  // Affiche les réponses détaillées dans une modale Bootstrap selon la tranche cliquée
function afficherDetailsParNote(type, index, tranche) {
  const cardsContainer = document.getElementById('modalCardsContainer');
  const hebIds = [108, 109, 110, 111, 112, 113];  // ID des questions hébergement
  const restIds = [114, 115, 116, 117, 118, 119, 120, 121];  // ID des questions restauration

  const tranches = [
    [1, 2],  // Faible
    [3, 3],  // Moyen
    [4, 5]   // Élevé
  ];
  const [min, max] = tranches[index];

  cardsContainer.innerHTML = "";

  const results = avisData.flatMap(a =>
    a.reponses.filter(r => {
      const val = parseFloat(r.reponse);
      const valid = !isNaN(val) && val >= min && val <= max;

      console.log("Question :", r.question?.text, " | Valeur brute :", r.reponse, " | Numérique :", val);

      return valid && (
        (type === 'hebergement' && hebIds.includes(r.question_id)) ||
        (type === 'restauration' && restIds.includes(r.question_id))
      );
    }).map(r => ({ question: r.question.text, reponse: r.reponse }))
  );

  console.log("🟢 Résultats filtrés :", results);

  if (!results.length) {
    cardsContainer.innerHTML = "<p>Aucune réponse trouvée.</p>";
  } else {
    results.forEach(r => {
      const card = document.createElement("div");
      card.className = "col-md-4 mb-3";
      card.innerHTML = `
        <div class="card h-100">
          <div class="card-body">
            <h5 class="card-title">${r.question}</h5>
            <p class="card-text">${r.reponse}</p>
          </div>
        </div>`;
      cardsContainer.appendChild(card);
    });
  }

  // ✅ Affiche correctement la modale via Bootstrap
  const modal = new bootstrap.Modal(document.getElementById('popupModal'));
  modal.show();
}

// ✅ Événements pour s'assurer qu'on gère bien aria-hidden (accessibilité)
const popupEl = document.getElementById('popupModal');

popupEl.addEventListener('shown.bs.modal', function () {
  popupEl.removeAttribute('aria-hidden');
});

popupEl.addEventListener('hidden.bs.modal', function () {
  popupEl.setAttribute('aria-hidden', 'true');
});

// Affiche les réponses de type texte + commentaires
function updateTextResponses(avis) {
  elements.generalResponses.innerHTML = '';
  elements.commentaires.innerHTML = '';
  const textReps = [], comments = [];
  avis.forEach(a => {
    if (a.commentaire) comments.push(a.commentaire);
    a.reponses.forEach(r => {
      if (isNaN(parseFloat(r.reponse))) {
        textReps.push({ question: r.question.text, answer: r.reponse });
      }
    });
  });
  textReps.forEach(r => {
    const li = document.createElement('li');
    li.innerHTML = `<strong>${r.question}:</strong> ${r.answer}`;
    elements.generalResponses.appendChild(li);
  });
  comments.forEach(c => {
    const li = document.createElement('li');
    li.textContent = c;
    elements.commentaires.appendChild(li);
  });
}

// Affiche ou masque le message de chargement
function showLoading(show) {
  const existing = document.querySelector('.loading');
  if (existing) existing.remove();
  if (show) {
    const loader = document.createElement('div');
    loader.className = 'loading';
    loader.textContent = 'Chargement des données...';
    document.querySelector('.dashboard-container').appendChild(loader);
  }
}
});


