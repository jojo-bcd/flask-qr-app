


//*********************************************js dasbaord event ************************************** */
/********************************JS  DASHBOARD — SANS CHAMBRES*****************************************/

document.addEventListener('DOMContentLoaded', () => {
  const elements = {
    totalAvis: document.getElementById('totalAvis'),
    highNotes: document.getElementById('highNotes'),
    midNotes: document.getElementById('midNotes'),
    lowNotes: document.getElementById('lowNotes'),
    avgHeb: document.getElementById('avgReunion'),
    avgRest: document.getElementById('avgRest'),
    generalResponses: document.getElementById('generalResponses'),
    commentaires: document.getElementById('commentaires'),
    applyFilters: document.getElementById('applyFilters'),
    useTestData: document.getElementById('useTestData'),
    startDate: document.getElementById('startDate'),
    endDate: document.getElementById('endDate'),
    debugInfo: document.getElementById('debugInfo')
  };

  let hebChart = null;
  let restChart = null;
  let avisData = [];

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

  initDates();
  processData(testData);
  updateDebugInfo("Données de test chargées");

  elements.applyFilters.addEventListener('click', fetchData);

  if (elements.useTestData) {
    elements.useTestData.addEventListener('click', () => {
      processData(testData);
      updateDebugInfo("Données de test rechargées");
    });
  }

  function initDates() {
    const today = new Date();
    const oneMonthAgo = new Date();
    oneMonthAgo.setMonth(today.getMonth() - 1);
    elements.startDate.valueAsDate = oneMonthAgo;
    elements.endDate.valueAsDate = today;
  }

  function updateDebugInfo(message) {
    if (elements.debugInfo) {
      elements.debugInfo.innerHTML = "<strong>Mode Debug:</strong> " + message;
    }
  }

  async function fetchData() {
    try {
      showLoading(true);
      updateDebugInfo("Chargement depuis l'API...");

      const params = new URLSearchParams({
        start: elements.startDate.value,
        end: elements.endDate.value
      });

      const response = await fetch(`/api/avis_event?${params}`);
      if (!response.ok) throw new Error(`Erreur HTTP: ${response.status}`);
      avisData = await response.json();
      processData(avisData);
      updateDebugInfo("Données API chargées: " + avisData.length + " avis");
    } catch (error) {
      console.error("Erreur fetch :", error);
      updateDebugInfo("Erreur API: " + error.message);
      processData(testData);
    } finally {
      showLoading(false);
    }
  }

  function processData(avis) {
    avisData = avis;
    updateCards(avis);
    const { hebData, restData } = processResponses(avis);
    updateCharts(hebData, restData);
    updateTextResponses(avis);
  }

  function updateCards(avis) {
    const total = avis.length;
    let high = 0, mid = 0, low = 0;
    avis.forEach(a => {
      if (a.note_globale >= 4) high++;
      else if (a.note_globale === 3) mid++;
      else low++;
    });

    elements.totalAvis.textContent = total;
    elements.highNotes.textContent = high;
    elements.midNotes.textContent = mid;
    elements.lowNotes.textContent = low;
  }

 function processResponses(avis) {
  const hebNotes = [], restNotes = [];
  const hebIds = [124, 125, 125, 126, 127, 128];
  const restIds = [129, 130, 131, 132, 133];

  avis.forEach(a => {
    if (typeof a.reponses !== 'object' || a.reponses === null) {
      console.warn("Données inattendues pour reponses:", a.reponses);
      return;
    }
    // Parcours toutes les catégories dans a.reponses (general, restauration, reunion, etc)
    Object.values(a.reponses).forEach(reponsesArray => {
      if (!Array.isArray(reponsesArray)) return;
      reponsesArray.forEach(r => {
        const note = parseFloat(r.reponse);
        if (isNaN(note)) return;
        if (hebIds.includes(r.question_id)) hebNotes.push(note);
        else if (restIds.includes(r.question_id)) restNotes.push(note);
      });
    });
  });

  return {
    hebData: calculateStats(hebNotes),
    restData: calculateStats(restNotes)
  };
}



  function calculateStats(notes) {
    const counts = [0, 0, 0];
    let total = 0;
    notes.forEach(n => {
      total += n;
      if (n <= 2) counts[0]++;
      else if (n === 3) counts[1]++;
      else counts[2]++;
    });

    return {
      counts: counts,
      average: notes.length ? (total / notes.length).toFixed(1) : 0
    };
  }

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

    const ctxHeb = document.getElementById('reunionChart');
    if (ctxHeb) {
      hebChart = new Chart(ctxHeb, {
        type: 'doughnut',
        data: {
          labels: doughnutLabels,
          datasets: [{ data: hebData.counts, backgroundColor: ['#ff4d4d', '#ffcc00', '#4CAF50'] }]
        },
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
        data: {
          labels: doughnutLabels,
          datasets: [{ data: restData.counts, backgroundColor: ['#ff4d4d', '#ffcc00', '#4CAF50'] }]
        },
        options: {
          ...chartOptions,
          onClick: (evt, el) => {
            if (el.length) afficherDetailsParNote('restauration', el[0].index, doughnutLabels[el[0].index]);
          }
        }
      });
    }
  }

  function afficherDetailsParNote(type, index, tranche) {
    const cardsContainer = document.getElementById('modalCardsContainer');
    const hebIds = [124, 125, 125, 126, 127, 128];
    const restIds = [129, 130, 131, 132, 133];
    const tranches = [[1, 2], [3, 3], [4, 5]];
    const [min, max] = tranches[index];

    cardsContainer.innerHTML = "";

   const results = avisData.flatMap(a =>
  Object.values(a.reponses || {}).flatMap(reponsesArray =>
    reponsesArray
      .filter(r => {
        const val = parseFloat(r.reponse);
        return !isNaN(val) && val >= min && val <= max &&
          ((type === 'hebergement' && hebIds.includes(r.question_id)) ||
           (type === 'restauration' && restIds.includes(r.question_id)));
      })
      .map(r => ({ question: r.question, reponse: r.reponse }))
  )
);


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

    const modal = new bootstrap.Modal(document.getElementById('popupModal'));
    modal.show();
  }

  const popupEl = document.getElementById('popupModal');
  popupEl.addEventListener('shown.bs.modal', () => {
    popupEl.removeAttribute('aria-hidden');
  });
  popupEl.addEventListener('hidden.bs.modal', () => {
    popupEl.setAttribute('aria-hidden', 'true');
  });

function updateTextResponses(avis) {
  elements.generalResponses.innerHTML = '';
  elements.commentaires.innerHTML = '';
  const textReps = [], comments = [];

  avis.forEach(a => {
    if (a.commentaire) comments.push(a.commentaire);
    if (typeof a.reponses === 'object' && a.reponses !== null) {
      Object.values(a.reponses).forEach(reponsesArray => {
        if (!Array.isArray(reponsesArray)) return;
        reponsesArray.forEach(r => {
          if (isNaN(parseFloat(r.reponse))) {
           textReps.push({
  question: r.question || "Question (non reconnue)",

  answer: r.reponse
});


          }
        });
      });
    }
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
