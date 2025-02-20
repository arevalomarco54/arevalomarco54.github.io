import tkinter as tk
from tkinter import messagebox
import random
import json

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

# Save updated people data to the JSON file
def save_people(people, filename="people_data.json"):
    data = [{"initials": p.initials, "seniority": p.seniority, "points": p.points} for p in people]
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

# Function to sort people based on assignment priority
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
def assign_tasks(sorted_people):
    tasks = {
        "Setup": 3,
        "During": {
            "Bar": 2,
            "Couch": 1,
            "Inner Door": 1,
            "Coat Check": 1,
            "Table": 1,
            "Outer Door": 2,
            "Sober": 2,
            "DJ": 1
        },
        "Shifts": {
            "Shift 1 (9:45-11:00)": {},
            "Shift 2 (11:00-12:15AM)": {}
        },
        "Cleanup": 3
    }

    assignments = {"Setup": [], "Shifts": {}, "Cleanup": []}

    # Assign Setup tasks
    for _ in range(tasks["Setup"]):
        if sorted_people:
            person = sorted_people.pop(0)
            assignments["Setup"].append(person.initials)

    # Assign Shift tasks (split into two shifts)
    for shift in tasks["Shifts"]:
        assignments["Shifts"][shift] = {}
        for role, count in tasks["During"].items():
            assignments["Shifts"][shift][role] = []
            for _ in range(count):
                if sorted_people:
                    person = sorted_people.pop(0)
                    assignments["Shifts"][shift][role].append(person.initials)

    # Assign Cleanup tasks
    for _ in range(tasks["Cleanup"]):
        if sorted_people:
            person = sorted_people.pop(0)
            assignments["Cleanup"].append(person.initials)

    return assignments

# GUI Application
class TaskAssignerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Assigner")
        
        # Load and sort people
        self.people = load_people()
        self.sorted_people = sort_people(self.people)
        
        # Assign tasks
        self.assignments = assign_tasks(self.sorted_people)
        
        # Create GUI elements
        self.create_gui()
    
    def create_gui(self):
        tk.Label(self.root, text="Task Assignments", font=("Arial", 16)).grid(row=0, column=0, columnspan=2)

        row_index = 1
        
        # Display Setup tasks
        tk.Label(self.root, text="Setup", font=("Arial", 14)).grid(row=row_index, column=0, sticky="w")
        row_index += 1
        for person in self.assignments["Setup"]:
            tk.Label(self.root, text=f"{person}", font=("Arial", 12)).grid(row=row_index, column=0, sticky="w")
            row_index += 1
        
        # Display Shifts and During tasks
        for shift_name, roles in self.assignments["Shifts"].items():
            tk.Label(self.root, text=f"{shift_name}", font=("Arial", 14)).grid(row=row_index, column=0, sticky="w")
            row_index += 1
            for role, people in roles.items():
                tk.Label(self.root, text=f"{role}: {', '.join(people)}", font=("Arial", 12)).grid(row=row_index, column=0, sticky="w")
                row_index += 1

        # Display Cleanup tasks
        tk.Label(self.root, text="Cleanup", font=("Arial", 14)).grid(row=row_index, column=0, sticky="w")
        row_index += 1
        for person in self.assignments["Cleanup"]:
            tk.Label(self.root, text=f"{person}", font=("Arial", 12)).grid(row=row_index, column=0, sticky="w")
            row_index += 1
        
        # Save button to update JSON file with new points (if needed)
        tk.Button(self.root, text="Save & Exit", command=self.save_and_exit).grid(row=row_index + 1, column=0)

    def save_and_exit(self):
        save_people(self.people)
        messagebox.showinfo("Saved", "Assignments saved successfully!")
        self.root.destroy()

# Main function to run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskAssignerApp(root)
    root.mainloop()
