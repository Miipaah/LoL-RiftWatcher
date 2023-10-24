import sys
import warnings
from urllib3.exceptions import InsecureRequestWarning
from PyQt5 import QtWidgets, QtCore
import playback
import replay
import tkinter as tk
from tkinter import filedialog

class DraggableWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.m_drag = False
        self.m_DragPosition = QtCore.QPoint()

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

        self.setStyleSheet("""
            DraggableWidget {
                background-color: rgba(128, 128, 128, 128);
            }
            QPushButton {
                background-color: rgba(255, 255, 255, 200);
            }
        """)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.m_drag = True
            self.m_DragPosition = event.globalPos() - self.pos()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(event.globalPos() - self.m_DragPosition)
            event.accept()

    def mouseReleaseEvent(self, event):
        self.m_drag = False

def play_replay():
    current_time = manager.get_current_time()
    audio.play(current_time)
    response = manager.play()
    print(response)

def pause_replay():
    audio.pause()
    response = manager.pause()
    print(response)

def browse_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        file_name = file_path.split("/")[-1]  # Get the name of the selected file
        file_label.config(text=f"Selected File: {file_name}")
        # Update the 'file' variable with the selected file path
        global file
        file = file_path

if __name__ == "__main__":
    warnings.simplefilter('ignore', InsecureRequestWarning)
    file = "select file"
    manager = replay.ReplayManager()
    audio = playback.player(file)
    app = QtWidgets.QApplication(sys.argv)

    window = DraggableWidget()
    window.setWindowTitle("Replay Controller")
    window.setWindowFlags(window.windowFlags() | QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)

    play_button = QtWidgets.QPushButton('Play')
    play_button.clicked.connect(play_replay)
    window.layout.addWidget(play_button)

    pause_button = QtWidgets.QPushButton('Pause')
    pause_button.clicked.connect(pause_replay)
    window.layout.addWidget(pause_button)

    # Create a button for file selection
    browse_button = QtWidgets.QPushButton('Browse File')
    browse_button.clicked.connect(browse_file)
    window.layout.addWidget(browse_button)

    # Create a label to display the selected file name
    file_label = QtWidgets.QLabel('Selected File: None')
    window.layout.addWidget(file_label)

    window.show()

    sys.exit(app.exec())
