# esports_performance_tracker

# Darkstorm Esports Performance Tracker 🎮

A lightweight, standalone desktop application built in Python to calculate and store post-match esports statistics. 

## 📝 Project Overview
This tool is designed to quickly calculate a player's Kill/Death (K/D) ratio and a custom 'Combat Score' based on their in-game performance. To ensure data is not lost between sessions, the application automatically provisions a local SQLite database to permanently store match records.

## ✨ Key Features
* **Interactive GUI:** User-friendly interface built with Python's built-in `tkinter` library.
* **Automated Math:** Safely calculates K/D ratios (including division-by-zero handling) and aggregates weighted stats for MVP scoring.
* **Data Persistence:** Uses `sqlite3` to automatically create a database (`match_history.db`) and insert new records via SQL queries.

## 🛠️ Tech Stack
* **Language:** Python 3
* **Interface:** Tkinter (Python Standard Library)
* **Database:** SQLite3 (Python Standard Library)

## 🧑‍💻 How to Run Locally
1. Download the repository files to your local machine.
2. Ensure you have Python installed. No external dependencies are required.
3. Open your terminal, navigate to the project folder, and run the following command:
   ```bash
   python gui_tracker.py
