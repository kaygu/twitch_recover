# Timeline drawn using the QGrapgicsScene components

from PyQt6.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsView, QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem
from PyQt6.QtGui import QColor, QBrush, QPen, QFont, QPainter
from PyQt6.QtCore import Qt, QRectF

import sys
import datetime
from typing import List

from utils.format import str_to_utc_timestamp

MAGIC_UNIT_DIVIDER = 3600 # 1 unit is one hour (TODO: adapt scale to length of time frame and zoom level)
MAGIC_UNIT_WIDTH = 15 # px
MAGIC_MARGIN_UNITS = 4 # number of units of margin around the timeline
MAGIC_STREAM_RECT_HEIGHT = 50 # px

# TODO : Lots of things
#   - Display items out of timeframe in b&w


class TimelineItem(QGraphicsRectItem):
    '''
    QGraphicsRectItem subclass to represent a single stream on the timeline
    '''
    def __init__(self, data: dict, normalized_start: float, row: int, verbose: bool=False, parent=None):
        super().__init__(parent)
        self.verbose = verbose

        self.unit_divider = MAGIC_UNIT_DIVIDER

        # data
        self.id = data.get('stream_id')
        self.label = data.get('name')
        self.normalized_start = normalized_start / self.unit_divider
        self.row = row
        self.duration = data.get('length') / self.unit_divider
        self.unit_width = MAGIC_UNIT_WIDTH
        
        # rect dimentsions
        self.height = MAGIC_STREAM_RECT_HEIGHT

        # Set the size of the item based on duration
        self.setRect(QRectF((self.normalized_start + MAGIC_MARGIN_UNITS) * self.unit_width, self.row * self.height + MAGIC_MARGIN_UNITS*self.unit_width, self.duration * self.unit_width, self.height))

        # Set the color of the item
        self.setBrush(QBrush(QColor(100, 200, 250)))
        self.setPen(QPen(Qt.GlobalColor.black))

        # Add label as text to the timeline item
        self.text = QGraphicsTextItem(str(self.id), self)
        self.text.setDefaultTextColor(Qt.GlobalColor.black)
        self.text.setFont(QFont("Arial", 10))
        self.text.setPos((self.normalized_start + MAGIC_MARGIN_UNITS) * self.unit_width + 10, self.row * self.height + 15 + MAGIC_MARGIN_UNITS*self.unit_width)

        if self.verbose:
            print(f'stream {self.id} at {self.normalized_start:.3f} for {self.duration:.3f} units ({MAGIC_UNIT_DIVIDER} seconds) on row {self.row}')


class TimelineScene(QGraphicsScene):
    '''
    QGraphicsScene subclass to hold the timeline items (streams and timeline axis)
    '''
    def __init__(self, streams: List[TimelineItem], start: datetime.datetime, end: datetime.datetime, verbose: bool=False, parent=None):
        super().__init__(parent)
        self.verbose = verbose

        self.streams = streams
        self.start_ts = start.timestamp()
        self.start_dt = start
        self.end_ts = end.timestamp()
        self.end_dt = end
        self.length = self.end_ts - self.start_ts
        self.unit_divider = MAGIC_UNIT_DIVIDER 
        self.unit_width = MAGIC_UNIT_WIDTH # 850 / (self.length // self.unit_divider)
        self.num_units = int(self.length) // self.unit_divider

        if self.verbose:
            print('\nSCENE:')
            print(f'length {self.length} seconds, {self.num_units} units of {self.unit_divider} seconds')
            print(f'n° units {self.num_units} of scale {self.unit_width} px')

        # Draw the timeline axis and the items
        self.drawTimelineAxis()
        self.addTimelineItems()

    def drawTimelineAxis(self):
        '''
        Draw horizontal lines to represent the timeline axis
        '''
            
        for i in range(self.num_units + MAGIC_MARGIN_UNITS):
            x_pos = (i + MAGIC_MARGIN_UNITS) * self.unit_width
            # Draw vertical grid line
            line = QGraphicsLineItem(x_pos, 0, x_pos, 500)
            line.setPen(QPen(Qt.GlobalColor.black))
            self.addItem(line)

            # Add day label below each line
            time_label = QGraphicsTextItem(f"{i+1}")
            time_label.setFont(QFont("Arial", 10))
            time_label.setDefaultTextColor(Qt.GlobalColor.black)
            time_label.setPos(x_pos + 2, (MAGIC_MARGIN_UNITS * self.unit_width) / 2)
            self.addItem(time_label)

    def addTimelineItems(self):
        # Add each item to the scene
        for stream in self.streams:
            self.addItem(stream)

class TimelineView(QGraphicsView):
    '''
    QGraphicsView subclass to display the timeline
    '''
    def __init__(self, scene: QGraphicsScene, verbose: bool=False, parent=None):
        super().__init__(parent)
        self.verbose = verbose

        self.setScene(scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setSceneRect(0, 0, 850, 200) # Magic numbers for now
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
    
class TimelineWindow(QMainWindow):
    '''
    Main window for the stream timeline
    '''
    def __init__(self, data:dict, verbose: bool = False):
        super().__init__()

        self.verbose = verbose

        # Handle data
        self.data = data
        self.tl_start = self.data.get('start')
        self.tl_end = self.data.get('end')
        self.streams = [TimelineItem(strm, str_to_utc_timestamp(strm.get('timestamp')) - self.tl_start.timestamp(), i, self.verbose) 
                        for i, strm in enumerate(self.data.get('streams'))]
        
        ##
        self.w_width = self.frameGeometry().width()
           

        # Create the scene
        self.scene = TimelineScene(self.streams, self.tl_start, self.tl_end, self.verbose, self)

        # Create the view
        self.view = TimelineView(self.scene, self.verbose, self)
        self.view.setSceneRect(0, 0, ((self.tl_end.timestamp() - self.tl_start.timestamp()) / MAGIC_UNIT_DIVIDER) * MAGIC_UNIT_WIDTH + MAGIC_UNIT_WIDTH*MAGIC_MARGIN_UNITS*2,\
                                len(self.streams) * MAGIC_STREAM_RECT_HEIGHT+MAGIC_UNIT_WIDTH*MAGIC_MARGIN_UNITS*2)

        
        # Set the view as the central widget
        self.setCentralWidget(self.view)

        self.setWindowTitle("Timeline Editor with QGraphicsScene")

        if self.verbose:
            print('\nWINDOW:')
            print(f'scene rect {self.view.sceneRect()}')
            # print(f'window width {self.w_width}') # inacurate

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
    window = TimelineWindow(data, verbose=True)
    window.show()
    sys.exit(app.exec())
