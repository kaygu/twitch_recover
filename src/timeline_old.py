# Timeline drawn with basic widget rewriting PaintEvent

from PyQt6.QtWidgets import QApplication, QWidget, QHBoxLayout, QLabel, QVBoxLayout, QScrollArea
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QColor, QFont

import sys
import datetime
from typing import List

from utils.format import str_to_utc_timestamp

class TimelineItem(QWidget):
    '''
    Widget displaying the streams on the timeline
    '''
    def __init__(self, data: dict, realtive_start: int, parent=None):
        super().__init__(parent)
        self.id = data.get('stream_id')
        self.label = data.get('name')
        self.start_date = str_to_utc_timestamp(data.get('timestamp'))
        self.relative_start = realtive_start
        self.duration = int(data.get('length'))
        self.setFixedSize(150, 50)
        self.setToolTip(f"{self.label}\nStart: {self.start_date}\nDuration: {self.duration}")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QColor(100, 200, 250))
        painter.drawRect(self.rect())

        painter.setFont(QFont("Arial", 10))
        painter.setPen(Qt.GlobalColor.black)
        painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, self.label)

class Timeline(QWidget):
    '''
    Widget in charge of drawing the timeline
    '''
    def __init__(self, items: List[TimelineItem], start: int, end: int, parent=None):
        super().__init__(parent)
        self.items = items
        self.start = start
        self.end = end
        self.length = end - start
        self.setMinimumSize(800, 150)

    def paintEvent(self, event):
        painter = QPainter(self)
        
        # Draw Timeline Background
        painter.setBrush(QColor(230, 230, 230))
        painter.drawRect(self.rect())

        # Draw Time Axis (for example, one unit = one day)
        painter.setPen(Qt.GlobalColor.black)
        painter.setFont(QFont("Arial", 10))
        
        # TODO: Add small buffer on each side of timeline 
        # Draw timeline scale
        unit_divider = 3600 # every hour (TODO: change to minutes of scale permits it)
        unit_width = self.frameGeometry().width() / (self.length // unit_divider)
        num_units = self.length // unit_divider 
        print(f'n° units {num_units} of scale {unit_width} px')
        for i in range(num_units):
            x = i * unit_width
            painter.drawLine(x, 0, x, self.frameGeometry().height())
            painter.drawText(x + 2, self.frameGeometry().height() -15, f"{i + 1}")

        # Draw the Items (clips) on the timeline
        for i, item in enumerate(self.items):
            print(f'item {item.id} starts at {item.relative_start} for {item.duration}')
            x_pos = (item.relative_start // unit_divider) * unit_width
            rect = QRect(x_pos, 50 *i, (item.duration // unit_divider) * unit_width, 50)
            painter.setBrush(QColor(100, 150, 250))
            painter.drawRect(rect)

            # Label for each item
            painter.setFont(QFont("Arial", 10))
            painter.setPen(Qt.GlobalColor.white)
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, str(item.id))

class TimelineWindow(QWidget):
    '''
    Window displaying the stream timeline
    '''
    def __init__(self, data: dict):
        super().__init__()

        self.data = data
        self.tl_start = int(self.data.get('start').timestamp())
        self.tl_end = int(self.data.get('end').timestamp())
        self.streams = [TimelineItem(i, str_to_utc_timestamp(i.get('timestamp')) - self.tl_start) 
                        for i in self.data.get('streams')]

        layout = QVBoxLayout()

        # Create scroll area for the timeline (to simulate a long timeline you can scroll)
        scroll_area = QScrollArea()
        timeline_widget = Timeline(self.streams, self.tl_start, self.tl_end)
        scroll_area.setWidget(timeline_widget)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        self.setLayout(layout)
        self.setWindowTitle("Timeline Editor")
        self.resize(900, 300)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    data = {'start': datetime.datetime(2024, 9, 18, 0, 14, 22, 0, tzinfo=datetime.timezone.utc), 'end': datetime.datetime(2024, 9, 21, 0, 14, 22, 0, tzinfo=datetime.timezone.utc), 'streams': [{'name': 'shroud', 'stream_id': 44835701531, 'timestamp': '2024-09-19T18:55:48Z', 'length': 34004.22}, {'name': 'shroud', 'stream_id': 44832696939, 'timestamp': '2024-09-18T17:16:45Z', 'length': 15456.1234}, {'name': 'shroud', 'stream_id': 44827952363, 'timestamp': '2024-09-17T17:14:59Z', 'length': 45123.7890}]}
    window = TimelineWindow(data)
    window.show()
    sys.exit(app.exec())
