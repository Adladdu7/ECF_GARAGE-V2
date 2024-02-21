$(document).ready(function () {
  const footerToggle = document.querySelector('#footer-toggle');
  const footer = document.querySelector('footer');
  const arrow = document.querySelector('.arrow');
  const arrowIcon = document.querySelector('.arrow-icon');

  footerToggle.addEventListener('click', function () {
      footer.classList.toggle('hidden');
      arrow.classList.toggle('arrow-up');
      arrowIcon.classList.toggle('arrow-icon-up');
      updateArrowPosition(); // Appeler la fonction pour mettre à jour la position de la flèche
  });

  // Mettre à jour la position de la flèche en fonction de la visibilité du pied de page
  function updateArrowPosition() {
      const footerRect = footer.getBoundingClientRect();
      arrow.style.bottom = `${footerRect.height + 10}px`; // Ajuster l'espacement

      // Ajuster la position de la flèche si le pied de page est masqué
      if (footer.classList.contains('hidden')) {
          arrow.style.bottom = '20px'; // Définir la distance souhaitée par rapport au bas
      }
  }

  // Appeler la fonction initialement et lors du redimensionnement de la fenêtre
  updateArrowPosition();
  window.addEventListener('resize', updateArrowPosition);
});
