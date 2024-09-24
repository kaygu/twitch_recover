# Timeline drawn using the QGrapgicsScene components

from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem
from PyQt6.QtGui import QColor, QBrush, QPen, QFont, QPainter
from PyQt6.QtCore import Qt, QRectF

import sys
import datetime
from typing import List

from utils.format import str_to_utc_timestamp

class TimelineItem(QGraphicsRectItem):
    def __init__(self, data: dict, normalized_start: int, row: int, parent=None):
        super().__init__(parent)

        self.unit_divider = 3600

        # data
        self.id = data.get('stream_id')
        self.label = data.get('name')
        self.normalized_start = normalized_start / self.unit_divider
        self.row = row
        self.duration = data.get('length') / self.unit_divider
        self.unit_width = 11.8 # ??
        print(f'start stream at {self.normalized_start} for {self.duration} seconds on row {self.row}')
        # rect dimentsions
        self.height = 50

        # Set the size of the item based on duration
        self.setRect(QRectF(self.normalized_start * self.unit_width, self.row * self.height, self.duration * self.unit_width, self.height))

        # Set the color of the item
        self.setBrush(QBrush(QColor(100, 200, 250)))
        self.setPen(QPen(Qt.GlobalColor.black))

        # Add label as text to the timeline item
        self.text = QGraphicsTextItem(str(self.id), self)
        self.text.setDefaultTextColor(Qt.GlobalColor.black)
        self.text.setFont(QFont("Arial", 10))
        self.text.setPos(self.normalized_start * self.unit_width + 10, self.row * self.height + 15)

class TimelineScene(QGraphicsScene):
    def __init__(self, streams: List[TimelineItem], start: int, end: int, parent=None):
        super().__init__(parent)
        self.streams = streams
        self.start = start
        self.end = end
        self.length = end - start
        self.unit_divider = 3600 # every hour (TODO: change to minutes of scale permits it)
        self.unit_width = 850 / (self.length // self.unit_divider)
        self.num_units = self.length // self.unit_divider 



        # Draw the timeline axis and the items
        self.drawTimelineAxis()
        self.addTimelineItems()

    def drawTimelineAxis(self):
        '''
        Draw horizontal lines to represent the timeline axis
        '''
        print(f'n° units {self.num_units} of scale {self.unit_width} px')
        for i in range(self.num_units):
            x_pos = i * self.unit_width
            # Draw vertical grid line
            line = QGraphicsLineItem(x_pos, 0, x_pos, 500)
            line.setPen(QPen(Qt.GlobalColor.black))
            self.addItem(line)

            # Add day label below each line
            time_label = QGraphicsTextItem(f"{i+1}")
            time_label.setFont(QFont("Arial", 10))
            time_label.setDefaultTextColor(Qt.GlobalColor.black)
            time_label.setPos(x_pos + 2, 80)
            self.addItem(time_label)

    def addTimelineItems(self):
        # Add each item to the scene
        for stream in self.streams:
            self.addItem(stream)

class TimelineWindow(QMainWindow):
    def __init__(self, data:dict, verbose: bool = False):
        super().__init__()

        self.verbose = verbose

        # Handle data
        self.data = data
        self.tl_start = int(self.data.get('start').timestamp())
        self.tl_end = int(self.data.get('end').timestamp())
        self.streams = [TimelineItem(strm, str_to_utc_timestamp(strm.get('timestamp')) - self.tl_start, i) 
                        for i, strm in enumerate(self.data.get('streams'))]
        
        ##
        self.w_width = self.frameGeometry().width()
        if self.verbose:
            print(f'window width {self.w_width}')

        # Create the scene
        self.scene = TimelineScene(self.streams, self.tl_start, self.tl_end, self)

        # Create the view
        self.view = QGraphicsView(self.scene, self)
        self.view.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.view.setSceneRect(0, 0, 850, 200)
        

        # Set the view as the central widget
        self.setCentralWidget(self.view)

        self.setWindowTitle("Timeline Editor with QGraphicsScene")
        # self.setMinimumSize(900, 300)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    data = {
        'start': datetime.datetime(2024, 9, 18, 0, 14, 22, 0, tzinfo=datetime.timezone.utc),
        'end': datetime.datetime(2024, 9, 21, 0, 14, 22, 0, tzinfo=datetime.timezone.utc),
        'streams': [
            {'name': 'shroud', 'stream_id': 44835701531, 'timestamp': '2024-09-19T18:55:48Z', 'length': 34004.22},
            {'name': 'shroud', 'stream_id': 44832696939, 'timestamp': '2024-09-18T17:16:45Z', 'length': 15456.1234},
            {'name': 'shroud', 'stream_id': 44827952363, 'timestamp': '2024-09-17T17:14:59Z', 'length': 45123.7890}
        ]
    }    
    window = TimelineWindow(data)
    window.show()
    sys.exit(app.exec())
