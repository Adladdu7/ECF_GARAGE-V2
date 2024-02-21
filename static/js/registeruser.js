$(document).ready(function() {
    // Lorsque le formulaire utilisateur est soumis
    $("#userForm").submit(function(event) {
        event.preventDefault(); // Empêcher la soumission par défaut du formulaire

        // Obtenir les données du formulaire
        var formData = {
            email: $("#email").val(),
            password: $("#password").val()
        };

        // Envoyer la requête AJAX à l'API
        $.ajax({
            type: "POST",
            url: "/register_employee",
            data: formData,
            success: function(response) {
                // Afficher le message de succès
                console.log(response)
                $("#success-message").text("Compte employé créé avec succès!");
                $("#error-message").empty();
            },
            error: function(xhr, status, error) {
                // Afficher le message d'erreur
                $("#error-message").text("Erreur lors de la création du compte employé : " + xhr.responseText);
                $("#success-message").empty();
            }
        });
    });

    // Lorsque le formulaire admin est soumis
    $("#adminForm").submit(function(event) {
        event.preventDefault(); // Empêcher la soumission par défaut du formulaire

        // Obtenir les données du formulaire
        var formData = {
            email: $("#email").val(),
            password: $("#password").val()
        };

        // Envoyer la requête AJAX à l'API
        $.ajax({
            type: "POST",
            url: "/register_admin",
            data: formData,
            success: function(response) {
                console.log(response)

                // Afficher le message de succès
                $("#success-message").text("Compte admin créé avec succès!");
                $("#error-message").empty();
            },
            error: function(xhr, status, error) {
                // Afficher le message d'erreur
                $("#error-message").text("Erreur lors de la création du compte admin : " + xhr.responseText);
                $("#success-message").empty();
            }
        });
    });
});
