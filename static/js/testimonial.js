$(document).ready(function() {
    // Lorsque le formulaire de témoignage est soumis
    $("#testimonialForm").submit(function(event) {
        event.preventDefault(); // Empêcher la soumission par défaut du formulaire

        // Effacer les messages précédents
        $("#message").empty();

        // Obtenir les données du formulaire
        var formData = {
            name: $("#name").val(),
            comment: $("#comment").val(),
            rating: $("input[name='rating']:checked").val()
        };

        // Envoyer la requête AJAX à l'API
        $.ajax({
            type: "POST",
            url: "/submit_testimonial", // Mettre à jour avec votre route d'API Flask
            data: formData,
            success: function(response) {
                // Afficher le message de succès
                $("#message").text("Témoignage ajouté avec succès !");
            },
            error: function(xhr, status, error) {
                // Afficher le message d'erreur
                $("#message").text("Erreur lors de l'ajout du témoignage : " + xhr.responseText);
            }
        });
    });
});
