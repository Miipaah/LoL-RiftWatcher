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
game_active = False
start_time = None
def get_game_time():
    global game_time
    global game_active
    while True:
        #print(game_active)
        pause_buffer = get_data(game_stats_url)["gameTime"]
        time.sleep(0.25)
        current_game_time = get_data(game_stats_url)["gameTime"]
        if current_game_time is not None:
            if current_game_time != pause_buffer:
                game_time = current_game_time
                game_active = True
            else:
                game_active= False

                game_time = "Paused"
        else:
            game_time = None
            print("Could not Retreive GameTime")
        
        

timer_thread = threading.Thread(target=get_game_time)
timer_thread.start()

import pyaudio
import wave
import threading

# Global variable to control recording
recording = False

def audio_recording():
    global recording
    global start_time

    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    OUTPUT_FILENAME = "output.wav"

    audio = pyaudio.PyAudio()

    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    frames = []

    print("Recording...")
    start_time = get_data(game_stats_url)["gameTime"]
    print(start_time)

    while recording:
        data = stream.read(CHUNK)
        if game_active:
            frames.append(data)
        else:
            pass

    print("Recording stopped.")

    stream.stop_stream()
    stream.close()
    audio.terminate()

    if start_time is not None:
        delay = start_time
        if delay > 0:
            delay_frames = int(delay * RATE)
            blank_frames = b'\x00' * (delay_frames * CHANNELS * 2)  # Silence frames
            frames = [blank_frames] + frames

    wf = wave.open(OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))  # Convert frames to bytes before writing
    wf.close()

def start_recording():
    global recording
    recording = True
    audio_thread = threading.Thread(target=audio_recording)
    audio_thread.start()

def stop_recording():
    global recording
    recording = False


if __name__ == "__main__":
    start_recording()
    
    input("Press Enter to stop recording...")
    stop_recording()
    exit()
exit(); 
