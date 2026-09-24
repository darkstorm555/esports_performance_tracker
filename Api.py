from fastapi import FastAPI, HTTPException
import json

# Initialize the FastAPI application
app = FastAPI(title="Esports Match API")

def load_data():
    """Helper function to load our mock database."""
    try:
        with open("match_data.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return None

@app.get("/")
def read_root():
    """The home endpoint verifying the API is running."""
    return {"message": "Welcome to the Esports Analytics API!"}

@app.get("/match/summary")
def get_match_summary():
    """Returns the full match data and calculates the team MVP."""
    data = load_data()
    if not data:
        # Handle the error gracefully if the file is missing
        raise HTTPException(status_code=404, detail="Match data not found")
    
    highest_score = -1
    mvp = None
    
    # Calculate MVP just like our terminal script
    for player in data["players"]:
        score = (player["kills"] * 2) + player["assists"] + (player["damage"] / 100)
        if score > highest_score:
            highest_score = score
            mvp = player["name"]
            
    # Add our calculated MVP to the response dictionary
    data["calculated_mvp"] = mvp
    return data

@app.get("/player/{player_name}")
def get_player_stats(player_name: str):
    """Searches for a specific player and calculates their K/D ratio."""
    data = load_data()
    if not data:
        raise HTTPException(status_code=500, detail="Database error")
        
    for player in data["players"]:
        if player["name"].lower() == player_name.lower():
            # Calculate K/D Ratio
            deaths = player["deaths"] if player["deaths"] > 0 else 1
            kd_ratio = player["kills"] / deaths
            
            # Return just this player's stats plus the new calculation
            return {
                "name": player["name"],
                "kills": player["kills"],
                "kd_ratio": round(kd_ratio, 2),
                "damage": player["damage"]
            }
            
    # If the loop finishes and no player is found, return a 404 error
    raise HTTPException(status_code=404, detail="Player not found in this match")
