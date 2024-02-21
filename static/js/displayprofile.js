$(document).ready(function () {
    // Ferme toutes les sections au chargement de la page
    $('.section-content').hide();

    // Gestionnaire d'événements pour les titres h3 dans les sections
    $('h3').click(function () {
        var sectionContent = $(this).next('.section-content');
        sectionContent.slideToggle();
        $('.section-content').not(sectionContent).slideUp();
    });

});
