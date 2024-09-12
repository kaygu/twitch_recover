from PyQt6.QtCore import QDateTime, Qt, QTimer
from PyQt6.QtWidgets import (QApplication, QMainWindow, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)

from connectors.sullygnome import SullygnomeConnector
from utils.format import str_to_datetime


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
        connector = SullygnomeConnector() # TODO: Develop other connectors in case the current service fails
        self.usernamesGroupBox.setDisabled(True)
        for n in usernames.split(';'):
            for vod in connector.get_past_vods(n, verbose=False):
                streamID, timestamp, start_time_str, end_time_str = vod
                start_datetime = str_to_datetime(start_time_str)
                end_datetime = str_to_datetime(end_time_str)
                if start_datetime > self.dateTimeStart.dateTime() and \
                        end_datetime < self.dateTimeEnd.dateTime():
                    print(f'{n} / {streamID} / {timestamp}')

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
        self.dateTimeStart = QDateTimeEdit(self.timePeriodGroupBox)
        self.dateTimeStart.setDateTime(QDateTime.currentDateTime().addDays(-1))
        self.dateTimeStart.setDateTimeRange(QDateTime.currentDateTime().addMonths(-2), 
                                       QDateTime.currentDateTime())
        self.dateTimeStart.setCalendarPopup(True)

        self.dateTimeEnd = QDateTimeEdit(self.timePeriodGroupBox)
        self.dateTimeEnd.setDateTime(QDateTime.currentDateTime())
        self.dateTimeEnd.setDateTimeRange(QDateTime.currentDateTime().addMonths(-2), 
                                       QDateTime.currentDateTime()) # TODO: Only pick a date after start date (dynamicly update widget)
        self.dateTimeEnd.setCalendarPopup(True)

        # TODO: ? Add option, either enter start & end timestamp or only start & duration 

        layout = QHBoxLayout()
        layout.addWidget(self.dateTimeStart)
        layout.addWidget(self.dateTimeEnd)

        self.timePeriodGroupBox.setLayout(layout)



if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())