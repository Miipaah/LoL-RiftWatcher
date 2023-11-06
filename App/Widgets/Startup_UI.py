from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel, QSlider, QVBoxLayout, QFileDialog
from PySide6.QtCore import Qt, QPoint, QFileInfo
from PySide6.QtGui import QFontMetrics
import sys

class RecordPage(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        
        self.label = QLabel("Recording Page")
        self.timer_label = QLabel("00:00:00")

        self.start_button = QPushButton("Start Recording")
        self.start_button.setStyleSheet("background-color: rgba(30, 30, 30, 191); color: white;")

        layout.addWidget(self.label)
        layout.addWidget(self.timer_label)
        layout.addWidget(self.start_button)

        # Set label text color to white
        self.label.setStyleSheet("color: white;")
        self.timer_label.setStyleSheet("color: white;")

class ReplayPage(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        self.label = QLabel("Replay Page")
        self.play_pause_button = QPushButton("Play")
        self.sync_button = QPushButton("Sync")
        self.mute_button = QPushButton("Mute")
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)

        self.play_pause_button.setStyleSheet("background-color: rgba(30, 30, 30, 191); color: white;")
        self.sync_button.setStyleSheet("background-color: rgba(30, 30, 30, 191); color: white;")
        self.mute_button.setStyleSheet("background-color: rgba(30, 30, 30, 191); color: white;")
        self.play_pause_button.setCheckable(True)
        self.play_pause_button.setChecked(False)
        self.mute_button.setCheckable(True)
        self.mute_button.setChecked(False)

        self.open_file_button = QPushButton("Open File")
        self.open_file_button.setStyleSheet("background-color: rgba(30, 30, 30, 191); color: white;")
        self.open_file_button.clicked.connect(self.open_file_dialog)
        self.volume_label = QLabel("Volume Slider")
        self.volume_label.setStyleSheet("color: white;")

        self.selected_file_label = QLabel("Selected File: None")
        self.selected_file_label.setStyleSheet("color: white;")

        layout.addWidget(self.label)
        layout.addWidget(self.play_pause_button)
        layout.addWidget(self.mute_button)
        layout.addWidget(self.sync_button)
        layout.addWidget(self.volume_label)
        layout.addWidget(self.volume_slider)
        layout.addWidget(self.open_file_button)
        layout.addWidget(self.selected_file_label)

        # Set label text color to white
        self.label.setStyleSheet("color: white;")

    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_dialog = QFileDialog(self)
        file_dialog.setOptions(options)
        file_dialog.setNameFilter("Audio Files (*.WAV *.MP3);;All Files (*)")

        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            if selected_files:
                selected_file = selected_files[0]
                # Extract the file name from the full path
                file_info = QFileInfo(selected_file)
                file_name = file_info.fileName()

                self.selected_file_label.setText(f"Selected File: {file_name}")
                # Set the maximum width of the label to prevent resizing
                max_label_width = 150  # Adjust as needed
                self.selected_file_label.setMaximumWidth(max_label_width)

                # Create a font metrics object to calculate elided text
                font_metrics = QFontMetrics(self.font())

                # Calculate the elided text
                elided_text = font_metrics.elidedText(file_name, Qt.ElideMiddle, max_label_width)

                self.selected_file_label.setText(f"Selected File: {elided_text}")

class DraggableWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Draggable Window")
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setGeometry(100, 100, 100, 150)
        self.setStyleSheet("background-color: #121212;")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.record_button = QPushButton("🔴 RECORD")
        self.replay_button = QPushButton("⏯️ REPLAY")
        self.exit_button = QPushButton("❎ EXIT")

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.record_button)
        layout.addWidget(self.replay_button)
        layout.addWidget(self.exit_button)

        self.record_button.setStyleSheet("background-color: rgba(30, 30, 30, 191); color: white;")
        self.replay_button.setStyleSheet("background-color: rgba(30, 30, 30, 191); color: white;")
        self.exit_button.setStyleSheet("background-color: rgba(30, 30, 30, 191); color: white;")

        if sys.platform == 'win32':
            self.central_widget.setStyleSheet("QDialogTitleBar { background-color: #333; color: white; }")

        self.dragging = False
        self.offset = QPoint()

        self.record_page = RecordPage()
        self.replay_page = ReplayPage()

        self.current_page = self.record_page

        self.record_button.clicked.connect(self.show_record_page)
        self.replay_button.clicked.connect(self.show_replay_page)

    def show_record_page(self):
        self.setCentralWidget(self.record_page)
        self.current_page = self.record_page

    def show_replay_page(self):
        self.setCentralWidget(self.replay_page)
        self.current_page = self.replay_page

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragging = True
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.dragging:
            self.move(self.mapToGlobal(event.pos() - self.offset))

    def mouseReleaseEvent(self, event):
        if self.dragging:
            self.dragging = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DraggableWindow()
    window.show()
    sys.exit(app.exec_())
