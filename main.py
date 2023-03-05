from PyQt5.QtWidgets import QApplication
from ComparerMainWindow import ComparerMainWindow
import sys


if __name__ == "__main__":

    app = QApplication(sys.argv)

    window = ComparerMainWindow()
    window.show()

    app.exec()
