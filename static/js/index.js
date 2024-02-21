$(document).ready(function () {

  // Définir la classe Vehicle
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

      // Méthode pour générer le HTML représentant le véhicule
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

  $.ajax({
      url: '/api/random_vehicle',
      method: 'GET',
      dataType: 'json',
      data: { count: 3 },
      success: function (vehiclesData) {
          const vehiclesListElement = $('#vehiclesList');
          const infoListElement = $('#infoList');

          const vehicles = vehiclesData.map(vehicleData => new Vehicle(...vehicleData));

          vehicles.forEach(vehicle => {
              const vehicleElement = $(vehicle.generateHTML());

              vehiclesListElement.append(vehicleElement);

              // Masquer les informations sur le véhicule initialement
              vehicleElement.find('.vehicle-info').hide();
          });

          $('.info-button').click(function () {
              const vehicleInfo = $(this).siblings('.vehicle-info');
              vehicleInfo.toggle();
              $('.vehicle-info').not(vehicleInfo).hide();

              if ($('.vehicle-info:visible').length > 0) {
                  $('#infoList').show();
              } else {
                  $('#infoList').hide();
              }
          });
      },
      error: function (error) {
          console.error('Erreur lors de la récupération des véhicules aléatoires :', error);
          // Gérer l'affichage de l'erreur ici
      }
  });

  const ratingInputs = document.querySelectorAll('.rating-input');
  const ratingValue = document.querySelector('#rating-value');

  ratingInputs.forEach(input => {
      input.addEventListener('click', function () {
          ratingValue.textContent = this.value;
      });
  });
});
