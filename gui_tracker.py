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

# Initialize the main window
app = tk.Tk()
app.title("Darkstorm Esports Tracker (Database Edition)")
app.geometry("350x450")
app.configure(padx=20, pady=20)

title_label = tk.Label(app, text="Player Database Tracker", font=("Arial", 14, "bold"))
title_label.pack(pady=(0, 15))

# Input fields
tk.Label(app, text="Player Name:").pack()
name_entry = tk.Entry(app)
name_entry.pack(pady=5)

tk.Label(app, text="Total Kills:").pack()
kills_entry = tk.Entry(app)
kills_entry.pack(pady=5)

tk.Label(app, text="Total Deaths:").pack()
deaths_entry = tk.Entry(app)
deaths_entry.pack(pady=5)

tk.Label(app, text="Total Damage:").pack()
damage_entry = tk.Entry(app)
damage_entry.pack(pady=5)

tk.Label(app, text="Total Assists:").pack()
assists_entry = tk.Entry(app)
assists_entry.pack(pady=5)

calc_button = tk.Button(app, text="Calculate & Save to DB", command=calculate_and_save, bg="black", fg="white")
calc_button.pack(pady=15)

result_label = tk.Label(app, text="Enter stats to save.", font=("Arial", 11), justify="left")
result_label.pack(pady=10)

if __name__ == "__main__":
    setup_database() # Ensure the database exists before the window opens
    app.mainloop()
