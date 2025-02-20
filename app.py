from flask import Flask, render_template, request, redirect, url_for, jsonify
import random
import json
import datetime
app = Flask(__name__)
app.secret_key = "jklhkjgjghlhjhlhjklh"  # Required for session management

# Set session timeout duration (e.g., 30 minutes)
SESSION_TIMEOUT = datetime.timedelta(minutes=30)

# Person class
class Person:
    def __init__(self, initials, seniority, points):
        self.initials = initials
        self.seniority = seniority
        self.points = points

    def __repr__(self):
        return f"{self.initials} (Seniority: {self.seniority}, Points: {self.points})"

# Load people data from a JSON file
def load_people(filename="people_data.json"):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            return [Person(p["initials"], p["seniority"], p["points"]) for p in data]
    except FileNotFoundError:
        return []

# Sort people based on assignment priority
def sort_people(people):
    sorted_people = sorted(people, key=lambda p: (p.points, p.seniority))
    i = 0
    while i < len(sorted_people) - 1:
        j = i
        while j < len(sorted_people) - 1 and sorted_people[j].points == sorted_people[j+1].points and sorted_people[j].seniority == sorted_people[j+1].seniority:
            j += 1
        if i != j:
            random.shuffle(sorted_people[i:j+1])
        i = j + 1
    return sorted_people

# Assign tasks based on the updated structure
import random

import random

def assign_tasks(sorted_people):
    tasks = {
        "Setup": 3,
        "Shift 1": {
                "Bar": 2,
            "Couch": 1,
            "Inner Door": 1,
            "Coat Check": 1,
            "Table": 1,
            "Outer Door": 2,
            "Sober": 2,
            "DJ": 1
            },
            "Shift 2": {
                "Bar": 2,
            "Couch": 1,
            "Inner Door": 1,
            "Coat Check": 1,
            "Table": 1,
            "Outer Door": 2,
            "Sober": 2,
            "DJ": 1
            },
        "Cleanup": 3
    }

    # Initialize assignments
    assignments = {"Setup": [], "Shift 1": {"Bar": [],
            "Couch": [],
            "Inner Door": [],
            "Coat Check": [],
            "Table": [],
            "Outer Door": [],
            "Sober": [],
            "DJ": []
            },
            "Shift 2": {
                "Bar": [],
            "Couch": [],
            "Inner Door": [],
            "Coat Check": [],
            "Table": [],
            "Outer Door":[],
            "Sober":[],
            "DJ": []
            }, "Cleanup": []}

    # Initialize available slots for tasks
    available_tasks = {
        "Setup": tasks["Setup"],
        "Shift1": {role: count for role, count in tasks["Shift 1"].items()},
        "Shift2": {role: count for role, count in tasks["Shift 2"].items()},
        "Cleanup": tasks["Cleanup"]
    }
    still_assigned =["Setup", "Shift 1", "Shift 2", "Cleanup"]
    # Assign each person randomly to a task
    while still_assigned:
        person = sorted_people.pop(0)  # Take the first person from the sorted list
        assigned = False

        while assigned == False and still_assigned:
            task_type = random.choice(still_assigned)  # Randomly choose a task type
            if task_type == "Setup":
                if available_tasks["Setup"] > 0:
                    assignments["Setup"].append(person.initials)
                    available_tasks["Setup"] -= 1
                    assigned = True
                else:
                    still_assigned.remove(task_type)
            elif task_type == "Shift 1":
                # Randomly pick a role in During that still has available slots
                available_roles = [role for role, count in available_tasks["Shift1"].items() if count > 0]
                if available_roles:
                    role = random.choice(available_roles)
                    if role not in assignments[task_type]:
                        assignments[task_type][role] = []
                    assignments[task_type][role].append(person.initials)
                    assigned = True
                    available_tasks["Shift1"][role] -= 1
                else:
                    still_assigned.remove(task_type)
            elif task_type == "Shift 2":
                # Randomly pick a role in During that still has available slots
                available_roles = [role for role, count in available_tasks["Shift2"].items() if count > 0]
                if available_roles:
                    role = random.choice(available_roles)
                    if role not in assignments[task_type]:
                        assignments[task_type][role] = []
                    assignments[task_type][role].append(person.initials)
                    assigned = True
                    available_tasks["Shift2"][role] -= 1
                else:
                    still_assigned.remove(task_type)

            elif task_type == "Cleanup":
                if available_tasks["Cleanup"] > 0:
                    assignments["Cleanup"].append(person.initials)
                    assigned = True
                    available_tasks["Cleanup"] -= 1
                else: 
                    still_assigned.remove(task_type)
    return assignments
ASSIGNMENTS  = {"Setup": [], "Shift 1": {"Bar": [],
            "Couch": [],
            "Inner Door": [],
            "Coat Check": [],
            "Table": [],
            "Outer Door": [],
            "Sober": [],
            "DJ": []
            },
            "Shift 2": {
                "Bar": [],
            "Couch": [],
            "Inner Door": [],
            "Coat Check": [],
            "Table": [],
            "Outer Door":[],
            "Sober":[],
            "DJ": []
            }, "Cleanup": []}
PEOPLE = load_people()
SORTED_PEOPLE = sort_people(PEOPLE)
DO_NOT_ASSIGN = []
from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import json

app = Flask(__name__)
app.secret_key = "your_secret_key"  # Required for session management

# Moderator password
MODERATOR_PASSWORD = "moderator123"

# Load people data from a JSON file
def load_people(filename="people_data.json"):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save updated people data to the JSON file
def save_people(data, filename="people_data.json"):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

# Load pending requests from a JSON file
def load_requests(filename="requests.json"):
    try:
        with open(filename, "r") as file:
            return [json.loads(line) for line in file]
    except FileNotFoundError:
        return []

# Save updated requests to the JSON file
def save_requests(requests, filename="requests.json"):
    with open(filename, "w") as file:
        for req in requests:
            json.dump(req, file)
            file.write("\n")

# Route for the main page showing task assignments
@app.route("/")
def index():
    return render_template("index.html", assignments=ASSIGNMENTS)
@app.route("/assign_tasks_route", methods=["POST"])
def assign_tasks_route():
    global ASSIGNMENTS, SORTED_PEOPLE
    
    ASSIGNMENTS = assign_tasks(SORTED_PEOPLE[:])
    return redirect(url_for("moderator"))
@app.route("/edit_task", methods=["POST"])
def edit_task():
    global ASSIGNMENTS

    # Update Setup
    setup_keys = [key for key in request.form.keys() if key.startswith("setup")]
    ASSIGNMENTS["Setup"] = [request.form[key] for key in setup_keys]

    # Update Shift 1
    shift1_keys = [key for key in request.form.keys() if key.startswith("shift1")]
    for key in shift1_keys:
        _, role, index = key.split("_")
        index = int(index) - 1
        ASSIGNMENTS["Shift 1"][role][index] = request.form[key]

    # Update Shift 2
    shift2_keys = [key for key in request.form.keys() if key.startswith("shift2")]
    for key in shift2_keys:
        _, role, index = key.split("_")
        index = int(index) - 1
        ASSIGNMENTS["Shift 2"][role][index] = request.form[key]

    # Update Cleanup
    cleanup_keys = [key for key in request.form.keys() if key.startswith("cleanup")]
    ASSIGNMENTS["Cleanup"] = [request.form[key] for key in cleanup_keys]

    return redirect(url_for("moderator"))

# Route for requesting out of a shift
@app.route("/request", methods=["GET", "POST"])
def request_shift():
    if request.method == "POST":
        # Parse form data
        selected_value = request.form.get("role_initials")  # Format: "Shift 1 - Bar - RAC"
        description = request.form.get("description", "")

        # Parse the selected value to extract shift, role, and initials
        parts = selected_value.split(" - ")
        shift = parts[0]
        role_or_person = parts[1]

        if shift in ["Shift 1", "Shift 2"]:
            role = parts[1]
            initials = parts[2]
        else:
            initials = parts[1]

        # Save the request to a file
        new_request = {"shift": shift, "role": role_or_person, "initials": initials, "description": description}
        with open("requests.json", "a") as file:
            json.dump(new_request, file)
            file.write("\n")

        return redirect(url_for("index"))

    return render_template("request.html", assignments=ASSIGNMENTS)


# Route for moderator login
@app.route("/moderator/login", methods=["GET", "POST"])
def moderator_login():
    if request.method == "POST":
        password = request.form.get("password")
        if password == MODERATOR_PASSWORD:
            # Log in the moderator and set session data
            session["moderator_logged_in"] = True
            session["logged_in_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Store login timestamp
            return redirect(url_for("moderator"))
        else:
            # Render the login page with an error message
            return render_template("moderator_login.html", error="Invalid password")

    # Render the login page
    return render_template("moderator_login.html")
@app.before_request
def check_session_timeout():
    if "logged_in_at" in session:
        # Calculate session age
        logged_in_at = session["logged_in_at"]
        logged_in_at_naive = datetime.datetime.strptime(logged_in_at, "%Y-%m-%d %H:%M:%S")

        if datetime.datetime.now() > logged_in_at_naive + SESSION_TIMEOUT:
            session.clear()
            return redirect(url_for("moderator_login"))

# Route for moderator approval page
@app.route("/moderator", methods=["GET", "POST"])
def moderator():
    if not session.get("moderator_logged_in"):
        return redirect(url_for("moderator_login"))

    if request.method == "POST":
        # Parse form data
        selected_value = request.form.get("role_initials")  # Format: "Shift 1 - Bar - RAC"
        
        # Extract shift, role, and initials
        parts = selected_value.split(" - ")
        print(parts, ASSIGNMENTS)
        shift = parts[0]
        role_or_person = parts[1]

        if shift in ["Shift 1", "Shift 2"]:
            role = parts[1]
            initials_to_remove = parts[2]
        else:
            initials_to_remove = parts[1]
        DO_NOT_ASSIGN.append(initials_to_remove)
        # Remove the person from their assigned task
        if shift == "Setup":
            ASSIGNMENTS["Setup"] = [p for p in ASSIGNMENTS["Setup"] if p != initials_to_remove]
        
        elif shift == "Cleanup":
            ASSIGNMENTS["Cleanup"] = [p for p in ASSIGNMENTS["Cleanup"] if p != initials_to_remove]

        elif shift in ["Shift 1", "Shift 2"]:
            if role in ASSIGNMENTS[f"{shift}"]:
                print(initials_to_remove)
                ASSIGNMENTS[f"{shift}"][role] = [p for p in ASSIGNMENTS[f"{shift}"][role] if p != initials_to_remove]

        # Assign a new person from the sorted list who is not already assigned
        for person in SORTED_PEOPLE:
            already_assigned = (
                person.initials in ASSIGNMENTS["Setup"]
                or person.initials in ASSIGNMENTS["Cleanup"]
                or any(person.initials in people for people in ASSIGNMENTS["Shift 1"].values())
                or any(person.initials in people for people in ASSIGNMENTS["Shift 2"].values())
            )
            if not already_assigned and not person.initials in DO_NOT_ASSIGN:
                if shift == "Setup":
                    ASSIGNMENTS["Setup"].append(person.initials)
                elif shift == "Cleanup":
                    ASSIGNMENTS["Cleanup"].append(person.initials)
                elif shift in ["Shift 1", "Shift 2"]:
                    if role not in ASSIGNMENTS[f"{shift}"]:
                        ASSIGNMENTS[f"{shift}"][role] = []
                    ASSIGNMENTS[f"{shift}"][role].append(person.initials) # Remove the assigned person from the sorted list
                break

        # Remove the approved request from the list
        pending_requests = load_requests()
        updated_requests = [
            req for req in pending_requests if not (req["initials"] == initials_to_remove and req["shift"] == shift and req.get("role") == role_or_person)
        ]
        save_requests(updated_requests)

        return redirect(url_for("moderator"))

    # Load pending requests from the file
    pending_requests = load_requests()
    return render_template("moderator.html", requests=pending_requests, assignments= ASSIGNMENTS, sorted_people = SORTED_PEOPLE[:])

# Route to log out the moderator
@app.route("/moderator/logout")
def moderator_logout():
    session.pop("moderator_logged_in", None)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
