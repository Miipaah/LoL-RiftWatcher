import tkinter
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

# Get events data (if needed)
get_data(events_url)

# Get initial game time
initial_game_time = get_data(game_stats_url)["gameTime"]

def timer():
    while True:
        current_game_time = get_data(game_stats_url)["gameTime"]
        time_difference = current_game_time - initial_game_time
        
        print(f"Game Time: {current_game_time:.2f} seconds")
        print(f"Time Difference: {time_difference:.2f} seconds")
        
        initial_game_time = current_game_time  # Update initial_game_time
        
        # Sleep for 1 second minus the time taken for the request
import tkinter
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

# Get events data (if needed)
get_data(events_url)

# Get initial game time
initial_game_time = get_data(game_stats_url)["gameTime"]

def format_time(milliseconds):
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}:{milliseconds:03d}"

def timer():
    while True:
        current_game_time = get_data(game_stats_url)["gameTime"]
        formatted_time = format_time(int(current_game_time * 1000))
        
        print(f"Game Time: {formatted_time}")
        
        
        # Sleep for 1 second minus the time taken for the request
        time.sleep(.25)

timer_thread = threading.Thread(target=timer)
timer_thread.start()

# Create a simple tkinter window for demonstration (optional)
root = tkinter.Tk()
root.geometry("200x100")
root.title("Game Time Monitor")

label = tkinter.Label(root, text="Game Time:")
label.pack()

game_time_label = tkinter.Label(root, text="00:00:00:000")
game_time_label.pack()

def update_game_time_label():
    while True:
        current_game_time = get_data(game_stats_url)["gameTime"]
        formatted_time = format_time(int(current_game_time * 1000))
        game_time_label.config(text=formatted_time)
        root.update()
        time.sleep(.25)

update_thread = threading.Thread(target=update_game_time_label)
update_thread.start()

root.mainloop()
