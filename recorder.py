import threading
import requests
import urllib3
import time
import pyaudiowpatch as pyaudio
import numpy as np
from game import LiveGame
from pydub import AudioSegment
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class Recorder:
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
        while live_game.get_current_time() == "paused":
            time.sleep(1)
    
        self.start_time = live_game.get_current_time()
        self.recording = True

            
        audio_thread = threading.Thread(target=self.audio_recording)
        audio_thread.start()

    def stop_recording(self):
        self.recording = False

    def poll_game_time(self):
        while True:
            self.game_time = live_game.get_current_time()
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




    


#Test Loop


if __name__ == "__main__":
    live_game = LiveGame()
    recorder = Recorder()

    recorder.start_recording()
    
    input("Press Enter to stop recording...")
    recorder.stop_recording()
    exit()
exit();   

