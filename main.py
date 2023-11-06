import sys
import warnings
from urllib3.exceptions import InsecureRequestWarning
from PyQt5 import QtWidgets, QtCore
import replay
import tkinter as tk
from tkinter import filedialog
import audio

def play_replay():
    current_time = manager.get_current_time()
    audio.play(current_time)
    response = manager.play()
    print(response)

def pause_replay():
    audio.pause()
    response = manager.pause()
    print(response)

audio = audio.Player
manager = replay.ReplayManager
