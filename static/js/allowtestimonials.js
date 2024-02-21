$(document).ready(function() {
    // Gérer la soumission des témoignages sélectionnés
    $("#submitSelectedTestimonials").on("click", function(event) {
        event.preventDefault();

        // Utiliser jQuery pour sélectionner toutes les cases à cocher cochées avec la classe "testimonial-checkbox"
        const témoignagesSélectionnés = $(".testimonial-checkbox:checked").map(function() {
            return $(this).val();
        }).get(); // Convertir l'objet jQuery en un tableau simple

        if (témoignagesSélectionnés.length > 0) {
            const formData = {
                témoignagesSélectionnés: témoignagesSélectionnés
            };

            $.ajax({
                type: "POST",
                url: "/soumettre_témoignages_sélectionnés",
                contentType: "application/json", // Définir le type de contenu sur JSON
                data: JSON.stringify(formData), // Convertir les données en une chaîne JSON
                success: function(response) {
                    // Gérer la réussite
                    console.log(response);
                    console.log("Témoignages sélectionnés soumis avec succès");
                    // Vous pouvez mettre à jour l'interface utilisateur ou afficher un message de réussite ici
                },
                error: function(xhr, status, error) {
                    // Gérer l'erreur
                    console.error("Erreur lors de la soumission des témoignages sélectionnés :", xhr.responseText);
                    // Vous pouvez mettre à jour l'interface utilisateur ou afficher un message d'erreur ici
                }
            });
        }
    });
});
