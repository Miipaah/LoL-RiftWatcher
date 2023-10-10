import threading
import requests
import urllib3
import time

# Define the URLs for the endpoints
events_url = "https://127.0.0.1:2999/liveclientdata/eventdata"
game_stats_url = "https://127.0.0.1:2999/liveclientdata/gamestats"

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Function to send a GET request and retrieve data while ignoring SSL
def get_data(endpoint_url):
    try:
        response = requests.get(endpoint_url, verify=False)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()  # Parse JSON response
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

game_time = None
def get_game_time():
    global game_time
    while True:
        print(game_time)
        pause_buffer = get_data(game_stats_url)["gameTime"]
        time.sleep(0.25)
        current_game_time = get_data(game_stats_url)["gameTime"]
        if current_game_time is not None:
            if current_game_time != pause_buffer:
                game_time = current_game_time
            else:
                game_time = "Paused"
        else:
            game_time = None
            print("Could not Retreive GameTime")
        
        

timer_thread = threading.Thread(target=get_game_time)
timer_thread.start()
