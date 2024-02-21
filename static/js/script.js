$(document).ready(function () {

    // Gérer la soumission du formulaire de contact
    $("#contactForm").submit(function (event) {
        event.preventDefault();

        // Débogage : Enregistrer les valeurs avant de créer formData

        var formData = {
            firstName: $("#firstName").val(),
            lastName: $("#lastName").val(),
            email: $("#email").val(),
            message: $("#message").val(),
            phone: $("#phone").val(),
            vehicleid: $("#searchInput").val()
        };

        console.log(formData)

        // Envoyer une requête AJAX de type POST
        $.ajax({
            type: "POST",
            url: "/api/contacts",
            data: JSON.stringify(formData),
            contentType: "application/json",
            success: function (response) {
                // Gérer le succès
                console.log($("#firstName").val());
                console.log($("#searchInput").val());
                afficherConfirmation("Message envoyé avec succès !");
                $("#firstName").val("");
                $("#lastName").val("");
                $("#email").val("");
                $("#phone").val("");
                $("#message").val("");
                $("#searchInput").val(""); // Effacer le véhicule sélectionné
            },
            error: function (error) {
                // Gérer l'erreur
                afficherConfirmation("Une erreur s'est produite lors de l'envoi du message.");
            }
        });
    });

    // Fonction pour afficher le message de confirmation
    function afficherConfirmation(message) {
        var confirmationDiv = $("#confirmation");
        confirmationDiv.text(message);
        confirmationDiv.fadeIn(300).delay(2000).fadeOut(400);
    }

});
