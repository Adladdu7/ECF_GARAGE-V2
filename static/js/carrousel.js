// Sélectionner tous les éléments de témoignage
const testimonials = document.querySelectorAll('.testimonial-slide');

// Sélectionner le bouton précédent et le bouton suivant
const prevButton = document.getElementById('prev-slide');
const nextButton = document.getElementById('next-slide');

// Nombre de témoignages à afficher par page
const testimonialsPerPage = 2;

// Index du témoignage actuellement affiché
let currentIndex = 0;

// Fonction pour afficher les témoignages appropriés
function showTestimonials() {
    testimonials.forEach((testimonial, index) => {
        if (index >= currentIndex && index < currentIndex + testimonialsPerPage) {
            // Afficher le témoignage
            testimonial.style.display = 'block';
        } else {
            // Masquer le témoignage
            testimonial.style.display = 'none';
        }
    });
}

// Gérer le clic sur le bouton précédent
prevButton.addEventListener('click', () => {
    if (currentIndex > 0) {
        // Décrémenter l'index pour afficher les témoignages précédents
        currentIndex -= testimonialsPerPage;
        showTestimonials();
    }
});

// Gérer le clic sur le bouton suivant
nextButton.addEventListener('click', () => {
    if (currentIndex + testimonialsPerPage < testimonials.length) {
        // Incrémenter l'index pour afficher les témoignages suivants
        currentIndex += testimonialsPerPage;
        showTestimonials();
    }
});

// Afficher les témoignages au chargement de la page
showTestimonials();
