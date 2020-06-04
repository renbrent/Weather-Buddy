import sys, requests
from PySide2.QtCore import Qt, QUrl
from PySide2.QtWidgets import (QApplication, QInputDialog, QHeaderView, QHBoxLayout, QLabel, QLineEdit,
                               QMainWindow, QMessageBox, QPushButton, QSizePolicy, QSlider,
                               QStyle, QVBoxLayout, QWidget)
from PySide2.QtMultimedia import QMediaPlayer
from PySide2.QtGui import QIcon

# URLS for Current and 5 day/ 3 hour forecast
urls = [
    "https://community-open-weather-map.p.rapidapi.com/weather",
    "https://community-open-weather-map.p.rapidapi.com/forecast"
]

headers = {
    'x-rapidapi-host': "community-open-weather-map.p.rapidapi.com",
    'x-rapidapi-key': ""
    }

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setFixedSize(1200,800)
        self.setWindowTitle("Weather Buddy")


def main():
    f = open("SECRET_KEY.txt", "r")
    headers['x-rapidapi-key'] = f
    f.close()

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec_())



if __name__ == "__main__":
    main()