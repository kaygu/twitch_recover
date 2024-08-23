from PyQt6.QtCore import QDateTime, Qt, QTimer
from PyQt6.QtWidgets import (QApplication, QMainWindow, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)

from connectors.sullygnome import SullygnomeConnector


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.originalPalette = QApplication.palette()  

        self.createUsernamesGroupBox()
        self.createTimePeriodGroupBox()

    
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.usernamesGroupBox, 0, 0)
        mainLayout.addWidget(self.timePeriodGroupBox, 1, 0)

        mainLayout.setRowStretch(0, 1)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)

        container = QWidget()
        container.setLayout(mainLayout)
        self.setCentralWidget(container)

        self.setWindowTitle("Twitch Bulk Download")

    def onUsernameButtonPressed(self, usernames:str):
        # Do research for the twitch usernames
        connector = SullygnomeConnector()
        # TODO: If twitchTracker fails, try other services (like sullygname)
        print(f"Button Pressed, searching for")
        for n in usernames.split(';'):
            print(n)
            connector.get_past_vods(n, True)
        self.usernamesGroupBox.setDisabled(True)

    def createUsernamesGroupBox(self):
        self.usernamesGroupBox = QGroupBox("Twitch Usernames")

        usernames = QLineEdit('iitztimmy')
        usernames.setEchoMode(QLineEdit.EchoMode.Normal)

        button = QPushButton("Search VODs")
        button.clicked.connect(lambda: self.onUsernameButtonPressed(usernames.text()))

        layout = QGridLayout()
        layout.addWidget(usernames, 0, 0, 1, 2)
        layout.addWidget(button, 1, 1, 1, 1)

        self.usernamesGroupBox.setLayout(layout)


    def createTimePeriodGroupBox(self):
        self.timePeriodGroupBox = QGroupBox("Timestamps")

        # Add label for start & end timestamps
        dateTimeStart = QDateTimeEdit(self.timePeriodGroupBox)
        dateTimeStart.setDateTime(QDateTime.currentDateTime())

        dateTimeEnd = QDateTimeEdit(self.timePeriodGroupBox)
        dateTimeEnd.setDateTime(QDateTime.currentDateTime())

        # TODO: Add option, either enter start & end timestamp or only start & duration 

        layout = QHBoxLayout()
        layout.addWidget(dateTimeStart)
        layout.addWidget(dateTimeEnd)

        self.timePeriodGroupBox.setLayout(layout)



if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())