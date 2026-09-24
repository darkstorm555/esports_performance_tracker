import tkinter as tk
from tkinter import messagebox
import sqlite3

def setup_database():
    """Creates the SQLite database and table if they do not exist."""
    conn = sqlite3.connect("match_history.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS player_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            kills INTEGER,
            deaths INTEGER,
            damage INTEGER,
            assists INTEGER,
            kd_ratio REAL,
            score REAL
        )
    ''')
    conn.commit()
    conn.close()

def calculate_and_save():
    """Calculates metrics and saves the record to the SQLite database."""
    try:
        player_name = name_entry.get()
        kills = int(kills_entry.get())
        deaths = int(deaths_entry.get())
        damage = int(damage_entry.get())
        assists = int(assists_entry.get())

        effective_deaths = deaths if deaths > 0 else 1
        kd_ratio = kills / effective_deaths
        score = (kills * 2) + assists + (damage / 100)

        # Connect to database and insert the new record
        conn = sqlite3.connect("match_history.db")
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO player_stats (name, kills, deaths, damage, assists, kd_ratio, score)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (player_name, kills, deaths, damage, assists, kd_ratio, score))
        conn.commit()
        conn.close()

        result_text = (
            f"--- {player_name.upper()} SAVED ---\n"
            f"K/D Ratio: {kd_ratio:.2f} | Score: {score:.2f}\n"
            f"Data successfully written to database."
        )
        result_label.config(text=result_text, fg="green")
        
        # Clear the input fields for the next entry
        name_entry.delete(0, tk.END)
        kills_entry.delete(0, tk.END)
        deaths_entry.delete(0, tk.END)
        damage_entry.delete(0, tk.END)
        assists_entry.delete(0, tk.END)
        
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers.")

def search_player():
    """Queries the database for all matches of a specific player and calculates averages."""
    player_name = search_entry.get()
    if not player_name:
        messagebox.showwarning("Input Error", "Please enter a player name to search.")
        return

    conn = sqlite3.connect("match_history.db")
    cursor = conn.cursor()
    # Fetch all records matching the player name (COLLATE NOCASE makes it case-insensitive)
    cursor.execute("SELECT kd_ratio, score FROM player_stats WHERE name = ? COLLATE NOCASE", (player_name,))
    records = cursor.fetchall()
    conn.close()

    if not records:
        search_result_label.config(text=f"No match history found for {player_name}.", fg="red")
        return

    # Calculate lifetime averages from the queried records
    total_matches = len(records)
    avg_kd = sum(row[0] for row in records) / total_matches
    avg_score = sum(row[1] for row in records) / total_matches

    search_result_text = (
        f"--- {player_name.upper()} LIFETIME STATS ---\n"
        f"Matches Played: {total_matches}\n"
        f"Average K/D: {avg_kd:.2f}\n"
        f"Average Score: {avg_score:.2f}"
    )
    search_result_label.config(text=search_result_text, fg="blue")

# Initialize the main window
app = tk.Tk()
app.title("Darkstorm Esports Tracker (Full Edition)")
app.geometry("380x650")
app.configure(padx=20, pady=20)

title_label = tk.Label(app, text="Player Database Tracker", font=("Arial", 14, "bold"))
title_label.pack(pady=(0, 10))

# --- DATA ENTRY SECTION ---
tk.Label(app, text="Player Name:").pack()
name_entry = tk.Entry(app)
name_entry.pack(pady=2)

tk.Label(app, text="Total Kills:").pack()
kills_entry = tk.Entry(app)
kills_entry.pack(pady=2)

tk.Label(app, text="Total Deaths:").pack()
deaths_entry = tk.Entry(app)
deaths_entry.pack(pady=2)

tk.Label(app, text="Total Damage:").pack()
damage_entry = tk.Entry(app)
damage_entry.pack(pady=2)

tk.Label(app, text="Total Assists:").pack()
assists_entry = tk.Entry(app)
assists_entry.pack(pady=2)

calc_button = tk.Button(app, text="Calculate & Save to DB", command=calculate_and_save, bg="black", fg="white")
calc_button.pack(pady=10)

result_label = tk.Label(app, text="Enter stats to save.", font=("Arial", 10), justify="center")
result_label.pack(pady=5)

# --- VISUAL SEPARATOR ---
tk.Frame(app, height=2, bd=1, relief="sunken").pack(fill="x", pady=10)

# --- SEARCH SECTION ---
search_title = tk.Label(app, text="Search Player History", font=("Arial", 12, "bold"))
search_title.pack(pady=(0, 5))

tk.Label(app, text="Enter Player Name:").pack()
search_entry = tk.Entry(app)
search_entry.pack(pady=2)

search_button = tk.Button(app, text="Fetch Stats", command=search_player, bg="blue", fg="white")
search_button.pack(pady=5)

search_result_label = tk.Label(app, text="Search results will appear here.", font=("Arial", 10), justify="center")
search_result_label.pack(pady=5)

if __name__ == "__main__":
    setup_database()
    app.mainloop()
