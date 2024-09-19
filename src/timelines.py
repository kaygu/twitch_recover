from PyQt6.QtCore import Qt, QDateTime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)

from utils.m3u8 import M3U8

class TimelinesWindow(QWidget):
    '''
    Window that appears when vizualizing timelines
    '''
    def __init__(self, verbose: bool = False):
        super().__init__()
        self.verbose = verbose
        if self.verbose:
            print("Displaying new window with stream timelines")
        mainLayout = QVBoxLayout()
        self.label = QLabel("Another Window")
        self.submit_button = QPushButton('Download')
        

        self.setupDisplayStreams()
        mainLayout.addWidget(self.label)
        mainLayout.addWidget(self.streamsGroupBox)
        mainLayout.addWidget(self.submit_button, alignment=Qt.AlignmentFlag.AlignRight)
        self.setLayout(mainLayout)

        self.setMinimumSize(320, 250)

    def setStreamData(self, data: dict):
        # Do some data checks here?
        if self.verbose:
            print(data)
        self.data = data
        self.streams = data.get('streams')
        
        for stream in self.streams:
            m3u8 = M3U8(stream.get('m3u8'), self.verbose)
            m3u8.get_length()
            m3u8.count_muted_segements()
            m3u8.count_muted_seconds()
            m3u8.download(start=data.get('start'), end=data.get('end'))
        self.updateDisplayStreams()
        self.updateLabel()
    
    def setupDisplayStreams(self):
        self.streamsGroupBox = QGroupBox('Stream Timelines')
        layout = QGridLayout()
        self.streamsGroupBox.setLayout(layout)

    def updateDisplayStreams(self):
        '''
        Once new dta is fetched, update visuals
        '''
        layout = self.streamsGroupBox.layout()
        for i, stream in enumerate(self.streams):
            layout.addWidget(QCheckBox(), i, 0) # Save state of the check box
            layout.addWidget(QLabel(stream.get('name')), i, 1)
            layout.addWidget(QLabel(stream.get('timestamp')), i, 2)
        self.streamsGroupBox.setLayout(layout)

    def updateLabel(self):
        self.label.setText(f"{self.data.get('start')} -> {self.data.get('end')}")
