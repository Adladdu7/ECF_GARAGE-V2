$(document).ready(function () {
    // Fonction pour gérer l'ajout d'une voiture
    function gérerAjoutVoiture(event) {
        event.preventDefault(); // Empêcher le comportement de soumission par défaut du formulaire
        var formData = new FormData(this); // Créer un objet FormData à partir du formulaire

        $.ajax({
            url: '/ajouter_voiture', // Point de terminaison(endpoint) pour l'ajout d'une voiture
            type: 'POST',
            data: formData,
            processData: false, // Empêcher jQuery de traiter les données
            contentType: false, // Laisser le navigateur définir le type de contenu
            success: function (response) {
                console.log('Voiture ajoutée avec succès');
                $('#message-ajout-voiture').text(response.message); // Afficher le message de réussite
            },
            error: function (xhr, status, error) {
                console.log('Erreur lors de l\'ajout de la voiture :', error);
                $('#message-ajout-voiture').text('Erreur lors de l\'ajout de la voiture.'); // Afficher le message d'erreur
            }
        });
    }

    // Ajouter un écouteur d'événements pour la soumission du formulaire d'ajout de voiture
    $('#formulaireAjoutVoiture').submit(gérerAjoutVoiture);
});
