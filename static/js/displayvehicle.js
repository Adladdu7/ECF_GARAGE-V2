// Classe représentant un véhicule
class Vehicle {
    constructor(make, model, price, year, kilometers, id, img) {
        this.make = make;
        this.model = model;
        this.price = price;
        this.year = year;
        this.kilometers = kilometers;
        this.id = id;
        this.img = img;

    }

    // Méthode pour générer le HTML représentant le véhicule
    generateHTML() {
        return `
            <div class="vehicle">
                <h2>${this.make} ${this.model}</h2>
                <p>Prix : ${this.price}€</p>
                <p>Année : ${this.year}</p>
                <p>Kilométrage : ${this.kilometers} km</p>
                <p>Références : ${this.id}</p>
                <img src="${this.img}" alt="${this.make} ${this.model}" data-vehicle-id="${this.id}">
            </div>
        `;
    }
    
}

// Classe pour gérer les opérations liées aux véhicules
class VehicleManager {
    constructor() {
        this.vehiclesListElement = $('#vehiclesList');
        this.infoListElement = $('#infoList');
        console.log(this.vehiclesListElement)
    }

    // Méthode pour charger les véhicules via AJAX
    loadVehicles() {
    $.ajax({
        url: '/api/vehicles',
        type: 'GET',
        dataType: 'json',  // Ajoutez cette ligne pour indiquer que la réponse est au format JSON
        success: (data) => {
            this.displayVehicles(data);
        },
        error: (xhr, status, error) => {
            console.log('Erreur lors du chargement des véhicules :', error);
        }
    });
    }

    // Méthode pour filtrer les véhicules via AJAX
    filterVehicles(event) {
        event.preventDefault();
        const formData = $('#filterForm').serialize();
        $.ajax({
            url: '/api/filter_vehicles',
            type: 'POST',
            data: formData,
            success: (data) => {
                this.displayVehicles(data);
            },
            error: (xhr, status, error) => {
                console.log('Erreur lors du filtrage des véhicules :', error);
            }
        });
    }

    // Méthode pour afficher les véhicules dans le DOM
    displayVehicles(data) {
    this.vehiclesListElement.empty();

    if (data.length > 0) {
        this.vehiclesListElement.show();

        data.forEach((vehicleData) => {
            const vehicle = new Vehicle(vehicleData.make, vehicleData.model, vehicleData.price, vehicleData.year, vehicleData.kilometers, vehicleData.id, vehicleData.img);
            const listItem = $(vehicle.generateHTML());
            this.vehiclesListElement.append(listItem);
        });
    } else {
        this.vehiclesListElement.hide();
    }
    }


    // Méthode pour masquer la liste d'informations
    hideInfoList() {
        this.infoListElement.hide();
    }

    // Méthode pour gérer le clic sur le bouton d'informations
    handleInfoButtonClick() {
        const vehicleInfo = $(this).siblings('.vehicle-info');
        vehicleInfo.toggle();

        $('.vehicle-info').not(vehicleInfo).hide();

        if ($('.vehicle-info:visible').length > 0) {
            this.infoListElement.show();
        } else {
            this.infoListElement.hide();
        }
    }
}

// Instance de la classe VehicleManager
const vehicleManager = new VehicleManager();

// Charger les véhicules lors du chargement de la page
vehicleManager.loadVehicles();

// Ajouter un écouteur d'événements pour la soumission du formulaire de filtrage
$('#filterForm').submit((event) => {
    vehicleManager.filterVehicles(event);
});

// Masquer initialement la liste d'informations
vehicleManager.hideInfoList();

// Gérer le clic sur le bouton d'informations
$('.info-button').click(function () {
    vehicleManager.handleInfoButtonClick.call(this);
});
