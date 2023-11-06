

import requests
import urllib3
import threading
import requests
import urllib3
import time
import pyaudiowpatch as pyaudio
import numpy as np
from pydub import AudioSegment
import pygame

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class Game_Live:
    def __init__(self, base_url="https://127.0.0.1:2999"):
        self.base_url = base_url
        self.endpoint = f"{self.base_url}/liveclientdata/gamestats"
        self.state = None

    def __getstate__(self):
        response = requests.get(self.endpoint, verify=False)
        response.raise_for_status()
        self.state = response.json()
        return self.state
    
    def get_current_time(self):
        if self.state is None:
            self.__getstate__()

        current_time_buffer = self.state.get('gameTime', 0) 

        self.__getstate__()
        current_time = self.state.get('gameTime', 0)

        if current_time_buffer == current_time:
            return "paused"
        else:
            return current_time
class Game_Replay:

    def __init__(self, base_url="https://127.0.0.1:2999"):
        self.base_url = base_url
        self.endpoint = f"{self.base_url}/replay/playback"
        self.state = None
        self.paused = False
        self.time = 0.0


    def get_state(self):
        response = requests.get(self.endpoint, verify=False)
        response.raise_for_status()
        self.state = response.json()
        return self.state

    def get_current_time(self):
        if self.state is None:
            self.get_state()

        current_time = self.state.get('time', 0) 
        return current_time

    def play(self):
        if self.state is None:
            self.get_state()
        
        response = requests.post(self.endpoint, json={'paused': False}, verify=False)
        response.raise_for_status()
        self.get_state()  # Update the local state after changing the server state
        return response.json()

    def pause(self):
        if self.state is None:
            self.get_state()
        
        response = requests.post(self.endpoint, json={'paused': True}, verify=False)
        response.raise_for_status()
        self.get_state()  # Update the local state after changing the server state
        return response.json()   
class Audio_Input:
    def __init__(self):
        self.recording = False
        self.start_time = None
        self.start_time = None
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 2
        self.RATE = 48000
        self.OUTPUT_FILENAME = "output.wav"
        self.audio = pyaudio.PyAudio()
        self.game_time = None

        self.loopback_device_index = None
        for i in range(self.audio.get_device_count()):
            device_info = self.audio.get_device_info_by_index(i)
            if "loopback" in device_info["name"].lower():
                self.loopback_device_index = i
                break
        if self.loopback_device_index is None:
            print("Default WASAPI loopback device not found. Please Make sure (Stereo Mix) is enabled in Control Panel / Input Devices.")
            exit(1)

        self.game_time_thread = threading.Thread(target=self.poll_game_time)
        self.game_time_thread.daemon = True  # Make the thread a daemon to exit with the main program
        self.game_time_thread.start()

    def start_recording(self):
        while Game_Live.get_current_time() == "paused":
            time.sleep(1)

        self.start_time = Game_Live.get_current_time()
        self.recording = True

            
        audio_thread = threading.Thread(target=self.audio_recording)
        audio_thread.start()

    def stop_recording(self):
        self.recording = False

    def poll_game_time(self):
        while True:
            self.game_time = Game_Live.get_current_time()
            time.sleep(0.25)

    def audio_recording(self):
        frames = []

        mic_stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            frames_per_buffer=self.CHUNK
        )

        team_stream = self.audio.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=self.RATE,
            input=True,
            input_device_index=self.loopback_device_index,
            frames_per_buffer=self.CHUNK
        )

        print("Recording...")
        print(self.start_time)

        while self.recording:
            mic_data = mic_stream.read(self.CHUNK)
            team_data = team_stream.read(self.CHUNK)

            if self.game_time != "paused":
                mic_array = np.frombuffer(mic_data, dtype=np.int16)
                team_array = np.frombuffer(team_data, dtype=np.int16)

                if len(mic_array) == len(team_array):
                    combined_audio = mic_array + team_array
                    combined_data = combined_audio.tobytes()
                    frames.append(combined_data)

        print("Recording stopped.")

        mic_stream.stop_stream()
        mic_stream.close()
        team_stream.stop_stream()
        team_stream.close()
        self.audio.terminate()

        if self.start_time is not None:
            delay = self.start_time
            if delay > 0:
                delay_frames = int(delay * self.RATE)
                blank_frames = b'\x00' * (delay_frames * self.CHANNELS * 2)
                frames = [blank_frames] + frames

        audio_data = b''.join(frames)
        audio_segment = AudioSegment(
            audio_data,
            sample_width=self.audio.get_sample_size(self.FORMAT),
            frame_rate=self.RATE,
            channels=self.CHANNELS
        )
        
        audio_segment.export(self.OUTPUT_FILENAME, format="mp3")
class Audio_Output:

    
    def __init__(self):
        self.paused = False
        self.path = None  # Initialize path as None

    def start_player(self, path):
        self.path = path  # Set the path when starting playback
        pygame.mixer.music.load(path)
        pygame.mixer.music.play()

    def play(self, game_time):
        if self.path:
            if self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
            else:
                pygame.mixer.music.set_pos(game_time)
                pygame.mixer.music.play()
                self.paused = False

    def pause(self):
        if self.path:
            if not self.paused:
                pygame.mixer.music.pause()
                self.paused = True


