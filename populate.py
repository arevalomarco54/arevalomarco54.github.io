import json


def save_people_to_json(data, filename="people_data.json"):
    """
    Saves a list of tuples (initials, points, seniority) to a JSON file.

    Args:
        data (list of tuples): List of tuples in the format ("initials", "points", "seniority").
        filename (str): The name of the JSON file to save the data to.

    Example:
        save_people_to_json(
            [("RAC", 10, 1), ("DOM", 5, 2), ("AXC", 15, 1)],
            "people_data.json"
        )
    """
    # Convert the list of tuples into a list of dictionaries
    people = [
        {"initials": initials, "points": points, "seniority": seniority}
        for initials, points, seniority in data
    ]

    # Save the list of dictionaries to a JSON file
    with open(filename, "w") as file:
        json.dump(people, file, indent=4)

    print(f"Data successfully saved to {filename}")


all = [
    ("MXT", 1, 4),
    ("IJM", 0, 4),
    ("VXK", 0, 4),
    ("EOO", 0, 4),
    ("VXK", 0, 4),
    ("TWK", 0, 4),
    ("RPK", 0, 4),
    ("TLM", 0, 4),
    ("JCE", 0, 4),
    ("MXP", 1, 3),
    ("FXL", 1, 3),
    ("AXZ", 1, 3),
    ("JDD", 1, 3),
    ("KXW", 1, 3),
    ("FGP", 1, 3),
    ("GXD", 1, 3),
    ("JXL", 1, 3),
    ("AXS", 1, 3),
    ("NCK", 1, 3),
    ("AJH", 1, 3),
    ("DJL", 0, 2),
    ("INR", 1, 2),
    ("AXC", 1, 2),
    ("JJN", 1, 2),
    ("MJC", 1, 2),
    ("ECA", 1, 2),
    ("YKL", 1, 2),
    ("GDM", 1, 2),
    ("CRW", 1, 2),
    ("JIJ", 0, 2),
    ("SJC", 0, 2),
    ("DOM", 1, 1),
    ("KLY", 0, 1),
    ("ALL", 0, 1),
    ("RAC", 1, 1),
    ("MRA", 1, 1),
    ("BXW", 1, 1),
    ("HAW", 0, 1),
    ("VDS", 1, 1),
    ("THN", 1, 1),
    ("SXZ", 0, 1),
    ("BJL", 1, 1),
    ("BXL", 0, 1),
]
save_people_to_json(all)
