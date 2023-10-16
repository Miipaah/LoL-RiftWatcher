import threading
import requests
import urllib3
import time
import wave
import pyaudiowpatch as pyaudio
import numpy as np

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

#global vars
game_time = None
game_active = False
start_time = None


def get_game_time():
    global game_time
    global game_active
    while True:

        #reset game time to previous value
        pause_buffer = get_data(game_stats_url)["gameTime"]
        time.sleep(0.25)
        current_game_time = get_data(game_stats_url)["gameTime"]
        
        #if game time is returned check if same as last value
        if current_game_time is not None:

            #different value from last  = game progress
            if current_game_time != pause_buffer:
                game_time = current_game_time
                game_active = True
            else:

                #same value = game pause
                game_active= False

                game_time = "Paused"
        else:
            game_time = None
            print("Could not Retreive GameTime")
        
        
#start Global timer and Pause detection via Threader
timer_thread = threading.Thread(target=get_game_time)
timer_thread.start()


# Global variable to control recording
recording = False

def audio_recording():
    global recording
    global start_time

#Wav Audio parameters
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 48000
    OUTPUT_FILENAME = "output.wav"
 

    audio = pyaudio.PyAudio()

    #scan devices for index of Stereo Mix for Desktop Audio (Game Audio)

    loopback_device_index = None
    for i in range(audio.get_device_count()):
        device_info = audio.get_device_info_by_index(i)
        if "loopback" in device_info["name"].lower():
            loopback_device_index = i
            break

    if loopback_device_index is None:
        print("Default WASAPI loopback device not found. Please specify the correct device index.")
        exit(1)
    

    #Record Default Microphone Input

    mic_stream = audio.open(

                format=FORMAT, 
                channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK

                )
    #Record Defualt Stereo Mix: Loopback

    team_stream = audio.open(

                format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=loopback_device_index,
                frames_per_buffer=CHUNK

                )

    frames = []

    print("Recording...")
    start_time = get_data(game_stats_url)["gameTime"]
    print(start_time)

#only appends audio chuinks if game is Active (not Paused)
    while recording:
        mic_data = mic_stream.read(CHUNK)
        team_data = team_stream.read(CHUNK)
        if game_active:
                        # Convert the binary audio data to NumPy arrays
            mic_array = np.frombuffer(mic_data, dtype=np.int16)
            team_array = np.frombuffer(team_data, dtype=np.int16)

            # Check if the arrays have the same length
            if len(mic_array) == len(team_array):
                # Mix the audio by adding the samples together
                combined_audio = mic_array + team_array

                # Convert the combined audio back to binary data
                combined_data = combined_audio.tobytes()

                frames.append(combined_data)
            else:
                print("Audio frame length mismatch. Skipping frame.")
        else:
            #skip frames when Active is False
            pass

    print("Recording stopped.")

    mic_stream.stop_stream()
    mic_stream.close()
    team_stream.stop_stream()
    team_stream.close()
    audio.terminate()

#gametime recording started is added on as deadAudio for Syncing
    if start_time is not None:
        delay = start_time
        if delay > 0:
            delay_frames = int(delay * RATE)
            #adds blank chunks containing only timecode data
            blank_frames = b'\x00' * (delay_frames * CHANNELS * 2)  # Silence frames
            frames = [blank_frames] + frames

#generates wav file based on stored frames[]
    wf = wave.open(OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))  # Convert frames to bytes before writing
    wf.close()

#starts record stream
def start_recording():
    global recording
    recording = True
    audio_thread = threading.Thread(target=audio_recording)
    audio_thread.start()

#stops record stream
def stop_recording():
    global recording
    recording = False

#Test Loop
if __name__ == "__main__":
    start_recording()
    
    input("Press Enter to stop recording...")
    stop_recording()
    exit()
exit(); 
