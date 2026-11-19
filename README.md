
# RPG Build Planner

A desktop application for browsing, filtering, and comparing RPG weapons based on their attributes and character requirements.

RPG Build Planner helps players find suitable weapons by analyzing damage, weight, Strength requirements, Dexterity requirements, and scaling attributes.

The project was developed in Python as a portfolio project focused on application development, database integration, GUI design, and software testing.

## Features

- Browse a collection of 40 RPG weapons.
- Filter weapons by category.
- Filter by maximum Strength requirement.
- Filter by maximum Dexterity requirement.
- Filter by maximum weapon weight.
- Combine multiple filtering criteria.
- Sort weapons by damage (ascending and descending).
- Sort weapons by weight (ascending and descending).
- Display the three highest-damage weapons in featured cards.
- View all weapons in a structured table.
- Store weapon data in an SQLite database.
- Automatically initialize the database and import data from JSON when needed.
- Run the application through either a command-line interface or a graphical user interface.

## Screenshots

<!-- Add application screenshots here. -->

## Technologies

- Python
- Tkinter and ttk
- SQLite
- JSON
- unittest

## Project Structure

```text
RPG_Build_Planner/
│
├── data/
│   ├── items.json
│   └── items.db          # Generated locally
│
├── tests/
│   ├── __init__.py
│   ├── test_items.py
│   └── test_database.py
│
├── main.py
├── database.py
├── gui.py
├── gui_backup.py
├── README.md
└── .gitignore
```

## Requirements

- Python 3.10 or newer
- Tkinter support

No additional third-party Python packages are required.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/jjannowak/RPG_Build_Planner.git
```

2. Navigate to the project directory:

```bash
cd RPG_Build_Planner
```

3. Run the graphical interface:

```bash
python gui.py
```

The application automatically creates the SQLite database and imports weapon data from `data/items.json` when the database is empty.

## Command-Line Interface

To run the command-line version:

```bash
python main.py
```

Follow the instructions displayed in the terminal to filter and sort weapons.

## Running Tests

Run the automated test suite using:

```bash
python -m unittest discover -v
```

The test suite covers weapon data validation, filtering, sorting, database initialization, and JSON data import.

## Database

Weapon data is stored in `data/items.json` as the source dataset.

SQLite is used for local data storage. The database file (`items.db`) is generated automatically and is excluded from version control.

## Project Goals

This project demonstrates practical skills in:

- Python application development.
- Object-independent functional programming and modular code organization.
- GUI development with Tkinter.
- Relational database management with SQLite.
- JSON data handling.
- Automated testing with unittest.
- Building and maintaining a structured software project.

## License

This project is currently intended for educational and portfolio purposes.
