import json
import numpy as np
import os
import openai
from datetime import datetime
from dateutil.relativedelta import relativedelta

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for

from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from aux import login_required
from database.db_setup import get_db, close_connection
import requests


# Configuración mejorada del modo debug
app = Flask(__name__)
app.config.update(
    DEBUG=True,
    TEMPLATES_AUTO_RELOAD=True,
    SEND_FILE_MAX_AGE_DEFAULT=0,
    ENV="development"
)
app.jinja_env.auto_reload = True
openai.api_key = os.getenv('OPENAI_API_KEY')

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database/LIFE.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Example route (Main page)
@app.route('/')
def index():
    """Main page route"""
    user_id = session.get('user_id')  # Obtén el ID del usuario en la sesión
    user = None
    baby = None

    if user_id:
        # Obtén los datos del usuario desde la base de datos
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()
        
        if result:
            user = result[0]  # El nombre de usuario está en la primera columna
        
            cursor.execute("SELECT first_name, last_name, birth_date, gender, email FROM babies WHERE user_id = ?", (user_id,))
            baby_result = cursor.fetchone()

            if baby_result:
                baby = {
                    "first_name": baby_result[0],
                    "last_name": baby_result[1],
                    "birth_date": baby_result[2],
                    "gender": baby_result[3],
                    "email": baby_result[4]
                }
        else:
            # Si el usuario no se encuentra en la base de datos, elimina la sesión
            session.clear()

    return render_template('home.html' if user else 'cover.html', user=user, baby=baby)    

def rows_to_dict(rows, columns):
    """Converts a list of rows and columns into a list of dictionaries"""
    return [dict(zip(columns, row)) for row in rows]


# Route to register a baby
@app.route("/baby", methods=["GET", "POST"])
@login_required
def baby():
    """Register baby details for the logged-in user"""
    if request.method == "POST":
        # Get the baby details from the form
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        birth_date = request.form.get("birth_date")
        gender = request.form.get("gender")
        # email = request.form.get("email") # Optional

        # Ensure the data is provided
        if not first_name or not last_name or not birth_date:
            flash("First name, last name, and birth date are required")
            return redirect("/baby")
        try:
            # Save the baby details in the database
            user_id = session["user_id"]
            db.execute(
                "INSERT INTO babies (user_id, first_name, last_name, birth_date, gender) VALUES (?, ?, ?, ?, ?)",
                user_id, first_name, last_name, birth_date, gender
            )
            flash("Baby registered successfully!", "success")
            return redirect("/")  # Redirect to main page
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "error")
            return redirect(url_for('baby'))
    
    return render_template("baby.html")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    """View and update user profile"""
    user_id = session["user_id"]
    db = get_db()
    cursor = db.cursor()
    
    if request.method == "POST":
        form_type = request.form.get("form_type")
        
        # Handle user profile update
        if form_type == "user_update":
            first_name = request.form.get("first_name")
            email = request.form.get("email")
            current_password = request.form.get("current_password")
            new_password = request.form.get("new_password")
            confirm_password = request.form.get("confirm_password")

            # Validación del nombre de usuario (solo letras)
            # Validación del nombre de usuario (letras, números, guiones, etc.)
            import re
            if not re.match(r'^[A-Za-z0-9_\-.]+$', first_name):
                flash("Username can contain only letters, numbers, underscores, dots and hyphens", "error")
                return redirect("/profile")
            
            # Validate current password if trying to change password
            if new_password:
                # First verify current password
                cursor.execute("SELECT password FROM users WHERE id = ?", (user_id,))
                stored_hash = cursor.fetchone()[0]
                
                if not check_password_hash(stored_hash, current_password):
                    flash("Current password is incorrect", "error")
                    return redirect("/profile")
                
                # Then check if new passwords match
                if new_password != confirm_password:
                    flash("New passwords do not match", "error")
                    return redirect("/profile")
                
                # Update user data with new password
                cursor.execute(
                    "UPDATE users SET username = ?, email = ?, password = ? WHERE id = ?",
                    (first_name, email, generate_password_hash(new_password), user_id)
                )
            else:
                # Update user data without changing password
                cursor.execute(
                    "UPDATE users SET username = ?, email = ? WHERE id = ?",
                    (first_name, email, user_id)
                )
                
            db.commit()
            flash("User profile updated successfully!", "success")
            
        # Handle baby profile update
        elif form_type == "baby_update":
            baby_id = request.form.get("baby_id")
            if baby_id:
                baby_first_name = request.form.get("baby_first_name")
                baby_last_name = request.form.get("baby_last_name")
                baby_birth_date = request.form.get("baby_birth_date")

                # Vadlidate baby names (only letters)
                import re
                if not re.match(r'^[A-Za-zÁáÉéÍíÓóÚúÜüÑñ ]+$', baby_first_name) or not re.match(r'^[A-Za-zÁáÉéÍíÓóÚúÜüÑñ ]+$', baby_last_name):
                    flash("Baby names must contain only letters", "error")
                    return redirect("/profile")

                cursor.execute(
                    "UPDATE babies SET first_name = ?, last_name = ?, birth_date = ? WHERE id = ? AND user_id = ?",
                    (baby_first_name, baby_last_name, baby_birth_date, baby_id, user_id)
                )
                db.commit()
                flash("Baby profile updated successfully!", "success")

        return redirect("/profile")
    
    # Fetch user data
    cursor.execute("SELECT username, email FROM users WHERE id = ?", (user_id,))
    user_data = cursor.fetchone()

    # Fetch baby data
    cursor.execute("SELECT id, first_name, last_name, birth_date, gender FROM babies WHERE user_id = ?", (user_id,))
    baby_data = cursor.fetchall()
    
    return render_template("profile.html", user=user_data, babies=baby_data)


# Route to delete a baby
@app.route("/delete_baby/<int:baby_id>", methods=["POST"])
@login_required
def delete_baby(baby_id):
    """Delete a baby from the database"""
    user_id = session["user_id"]
    db = get_db()
    cursor = db.cursor()

    # Delete the baby from the database
    cursor.execute("DELETE FROM babies WHERE id = ? AND user_id = ?", (baby_id, user_id))
    db.commit()

    flash("Baby deleted successfully!", "success")
    return redirect("/profile")


# Route to create a new user
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register a new user and redirect to baby registration"""
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Ensure the data is provided
        if not username:
            flash("Must provide username", "error")
            return redirect("/register")
        elif not password:
            flash("Must provide password", "error")
            return redirect("/register")
        elif not email:
            flash("Must provide email", "error")
            return redirect("/register")

        # Check if the user already exists
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            flash("Username already exists", "error")
            return redirect("/register")

        try:
            # Register the new user
            cursor.execute(
                "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                (username, email, generate_password_hash(password))
            )
            db.commit()

            # Retrieve the user's id
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            user_id = cursor.fetchone()[0]
            session["user_id"] = user_id  # Store user in session

            flash("Registered successfully! Please provide baby details.", "success")
            return redirect("/baby")  # Redirect to baby registration form
        
        except Exception as e:
            flash(f"An error occurred during registration: {str(e)}", "error")
            return redirect("/register")

    return render_template("register.html")


# Route to login
def rows_to_dict(rows, columns):
    """Convierte filas a diccionarios usando los nombres de las columnas."""
    return [dict(zip(columns, row)) for row in rows]


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Validate provided data
        if not username or not password:
            return "Must provide username and password", 400

        # Search for the user in the database
        db = get_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        rows = cursor.fetchall()

        # Convert the rows to a list of dictionaries
        columns = ['id', 'username', 'email', 'password', 'created_at']
        rows_dict = rows_to_dict(rows, columns)

        # Validate the user and password
        if not rows_dict or not check_password_hash(rows_dict[0]['password'], password):
            return "Invalid username or password", 401

        # Save the user's id in the session
        session["user_id"] = rows_dict[0]['id']

        return redirect(url_for("index"))
    
    return render_template("login.html")


# Route to add babies milestones
@app.route("/milestones", methods=["GET", "POST"])
def milestones():
    data = request.get_json()

    required_fields = ["milestone", "date"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "User not logged in"}), 401

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO milestones (user_id, milestone, date) VALUES (?, ?, ?)",
        (user_id, data["milestone"], data["date"])
    )
    db.commit()
    return jsonify({"message": "Milestone added successfully!"}), 201


# Route to chatbot
@app.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()  # Asegúrate de que los datos lleguen en formato JSON
    question = data.get("question") if data else None

    if not question:
        return jsonify({"answer": "You must provide a question"}), 400

    try:
        # Conection to the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant for parents with newborns. Answer with helpful tips."},
                {"role": "user", "content": question}
            ]
        )

        # Extract the answer from the response
        answer = response["choices"][0]["message"]["content"]
        return jsonify({"answer": answer}), 200

    except openai.error.OpenAIError as e:
        print(f"Error with the OpenAI API: {e}")
        return jsonify({"answer": "There was an error processing the question"}), 500


# Route to get the weather (OpenWeatherMap API)
@app.route("/weather", methods=["GET"])
def weather():
    city = request.args.get("city", "Mexico City")
    api_key = "my openweather api key"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
    response = requests.get(url)
    data = response.json()
    return jsonify(data), 200


# Route to create a new goal
@app.route("/goals", methods=["POST"])
def create_goal():
    data = request.get_json()

    required_fields = ["user_id", "name", "description", "target_date", "budget"]
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400
    
    db = get_db()
    cursor = db.cursor()
    query = """
        INSERT INTO goals (user_id, name, description, target_date, budget)
        VALUES (?, ?, ?, ?, ?)
        """
    cursor.execute(query, (
        data["user_id"],
        data["name"],
        data["description"],
        data["target_date"],
        data["budget"]
    ))
    db.commit()
    return jsonify({"message": "Goal created successfully!"}), 201


# Route to get all goals for a user
@app.route("/goals/<int:user_id>", methods=["GET"])
def get_goals(user_id):
    db = get_db()
    cursor = db.cursor()
    query = " SELECT * FROM goals WHERE user_id = ?"
    cursor.execute(query, (user_id,))
    goals = cursor.fetchall()
    return jsonify(goals), 200


@app.route('/getBabyData', methods=['GET'])
@login_required
def get_baby_data():
    baby_id = request.args.get('id', type=int)
    db = get_db()  # Conexión a la base de datos
    cursor = db.cursor()

    # Recuperar los datos del bebé (asumiendo que el bebé tiene un campo 'user_id')
    cursor.execute("SELECT gender, birth_date FROM babies WHERE id = ?", (baby_id,))
    baby_data = cursor.fetchone()

    if baby_data:
        baby = {
            "gender": baby_data[0],
            "birth_date": baby_data[1]
        }
        return jsonify(baby)
    else:
        return jsonify({"error": "Baby not found"}), 404



@app.route("/get_growth_data")
def get_growth_data():
    user_id = session["user_id"]
    data = db.execute("SELECT year, month, growth_cm FROM growth_data WHERE user_id = ? ORDER BY year, month", user_id)
    has_data = len(data) > 0
    return jsonify({"has_data": has_data, "data": data})


# Define the base directory - Solución al problema de rutas absolutas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Define the paths to the JSON files con rutas relativas
boys_weight_file = os.path.join(BASE_DIR, "static/JS/json/boys_weight_for_age_percentiles.json")
boys_height_file = os.path.join(BASE_DIR, "static/JS/json/boys_height_for_age_percentiles.json")
girls_weight_file = os.path.join(BASE_DIR, "static/JS/json/girls_weight_for_age_percentiles.json")
girls_height_file = os.path.join(BASE_DIR, "static/JS/json/girls_height_for_age_percentiles.json")


@app.route("/add_growth", methods=["GET", "POST"])
@login_required
def add_growth():
    user_id = session["user_id"]
    
    # Obtener los datos del bebé desde la base de datos
    baby = db.execute("SELECT * FROM babies WHERE user_id = ?", user_id)
    
    if not baby:
        flash("No baby data found. Please register your baby first.", "error")
        return redirect("/baby")
    
    baby = baby[0]  # Asumimos que solo hay un bebé por usuario
    birth_date = datetime.strptime(baby["birth_date"], "%Y-%m-%d")
    gender = baby["gender"]
    
    # Calcular la edad del bebé en años y meses
    age = relativedelta(datetime.now(), birth_date)
    age_years = age.years
    age_months = age.months + age_years * 12  # Edad en meses
    
    current_year = datetime.now().year
    current_month = datetime.now().month

    # Limitar los años disponibles:
    if age_years < 5:
        years = [str(i) for i in range(birth_date.year, current_year + 1)]
    else:
        years = [str(i) for i in range(current_year - 5, current_year + 1)]

    # Limitar los meses disponibles:
    valid_months = [str(i) for i in range(1,13)]

    # Cargar los archivos de percentiles
    if gender == 'male':
        weight_file = boys_weight_file
        height_file = boys_height_file
    else:
        weight_file = girls_weight_file
        height_file = girls_height_file
    
    with open(weight_file) as f:
        weight_percentiles = json.load(f)
    
    with open(height_file) as f:
        height_percentiles = json.load(f)
    
    possible_date = []
    for year in years:
        start_month = birth_date.month if int(year) == birth_date.year else 1
        end_month = current_month + 1 if int(year) == current_year else 13
        for month in range(start_month, end_month):
            possible_date.append((int(year), month))
    
    # Calcular rangos para cada combinacion de year & month
    ranges_by_date = {}
    for year, month in possible_date:
        # Calcular la edad en meses para la fecha seleccionada
        selected_date = datetime(year, month, 1)
        age_at_selected = relativedelta(selected_date, birth_date)
        age_months_at_selected = age_at_selected.years * 12 + age_at_selected.months
        
        # Obtener percentiles para esa edad
        weight_entry = next((entry for entry in weight_percentiles if entry["Month"] == age_months_at_selected), None)
        height_entry = next((entry for entry in height_percentiles if entry["Day"] == age_months_at_selected * 30), None)

        if weight_entry and height_entry:
            weight_percentiles_list = [
                weight_entry["P01"], weight_entry["P1"], weight_entry["P3"],
                weight_entry["P5"], weight_entry["P10"], weight_entry["P15"],
                weight_entry["P25"], weight_entry["P50"], weight_entry["P75"],
                weight_entry["P85"], weight_entry["P90"], weight_entry["P95"],
                weight_entry["P97"], weight_entry["P99"], weight_entry["P999"]
            ]
            height_percentiles_list = [
                height_entry["P01"], height_entry["P1"], height_entry["P3"],
                height_entry["P5"], height_entry["P10"], height_entry["P15"],
                height_entry["P25"], height_entry["P50"], height_entry["P75"],
                height_entry["P85"], height_entry["P90"], height_entry["P95"],
                height_entry["P97"], height_entry["P99"], height_entry["P999"]
            ]
            
            weight_min = min(weight_percentiles_list)
            weight_max = max(weight_percentiles_list)
            weight_range = [round(w, 1) for w in np.arange(weight_min, weight_max + 0.1, 0.1)]
            
            height_min = min(height_percentiles_list)
            height_max = max(height_percentiles_list)
            height_range = [round(h, 1) for h in np.arange(height_min, height_max + 0.1, 0.1)]
            
            # Crear la clave como cadena en lugar de tupla
            key = f"{year}-{month}"
            ranges_by_date[key] = {
                'weight_range': weight_range,
                'height_range': height_range
            }
    
    # Convert to JSON to send to the template
    ranges_json = json.dumps(ranges_by_date)
    
    # Handle POST request
    if request.method == "POST":
        year = int(request.form.get("year"))
        month = int(request.form.get("month"))
        weight = float(request.form.get("weight"))
        height = float(request.form.get("height"))

        if not year or not month or not weight or not height:
            flash("All fields are required", "error")
            return redirect("/add_growth")
        
        if year < birth_date.year or (year == birth_date.year and month < birth_date.month):
            flash("Selected date is before the baby's birth date", "error")
            return redirect("/add_growth")
        
        if weight <= 0 or weight > 80:
            flash("Weight must be greater than 0.0 kg and less than or equal to 80 kg", "error")
            return redirect("/add_growth")
        
        if height <= 0 or height > 200:
            flash("Height must be greater than 0.0 cm and less than or equal to 200 cm", "error")
            return redirect("/add_growth")
        
        # Calcular la edad en el momento seleccionado para verificar los percentiles
        selected_date = datetime(year, month, 1)
        age_at_selected_date = relativedelta(selected_date, birth_date)
        age_months_at_selected = age_at_selected_date.years * 12 + age_at_selected_date.months

        weight_entry = next((entry for entry in weight_percentiles if entry["Month"] == age_months_at_selected), None)
        height_entry = next((entry for entry in height_percentiles if entry["Day"] == age_months_at_selected * 30), None)

        if not weight_entry or not height_entry:
            flash("Percentiles not found for the selected age", "error")
            return redirect("/add_growth")
        
        # Actualizar o agregar los datos de crecimiento
        existing_record = db.execute("SELECT * FROM growth_data WHERE user_id = ? AND year = ? AND month = ?", user_id, year, month)
        last_record = db.execute(
            "SELECT id, height, growth_cm FROM growth_data WHERE user_id = ? ORDER BY year DESC, month DESC LIMIT 1", user_id
        )
        
        growth_cm = 0
        if last_record:
            last_height = last_record[0]["height"]
            last_growth_cm = last_record[0]["growth_cm"]
            growth_cm = height - last_height + last_growth_cm
        else:
            growth_cm = height
        
        if existing_record:
            db.execute(
                "UPDATE growth_data SET weight = ?, height = ?, growth_cm = ? WHERE user_id = ? AND year = ? AND month = ?",
                weight, height, growth_cm, user_id, year, month
            )
            flash("Growth data updated successfully!", "success")
        else:
            db.execute(
                "INSERT INTO growth_data (user_id, birthdate, year, month, weight, height, growth_cm) VALUES (?, ?, ?, ?, ?, ?, ?)",
                user_id, birth_date, year, month, weight, height, growth_cm
            )
            flash("Growth data added successfully!", "success")
        
        return redirect("/")

    # Renderizar el template con los datos necesarios
    return render_template("add_growth.html", baby=baby, years=years, months=valid_months, current_year=current_year, ranges_json=ranges_json)


# Route to logout
@app.route("/logout")
def logout():
    ''' Logout the user '''
    if "user_id" in session:
        # Forget any user_id
        session.clear()

    # Redirect user to login form
    return redirect("/")


# Initialize the server con configuración para recarga automática
if __name__ == '__main__':
    # Importante: use_reloader=True asegura la recarga automática
    app.run(debug=True, use_reloader=True, host='0.0.0.0')


@app.teardown_appcontext
def teardown_db(exception):
    close_connection(exception)