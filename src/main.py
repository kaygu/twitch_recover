from PyQt6.QtCore import QDateTime, Qt, QTimer, QTimeZone
from PyQt6.QtWidgets import (QApplication, QMainWindow, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)

import datetime

from timelines import TimelinesWindow
from connectors.sullygnome import SullygnomeConnector
from connectors.twitch import TwitchConnector
from utils.format import str_to_datetime, convert_to_utc_timestamp, qdatetime_to_utc_datetime
from utils.m3u8 import M3U8


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        # self.originalPalette = QApplication.palette()  

        self.createUsernamesGroupBox()
        self.createTimePeriodGroupBox()
        self.createButtonGroupBox()

    
        mainLayout = QGridLayout()
        mainLayout.addWidget(self.usernamesGroupBox, 0, 0)
        mainLayout.addWidget(self.timePeriodGroupBox, 1, 0)
        mainLayout.addWidget(self.buttonGroupBox, 2, 0)

        container = QWidget()
        container.setLayout(mainLayout)
        self.setCentralWidget(container)

        self.setWindowTitle("Twitch Bulk Download")
        self.setMinimumSize(320, 250)

    def onUsernameButtonPressed(self, usernames:str):
        # Do research for the twitch usernames
        connector = SullygnomeConnector() # TODO: Develop other connectors in case the current service fails
        twitchConnector = TwitchConnector() # Used to find the m3u8 files
        # self.usernamesGroupBox.setDisabled(True)
        user_start_dt = qdatetime_to_utc_datetime(self.dateTimeStart)
        user_end_dt = qdatetime_to_utc_datetime(self.dateTimeEnd)
        data = {'start': user_start_dt, 'end': user_end_dt, 'streams':[]}
        for n in usernames.split(';'):
            for vod in connector.get_past_vods(n, verbose=False):
                streamID, timestamp_str, start_time_str, end_time_str = vod
                start_datetime = str_to_datetime(start_time_str)
                end_datetime = str_to_datetime(end_time_str)

                if (start_datetime < user_end_dt and \
                        end_datetime > user_start_dt):
                    print(f'{n} / {streamID} / {timestamp_str}')
                    timestamp = convert_to_utc_timestamp(timestamp_str)
                    m3u8_url = twitchConnector.get_vod(n, streamID, timestamp)
                    data['streams'].append({'name': n, 'stream_id': streamID, 'timestamp': timestamp_str, 'm3u8': m3u8_url})
        
        self.w = TimelinesWindow(verbose=True)
        self.w.setStreamData(data)
        self.w.show()

    def createUsernamesGroupBox(self):
        self.usernamesGroupBox = QGroupBox('Twitch Usernames', self)

        self.usernames = QLineEdit('shroud') # Keep history from latest query
        self.usernames.setEchoMode(QLineEdit.EchoMode.Normal)

        layout = QHBoxLayout()
        layout.addWidget(self.usernames)

        self.usernamesGroupBox.setLayout(layout)

    def createButtonGroupBox(self):
        self.buttonGroupBox = QGroupBox('Submit', self)
        button = QPushButton("Search VODs")
        button.clicked.connect(lambda: self.onUsernameButtonPressed(self.usernames.text()))

        layout = QHBoxLayout()
        layout.addWidget(button)
        self.buttonGroupBox.setLayout(layout)


    def onStartDateTimeChanged(self, dateTime):
        '''
        Changes range of end datetime based on starting datetime
        '''
        self.dateTimeEnd.setDateTimeRange(dateTime, QDateTime.currentDateTime())


    def createTimePeriodGroupBox(self):
        self.timePeriodGroupBox = QGroupBox('Timestamps', self)

        # Add label for start & end timestamps
        self.dateTimeStart = QDateTimeEdit(self.timePeriodGroupBox)
        self.dateTimeStart.setDateTime(QDateTime.currentDateTime().addDays(-1))
        self.dateTimeStart.setTimeZone(QTimeZone.utc())
        self.dateTimeStart.setDateTimeRange(QDateTime.currentDateTime().addMonths(-2), 
                                       QDateTime.currentDateTime())
        self.dateTimeStart.setCalendarPopup(True)
        self.dateTimeStart.dateTimeChanged.connect(self.onStartDateTimeChanged)

        self.dateTimeEnd = QDateTimeEdit(self.timePeriodGroupBox)
        self.dateTimeEnd.setDateTime(QDateTime.currentDateTime())
        self.dateTimeEnd.setTimeZone(QTimeZone.utc())
        self.dateTimeEnd.setDateTimeRange(QDateTime.currentDateTime().addMonths(-2), 
                                       QDateTime.currentDateTime()) # TODO: Only pick a date after start date (dynamicly update widget)
        self.dateTimeEnd.setCalendarPopup(True)

        # TODO: ? Add option, either enter start & end timestamp or only start & duration 

        layout = QGridLayout()
        layout.addWidget(QLabel('Start Time'), 0, 0)
        layout.addWidget(self.dateTimeStart, 1, 0)
        layout.addWidget(QLabel('End Time'), 0, 1)
        layout.addWidget(self.dateTimeEnd, 1, 1)

        self.timePeriodGroupBox.setLayout(layout)



if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())