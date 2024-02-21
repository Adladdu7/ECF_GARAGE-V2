$(document).ready(function () {

    class Vehicle {
        constructor(reference, brand, model, price, year, mileage, image) {
            this.reference = reference;
            this.brand = brand;
            this.model = model;
            this.price = price;
            this.year = year;
            this.mileage = mileage;
            this.image = image;
        }

        generateHTML() {
            return `
                <div class="vehicle">
                    <img src="${this.image}" alt="${this.brand} ${this.model}">
                    <button class="info-button">Infos</button>
                    <div class="vehicle-info">
                        <h3>${this.brand} ${this.model}</h3>
                        <p>Marque : ${this.brand}</p>
                        <p>Modèle : ${this.model}</p>
                        <p>Prix : ${this.price}</p>
                        <p>Année : ${this.year}</p>
                        <p>Kilométrage : ${this.mileage}</p>
                        <p>Référence : ${this.reference}</p>
                    </div>
                </div>
            `;
        }
    }

    const searchInput = $("#searchInput");
    const searchResults = $("#searchResults");

    // Masquer initialement le conteneur searchResults
    searchResults.hide();

    searchInput.on("input", function () {
        const searchTerm = searchInput.val();

        if (searchTerm.trim() !== "") {
            console.log("Envoi d'une requête AJAX pour le terme de recherche :", searchTerm);
            // Effectuer une requête AJAX vers le serveur pour obtenir des résultats filtrés
            $.ajax({
                url: "/api/filter_vehicles",
                method: "POST",
                data: { ref: searchTerm },
                success: function (data) {
                    console.log("Données récupérées avec succès :", data);
                    searchResults.empty();

                    if (data.length > 0) {
                        searchResults.show(); // Afficher le conteneur des résultats de recherche

                        data.forEach(function (vehicleData) {
                            const vehicle = new Vehicle(...vehicleData);
                            const listItem = $(vehicle.generateHTML());
                            searchResults.append(listItem);
                        });
                    } else {
                        // Masquer le conteneur des résultats de recherche en l'absence de résultats de recherche
                        searchResults.hide();
                    }
                },
                error: function (xhr, status, error) {
                    console.log('Erreur lors du filtrage des véhicules :', error);
                }
            });
        } else {
            // Masquer le conteneur des résultats de recherche lorsque la recherche est vide
            searchResults.hide();
        }
    });
});
