from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QWidget, QLabel, QHBoxLayout, QMessageBox
from PyQt5.QtGui import QIcon
from BaseToolListWidget import BaseToolListWidget
from PyQt5.QtCore import Qt


class ComparerMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.interface()

    def interface(self):

        MainLayout = QHBoxLayout()
        LeftLayout = QVBoxLayout()
        MiddleLayout = QVBoxLayout()
        RightLayout = QVBoxLayout()

        self.RobotToolsBasesList = BaseToolListWidget()
        self.OfflineToolsBasesList = BaseToolListWidget()

        MiddleLayout.addWidget(QLabel("From kuka backup:"))
        MiddleLayout.addWidget(self.RobotToolsBasesList)

        RightLayout.addWidget(QLabel("From olp files:"))
        RightLayout.addWidget(self.OfflineToolsBasesList)

        self.MiddleVerticalScrollBar = self.RobotToolsBasesList.verticalScrollBar()
        self.RightVerticalScrollBar = self.OfflineToolsBasesList.verticalScrollBar()

        self.MiddleVerticalScrollBar.valueChanged.connect(self.move_scrollbar)
        self.RightVerticalScrollBar.valueChanged.connect(self.move_scrollbar)

        MainLayout.addLayout(LeftLayout)
        MainLayout.addLayout(MiddleLayout)
        MainLayout.addLayout(RightLayout)

        MainWidget = QWidget()
        MainWidget.setLayout(MainLayout)
        self.setCentralWidget(MainWidget)

        self.title = "Kuka Base and Tool Comparer"
        self.setWindowTitle(self.title)
        self.setWindowIcon(QIcon('kuka.png'))
        self.resize(900, 700)

    def move_scrollbar(self, value):

        self.MiddleVerticalScrollBar.setValue(value)
        self.RightVerticalScrollBar.setValue(value)

    def close_comparer(self):
        self.close()

    def closeEvent(self, event):

        window_title = "Close"
        message_text = "Do you want to close comparer?"
        buttons = QMessageBox.Yes | QMessageBox.No
        Reply = QMessageBox.question(self, window_title, message_text, buttons)

        if Reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:
            self.close_comparer()
