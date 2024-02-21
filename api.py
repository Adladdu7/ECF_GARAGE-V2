from flask import Flask, render_template, jsonify, request, session
from werkzeug.utils import secure_filename
from flaskext.mysql import MySQL  # Importer l'extension MySQL
import bcrypt  # Importer la bibliothèque bcrypt
from flask_bcrypt import Bcrypt  # Importer l'extension Bcrypt
from forms  import LoginForm
import json  # Importer le module json

import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = os.urandom(24)

bcrypt = Bcrypt(app)  # Initialiser Bcrypt avec votre application Flask

# Se connecter à la base de données MySQL
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'test'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

UPLOAD_FOLDER = 'static/images'  # Changez ceci pour le dossier où vous souhaitez stocker les images téléchargées
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Page d'accueil
@app.route('/')
def index():
    role = session.get('role')
    token = session.get('email') is not None
    get_allowed_testimonials()
    print(testimonials)

    return render_template('index.html', user_is_authenticated=token, role=role, testimonials=testimonials, opening_hours=get_opening_hours())

# Page "Véhicules en vente"
@app.route('/vehicles')
def vehicles_page():
    token = session.get('email') is not None
    return render_template('vehicles.html', user_is_authenticated=token, opening_hours=get_opening_hours())

# Page "Nous contacter"
@app.route('/contact')
def contact_page():
    token = session.get('email') is not None    
    return render_template('contact.html', user_is_authenticated=token, opening_hours=get_opening_hours())

@app.route('/testimonial')
def testimonial_page():
    token = session.get('email') is not None
    return render_template('testimonial.html', user_is_authenticated=token, opening_hours=get_opening_hours())


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    token = session.get('email') is not None
    form = LoginForm()  # Instantiate the LoginForm class
    return render_template('login.html', user_is_authenticated=token, opening_hours=get_opening_hours(), form=form)

@app.route('/logout')
def logout():
    # Effacer la session de l'utilisateur
    session.clear()
    token = session.get('email') is not None
    return render_template('index.html', user_is_authenticated=token, opening_hours=get_opening_hours())

@app.route('/profile')
def profile_page():
    # Récupérer les données de l'utilisateur à partir de la session
    email = session.get('email')
    role = session.get('role')
    token = session.get('email') is not None

    if role == 'employee':
        non_allowed_testimonials = fetch_non_allowed_testimonials()  # Implémentez cette fonction pour récupérer les témoignages non autorisés
        print(non_allowed_testimonials)
        return render_template('profile.html', email=email, role=role, user_is_authenticated=token, non_allowed_testimonials=non_allowed_testimonials, opening_hours=get_opening_hours())  # Transmettre les données d'ouverture au modèle
    else:
        return render_template('profile.html', email=email, role=role, user_is_authenticated=token, opening_hours=get_opening_hours(), services=get_service())  # Transmettre les données d'ouverture au modèle# Page "Nos services"

@app.route('/services')
def services_page():
    token = session.get('email') is not None
    return render_template('services.html', user_is_authenticated=token, opening_hours=get_opening_hours(), services=get_service())

#Création de l'objet Vehicle 
class Vehicle:
    def __init__(self, make, model, price, year, kilometers, img, vehicle_id):
        self.make = make
        self.model = model
        self.price = price
        self.year = year
        self.kilometers = kilometers
        self.img = img
        self.id = vehicle_id
class VehicleList:
    def __init__(self):
        self.vehicles = []

    def add_vehicle(self, vehicle):
        self.vehicles.append(vehicle)

    def remove_vehicle(self, vehicle_id):
        self.vehicles = [v for v in self.vehicles if v.id != vehicle_id]

    def get_all_vehicles(self):
        return [v.__dict__ for v in self.vehicles]
    
# Point d'API pour obtenir tous les véhicules
@app.route('/api/vehicles', methods=['GET'])
def get_all_vehicles():
    conn = mysql.connect()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM vehicles")
        vehicles_data = cursor.fetchall()

        vehicle_list = VehicleList()

        for vehicle_data in vehicles_data:
            vehicle_obj = Vehicle(
                make=vehicle_data[1],
                model=vehicle_data[2],
                price=vehicle_data[3],
                year=vehicle_data[4],
                kilometers=vehicle_data[5],
                img=vehicle_data[6],
                vehicle_id=vehicle_data[0],
            )
            vehicle_list.add_vehicle(vehicle_obj)

        return jsonify(vehicle_list.get_all_vehicles())
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/api/filter_vehicles', methods=['POST'])
def filter_vehicles():
    conn = mysql.connect()
    try:
        make = request.form.get('make')
        model = request.form.get('model')
        min_price = request.form.get('minPrice')
        max_price = request.form.get('maxPrice')
        min_year = request.form.get('minYear')
        max_year = request.form.get('maxYear')
        id = request.form.get('ref')
        img = request.form.get('img')


        # Construire la requête SQL pour filtrer les véhicules en fonction des critères
        query = "SELECT * FROM vehicles WHERE 1=1"
        params = []

        if make:
            query += " AND make = %s"
            params.append(make)
        if model:
            query += " AND model = %s"
            params.append(model)
        if min_price:
            query += " AND price >= %s"
            params.append(min_price)
        if max_price:
            query += " AND price <= %s"
            params.append(max_price)
        if min_year:
            query += " AND year >= %s"
            params.append(min_year)
        if max_year:
            query += " AND year <= %s"
            params.append(max_year)
        if id:
            query += " AND id LIKE %s"
            params.append(f'%{id}%')
        
        cursor = conn.cursor()
        cursor.execute(query, tuple(params))
        filtered_vehicles = cursor.fetchall()

        vehicle_list = []
        for vehicle in filtered_vehicles:
            vehicle_dict = {
                "make": vehicle[1],
                "model": vehicle[2],
                "price": vehicle[3],
                "year": vehicle[4],
                "kilometers": vehicle[5],
                "img": vehicle[6],  # Ajouter la valeur de la colonne "img" au dictionnaire
                "id": vehicle[0],
            }
            vehicle_list.append(vehicle_dict)

        return jsonify(vehicle_list)
    except Exception as e:
        return jsonify({"error": str(e)})
    finally:
        cursor.close()
        conn.close()

# Vérifier le mot de passe
def check_password(entered_password, stored_hash):
    return bcrypt.check_password_hash(stored_hash, entered_password)

# Permet de retrouver le mot de passe lié a l'adresse mail
def retrieve_password_hash_and_role_from_database(email):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        
        # Execute une requête afin de retrouver le mot de passe et le rôle associer a l'email
        query = "SELECT password, role FROM user WHERE email = %s"
        cursor.execute(query, (email,))
        result = cursor.fetchone()
        if result:
            password_hash, role = result  
            return password_hash, role
        else:
            return None, None  # L'utilisateur n'a pas été trouvé

    except Exception as e:
        print(f"Erreur durant la récupération du mot de passe et du rôle: {e}")
        return None, None
    finally:
        cursor.close()
        conn.close()

@app.route('/api/login', methods=['POST'])
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        print('Formulaire validé')
        email = form.email.data
        entered_password = form.password.data

        stored_hash, role = retrieve_password_hash_and_role_from_database(email)
        if stored_hash and check_password(entered_password, stored_hash):
            
            session['email'] = email
            session['role'] = role
            print('Connexion réussie')
            return jsonify({"success": True})
        else:
            print('Connexion échouée: Mauvais mot de passe ou utilisateur non trouvé')
            return jsonify({"success": False, "message": "Mauvais mot de passe ou utilisateur non trouvé."})
    else:
        print('Formulaire incorrecte')
    return jsonify({"success": False, "message": "Formulaire invalide."})


def insert_vehicle(make, model, price, year, kilometers, image_path):
    
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        # Définir la requête SQL pour insérer un nouveau véhicule
        sql_query = "INSERT INTO vehicles (make, model, price, year, kilometers, img) VALUES (%s, %s, %s, %s, %s, %s)"
        # Exécuter la requête avec les paramètres fournis
        cursor.execute(sql_query, (make, model, price, year, kilometers, image_path))
        # Valider les modifications dans la base de données
        conn.commit()
        print("Véhicule inséré avec succès!")
    except Exception as e:
        # Annuler les modifications en cas d'erreur
        conn.rollback()
        print("Erreur lors de l'insertion du véhicule :", e)


@app.route('/add_car', methods=['GET', 'POST'])
def add_car():

    message = None

    if request.method == 'POST':
        make = request.form.get('make')
        model = request.form.get('model')
        price = request.form.get('price')
        year = request.form.get('year')
        kilometers = request.form.get('year')

        # Gérer le téléchargement de l'image
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(image_path)
            print("L'image est conforme")
            try:
                insert_vehicle(make, model, price, year, kilometers, image_path)
                message = "Le véhicule a bien été inséré !"
            except Exception as e:
                message = f"Erreur lors de l'insertion du véhicule : {e}"
    token = session.get('email') is not None
    return render_template('profile.html', message=message, user_is_authenticated=token, opening_hours=get_opening_hours())


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Route permettant a l'admin de crée un compte employée
@app.route('/register_employee', methods=['POST'])
def register_employee():
    if session.get('role') == 'admin':
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = hash_password(password)

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            # Définir la requête SQL pour insérer un nouveau employé
            sql_query = "INSERT INTO user (email, password, role) VALUES (%s, %s, %s)"
            role = 'employé'
            # Exécuter la requête avec les paramètres fournis
            cursor.execute(sql_query, (email, hashed_password, role))
            # Valider les modifications dans la base de données
            conn.commit()
            message = "Compte employé créé avec succès !"
        except Exception as e:
            # Annuler les modifications en cas d'erreur
            conn.rollback()
            message = f"Erreur lors de la création du compte employé : {e}"
        finally:
            cursor.close()
            conn.close()

        token = session.get('email') is not None
        return render_template('profile.html', message=message, user_is_authenticated=token, opening_hours=get_opening_hours())
    else:
        return "Non autorisé", 401

# Point de terminaison de l'API pour gérer les soumissions de formulaire de contact
@app.route('/api/contacts', methods=['POST'])
def handle_contact_form():
    try:
        data = request.json
        print(data)
        prénom = data.get('prénom')
        nom = data.get('nom')
        message = data.get('message')
        email = data.get('email')
        téléphone = data.get('téléphone')
        print(téléphone)

        identifiant_véhicule = data.get('identifiant_véhicule')  # Nom de la clé corrigé
        
        # Obtenir le timestamp actuel
        conn = mysql.connect()
        try:
            cursor = conn.cursor()  
            # Insérer les données du formulaire de contact dans la table des contacts avec le timestamp
            requête_insertion = "INSERT INTO contacts (prénom, nom, email, téléphone, message, identifiant_véhicule) VALUES (%s, %s, %s, %s, %s, %s)"
            valeurs = (prénom, nom, email, téléphone, message, identifiant_véhicule)
            print(valeurs)
            cursor.execute(requête_insertion, valeurs)
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()

        réponse = {'success': True, 'message': 'Le message a bien été envoyé, Merci !'}
        return jsonify(réponse), 200
    except Exception as e:
        print("Erreur :", e)
        réponse = {'success': False, 'message': 'Une erreur s\'est produite, veuillez réessayer.'}
        return jsonify(réponse), 500

    
@app.route('/api/random_vehicle', methods=['GET'])
def random_vehicle():
    conn = mysql.connect()
    cursor = conn.cursor()

    # Retrouve tout les véhicules trier de manière aléatoire et limité au trois premiers résultats
    cursor.execute("SELECT * FROM vehicles ORDER BY RAND() LIMIT 3")
    random_vehicle = cursor.fetchall()
  


    return jsonify(random_vehicle)

# Route pour soumettre un témoignage
@app.route('/submit_testimonial', methods=['POST'])
def submit_testimonial():
    name = request.form.get('name')
    comment = request.form.get('comment')
    rating = request.form.get('rating')

    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        # Définir la requête SQL pour insérer un nouveau témoignage
        sql_query = "INSERT INTO testimonials (name, comment, rating, allowed) VALUES (%s, %s, %s, %s)"
        # Exécuter la requête avec les paramètres fournis
        cursor.execute(sql_query, (name, comment, rating, 0))  # Définir allowed à 0 (non) par défaut
        # Valider les modifications dans la base de données
        conn.commit()
        message = "Témoignage ajouté avec succès !"
    except Exception as e:
        # Annuler les modifications en cas d'erreur
        conn.rollback()
        message = f"Erreur lors de l'ajout du témoignage : {e}"
    finally:
        cursor.close()
        conn.close()

    return message

# Fonction pour récupérer les témoignages non autorisés
def fetch_non_allowed_testimonials():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        # Définir la requête SQL pour récupérer les témoignages avec allowed = 0
        sql_query = "SELECT * FROM testimonials WHERE allowed = 0"
        cursor.execute(sql_query)
        testimonials = cursor.fetchall()  # Récupérer tous les témoignages correspondants

    except Exception as e:
        testimonials = []  # En cas d'erreur, fournir une liste vide

    finally:
        cursor.close()
        conn.close()

    return testimonials

# Fonction pour obtenir les témoignages autorisés
def get_allowed_testimonials():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        # Définir la requête SQL pour récupérer les témoignages avec allowed = 1
        sql_query = "SELECT * FROM testimonials WHERE allowed = 1"
        cursor.execute(sql_query)
        testimonials = cursor.fetchall()  # Récupérer tous les témoignages correspondants

    except Exception as e:
        testimonials = []  # En cas d'erreur, fournir une liste vide

    finally:
        cursor.close()
        conn.close()

    return testimonials

# Obtenir une liste de témoignages autorisés
testimonials = get_allowed_testimonials()

# Route pour soumettre les témoignages sélectionnés
@app.route('/submit_selected_testimonials', methods=['POST'])
def submit_selected_testimonials():
    try:
        # Tenter de récupérer et de parser les données JSON de la requête
        data = json.loads(request.data)
        selected_testimonials = data.get('selectedTestimonials', [])
        print("Témoignages sélectionnés reçus :", selected_testimonials)  # Déclaration de débogage

        
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            # Mettre à jour le statut 'allowed' des témoignages sélectionnés à 1 (autorisé)
            for testimonial_id in selected_testimonials:
                # Utiliser l'identifiant testimonial_id comme identificateur pour mettre à jour le témoignage
                sql_query = "UPDATE testimonials SET allowed = 1 WHERE id = %s"
                print('Requête envoyée : ' + sql_query)
                cursor.execute(sql_query, (testimonial_id,))
                conn.commit()  # Valider les modifications dans la base de données

        except Exception as e:
            # Gérer les exceptions qui se produisent lors des opérations sur la base de données
            print(f"Erreur : {e}")
            conn.rollback()
        finally:
            # Fermer le curseur et la connexion dans le bloc 'finally' pour s'assurer que cela se produit
            if cursor:
                cursor.close()
            if conn:
                conn.close()

        # Retourner une réponse de succès
        return "Témoignages sélectionnés soumis avec succès"
    except json.JSONDecodeError as e:
        # Gérer l'erreur de décodage JSON
        print(f"Erreur de décodage JSON : {e}")
        return "Erreur : Données JSON non valides dans la requête", 400  # Retourner une réponse 400 Bad Request

@app.route('/create_super_admin', methods=['POST'])
def create_super_admin():
    # Vérifiez si l'utilisateur est authentifié
    token = session.get('email') is not None
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Hasher le mot de passe de manière sécurisée en utilisant bcrypt
        hashed_password = hash_password(password)

        # Insérer les données du super administrateur dans la base de données
        conn = mysql.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO user (email, password) VALUES (%s, %s)", (username, hashed_password))
            conn.commit()
            return render_template('index.html', testimonials=testimonials, user_is_authenticated=token, opening_hours=get_opening_hours())
        except Exception as e:
            conn.rollback()
            print(f"Erreur lors de la création du super administrateur : {e}")
        finally:
            cursor.close()
            conn.close()

    return render_template('install_super_admin.html', user_is_authenticated=token, testimonials=testimonials)

def hash_password(password):
    hashed_password = bcrypt.generate_password_hash(password)
    return hashed_password

@app.route('/super_admin_page')
def super_admin_page():
    token = session.get('email') is not None
    role = session.get('role')
    # Vérifiez si l'utilisateur actuel est un super administrateur
    if 'role' in session and session['role'] == 'superadmin':
        return render_template('super_admin_page.html', user_is_authenticated=token, role=role)
    else:
        # Redirigez vers une page d'erreur ou une autre page appropriée
        return "Accès non autorisé"

@app.route('/install_super_admin', methods=['GET', 'POST'])
def install_super_admin():
    # Vérifiez si l'utilisateur est authentifié
    token = session.get('email') is not None

    if request.method == 'POST':
        # Récupérez les données de courriel et de mot de passe postées depuis le formulaire
        email = request.form.get('email')
        password = request.form.get('password')

        # Validez les données (vous pouvez ajouter votre logique de validation ici)

        # Hasher le mot de passe de manière sécurisée en utilisant bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Vérifiez s'il existe déjà au moins un super administrateur
        conn = mysql.connect()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM user WHERE role = 'superadmin'")
            count = cursor.fetchone()[0]
            
            if count > 0:
                return "L'installation est déjà terminée. Vous pouvez désormais vous connecter. <a href='/'>Accueil</a> <a href='/login'>Se connecter</a>"
            
            # S'il n'y a pas de super administrateurs, insérez les données du super administrateur dans la base de données
            cursor.execute("INSERT INTO user (email, password, role) VALUES (%s, %s, %s)", (email, hashed_password, 'superadmin'))
            conn.commit()
            return "L'installation est finie. Vous pouvez désormais vous connecter. <a href='/'>Accueil</a> <a href='/login'>Se connecter</a>"
        except Exception as e:
            conn.rollback()
            print(f"Erreur lors de la création du super administrateur : {e}")
        finally:
            cursor.close()
            conn.close()
    
    # Vérifiez s'il existe des super administrateurs, et ne renvoyez pas la page s'il y en a au moins un
    conn = mysql.connect()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM user WHERE role = 'superadmin'")
        count = cursor.fetchone()[0]
        if count > 0:
            return "L'installation est déjà terminée. Vous pouvez désormais vous connecter. <a href='/'>Accueil</a> <a href='/login'>Se connecter</a>"
    except Exception as e:
        print(f"Erreur lors de la vérification de l'existence d'un super administrateur : {e}")
    finally:
        cursor.close()
        conn.close()

    return render_template('install_super_admin.html', user_is_authenticated=token, testimonials=testimonials)

@app.route('/register_admin', methods=['POST'])
def register_admin():
    if session.get('role') == 'superadmin':
        email = request.form.get('email')
        password = request.form.get('password')
        hashed_password = hash_password(password)
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            # Définir la requête SQL pour insérer un nouveau employé
            sql_query = "INSERT INTO user (email, password, role) VALUES (%s, %s, %s)"
            role = 'admin'
            # Exécuter la requête avec les paramètres fournis
            cursor.execute(sql_query, (email, hashed_password, role))
            # Valider les modifications dans la base de données
            conn.commit()
            message = "Compte administrateur créé avec succès!"
        except Exception as e:
            # Annuler les modifications en cas d'erreur
            conn.rollback()
            message = f"Erreur lors de la création du compte employé : {e}"
        finally:
            cursor.close()
            conn.close()

        token = session.get('email') is not None
        return render_template('super_admin_page.html', message=message, user_is_authenticated=token)
    else:
        return "Non autorisé", 401

@app.route('/update_opening_hours', methods=['POST'])
def update_opening_hours():
    if session.get('role') == 'admin':
        if request.method == 'POST':
            monday = request.form.get('monday')
            tuesday = request.form.get('tuesday')
            wednesday = request.form.get('wednesday')
            thursday = request.form.get('thursday')
            friday = request.form.get('friday')
            saturday = request.form.get('saturday')
            sunday = request.form.get('sunday')
            
            try:
                conn = mysql.connect()
                cursor = conn.cursor()

                # Mettre à jour les horaires d'ouverture dans la base de données
                cursor.execute("UPDATE opening_hours SET monday = %s, tuesday = %s, wednesday = %s, thursday = %s, friday = %s, saturday = %s, sunday = %s WHERE id = 1", (monday, tuesday, wednesday, thursday, friday, saturday, sunday))
                conn.commit()
                message = "Horaires d'ouverture modifiés avec succès!"
            except Exception as e:
                conn.rollback()
                message = f"Erreur lors de la modification des horaires d'ouverture : {e}"
            finally:
                cursor.close()
                conn.close()

            token = session.get('email') is not None

            return render_template('profile.html', message=message, user_is_authenticated=token, opening_hours=get_opening_hours() )
    else:
        return "Non autorisé", 401
    
def get_opening_hours():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        # Récupérer les horaires d'ouverture depuis la base de données
        cursor.execute("SELECT * FROM opening_hours WHERE id = 1")
        opening_hours = cursor.fetchone()
        return opening_hours
    except Exception as e:
        # Gérer l'exception (par exemple, enregistrer l'erreur)
        print(f"Erreur lors de la récupération des horaires d'ouverture : {e}")
        return None
    finally:
        cursor.close()
        conn.close()

get_opening_hours()


def get_service():
    try:
        conn = mysql.connect()
        cursor = conn.cursor()

        # Récupérer les services avec les prix depuis la base de données
        cursor.execute("SELECT name, description, price FROM services")
        serviceslist = cursor.fetchall()

        return serviceslist
    except Exception as e:
        # Gérer l'exception (par exemple, enregistrer l'erreur)
        print(f"Erreur lors de la récupération des services : {e}")
        return None
    finally:
        cursor.close()
        conn.close()

@app.route('/add_service', methods=['POST'])
def add_service():
    if session.get('role') == 'admin':
        if request.method == 'POST':
            new_service_name = request.form.get('new_service_name')
            new_service_description = request.form.get('new_service_description')
            new_service_price = request.form.get('new_service_price')

            try:
                conn = mysql.connect()
                cursor = conn.cursor()

                # Insérer le nouveau service dans la base de données
                cursor.execute("INSERT INTO services (name, description, price) VALUES (%s, %s, %s)",
                               (new_service_name, new_service_description, new_service_price))
                conn.commit()
                message = "Nouveau service ajouté avec succès !"
            except Exception as e:
                conn.rollback()
                message = f"Erreur lors de l'ajout du nouveau service : {e}"
            finally:
                cursor.close()
                conn.close()

            # Après avoir ajouté le nouveau service, récupérez les services mis à jour et transmettez-les à la page de profil
            services = get_service()
            token = session.get('email') is not None

            if services:
                services_list = [{"name": service[0], "description": service[1], "price": service[2]} for service in services]
                return render_template('profile.html', message=message, user_is_authenticated=token, services=services_list, opening_hours=get_opening_hours())
            else:
                return render_template('profile.html', message=message, user_is_authenticated=token, services=None, opening_hours=get_opening_hours())
    else:
        return "Non autorisé", 401

@app.route('/edit_services', methods=['POST'])
def edit_services():
    if session.get('role') == 'admin':
        if request.method == 'POST':
            # Récupérer les données des services modifiés depuis le formulaire
            service_names = request.form.getlist('service_name[]')
            service_descriptions = request.form.getlist('service_description[]')
            service_prices = request.form.getlist('service_price[]')

            try:
                conn = mysql.connect()
                cursor = conn.cursor()

                # Parcourir les données et mettre à jour les services dans votre base de données
                for name, description, price in zip(service_names, service_descriptions, service_prices):
                    cursor.execute("UPDATE services SET description = %s, price = %s WHERE name = %s",
                                   (description, price, name))
                    conn.commit()
                message = "Services mis à jour avec succès !"
            except Exception as e:
                conn.rollback()
                message = f"Erreur lors de la mise à jour des services : {e}"
            finally:
                cursor.close()
                conn.close()

            # Après avoir mis à jour les services, récupérez les services mis à jour et transmettez-les à la page de profil
            services = get_service()
            token = session.get('email') is not None

            if services:
                services_list = [{"name": service[0], "description": service[1], "price": service[2]} for service in services]
                return render_template('profile.html', message=message, user_is_authenticated=token, services=services_list, opening_hours=get_opening_hours())
            else:
                return render_template('profile.html', message=message, user_is_authenticated=token, services=None, opening_hours=get_opening_hours())
    else:
        return "Non autorisé", 401

    
if __name__ == '__main__':
    app.run(debug=True)
