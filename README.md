# Garage V. Parrot - Application Web

Bienvenue dans l'application web du Garage V. Parrot. Cette application a été développée pour gérer les véhicules en vente, les services proposés, et permettre aux utilisateurs de témoigner de leur expérience.

## Prérequis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre système :

- [Python](https://www.python.org/downloads/windows/) (version 3.6 ou supérieure)
- [MySQL](https://dev.mysql.com/downloads/installer/)

## Installation

1. Clonez ce dépôt GitHub sur votre machine locale en utilisant [Git Bash](https://gitforwindows.org/) :
   
git clone [https://github.com/Adladdu7/ECF_GARAGE](https://github.com/Adladdu7/ECF_GARAGE.git)https://github.com/Adladdu7/ECF_GARAGE.git

(Si vous avez l'habitude d'utiliser le CMD Windows vous pouvez procéder comme a votre habitude)

2. Accédez au répertoire du projet en utilisant Git Bash :
   
cd Garage-Parrot-Web

3. Créez un environnement virtuel (recommandé) en utilisant Git Bash :

python -m venv venv

4. Activez l'environnement virtuel en utilisant Git Bash :
   
venv\Scripts\activate

5. Installez les dépendances du projet à partir du fichier `requirements.txt` en utilisant Git Bash :

pip install -r requirements.txt


6. Configurez la base de données MySQL en créant une base de données et en mettant à jour les informations de connexion dans le fichier `api.py`. ( un fichier config a part est  avenir )

7. Executer les requête sql contenu dans sql.txt afin de crée les tables de base de données.
   
8. Lancez l'application web en utilisant Bash :
   
   python api.py

9. Accédez à l'application depuis votre navigateur en vous rendant à l'adresse `http://localhost:5000`.

10. Afin d'initialiser le Super Admin vous pourrez accéder à l'adresse `http://localhost:5000/install_super_admin` vous pourrez ainsi créer les utilisateur sans avoir a saisir des requête sql 
    
## Utilisation

L'application est désormais en cours d'exécution sur votre machine Windows. Vous pouvez explorer les fonctionnalités suivantes :

- Voir les véhicules en vente.
- Ajouter, modifier ou supprimer des véhicules.
- Gérer les services proposés par le garage.
- Laisser un témoignage sur votre expérience au Garage V. Parrot.


##Documentation

Vous trouverez également la charte graphique ainsi que la documentation technique dans le dossier "Documents".




