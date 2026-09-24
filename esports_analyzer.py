import json

def load_match_data(filepath):
    """Reads the JSON file and returns the data."""
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: The file {filepath} was not found.")
        return None

def analyze_match(data):
    """Processes the match data to calculate team and player statistics."""
    print(f"\n--- Match Summary: {data['squad_name']} ---")
    print(f"Map: {data['map']} | Placement: #{data['placement']} | Duration: {data['duration_minutes']} mins\n")
    
    total_team_kills = 0
    total_team_damage = 0
    mvp = None
    highest_score = -1

    # Print the table header
    print(f"{'Player':<15} | {'K/D Ratio':<10} | {'Damage':<8} | {'Assists'}")
    print("-" * 55)

    for player in data['players']:
        # Calculate K/D Ratio (handle division by zero if deaths are 0)
        deaths = player['deaths'] if player['deaths'] > 0 else 1
        kd_ratio = player['kills'] / deaths
        
        # Track overall team totals
        total_team_kills += player['kills']
        total_team_damage += player['damage']
        
        # Determine MVP based on a custom formula: Kills(x2) + Assists(x1) + (Damage / 100)
        player_score = (player['kills'] * 2) + player['assists'] + (player['damage'] / 100)
        if player_score > highest_score:
            highest_score = player_score
            mvp = player['name']
            
        # Display individual stats formatting float to 2 decimal places
        print(f"{player['name']:<15} | {kd_ratio:<10.2f} | {player['damage']:<8} | {player['assists']}")

    print("-" * 55)
    print(f"Total Team Kills: {total_team_kills}")
    print(f"Total Team Damage: {total_team_damage}")
    print(f"Match MVP: {mvp} 🏆\n")

if __name__ == "__main__":
    # Define the file we want to read
    file_path = "match_data.json"
    
    # Load the data
    match_data = load_match_data(file_path)
    
    # If the data loaded successfully, run the analysis
    if match_data:
        analyze_match(match_data)
