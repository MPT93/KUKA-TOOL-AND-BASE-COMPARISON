from PyQt5.QtWidgets import (
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QLabel,
    QHBoxLayout,
    QMessageBox,
    QFileDialog,
    QPushButton,
)
from PyQt5.QtGui import QIcon
from BaseToolListWidget import BaseToolListWidget
from PyQt5.QtCore import Qt
import zipfile
import os
import glob


class ComparerMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.interface()

    def interface(self):

        MainLayout = QHBoxLayout()
        LeftLayout = QVBoxLayout()
        MiddleLayout = QVBoxLayout()
        RightLayout = QVBoxLayout()

        OptionsLabel = QLabel("Options:")
        OptionsLabel.setAlignment(Qt.AlignTop)
        LeftLayout.addWidget(OptionsLabel)

        LoadFromKukaBackupButton = QPushButton("Load from kuka backup")
        LoadFromKukaBackupButton.clicked.connect(self.load_from_kuka_backup)
        LeftLayout.addWidget(LoadFromKukaBackupButton)

        LoadFromOlpFiles = QPushButton("Load from olp files")
        LoadFromOlpFiles.clicked.connect(self.load_from_olp_files)
        LeftLayout.addWidget(LoadFromOlpFiles)

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
        self.setWindowIcon(QIcon("kuka.png"))
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

    def show_critical_message_box(
        self,
        message_text="Not the right data format!",
        window_title="Error",
        button=QMessageBox.Cancel,
    ):

        Reply = QMessageBox.critical(self, window_title, message_text, button)
        return Reply

    def load_from_kuka_backup(self):

        try:
            zip_file_name, _ = QFileDialog.getOpenFileName(
                self, "Select Kuka .zip backup.", "", "*.zip"
            )

            if zip_file_name:
                with zipfile.ZipFile(zip_file_name, "r") as zip:
                    config_file_path = "KRC/R1/System/$config.dat"
                    with zip.open(config_file_path) as config_file:
                        config_file_content = config_file.readlines()

                    for line in config_file_content:
                        decoded_line = line.decode("UTF-8")
                        self.RobotToolsBasesList.update_data(decoded_line)

            self.RobotToolsBasesList.set_view()
        except (IndexError, ValueError):
            self.show_critical_message_box()
        except KeyError:
            message_text = "File KRC/R1/System/$config.dat does not exist!"
            self.show_critical_message_box(message_text)

    def load_from_olp_files(self):

        try:
            caption = "Select folder with olp files."
            base_path = QFileDialog.getExistingDirectory(caption=caption)

            if base_path:

                self.OfflineToolsBasesList.clear()
                self.OfflineToolsBasesList.create_empty_tools_bases_table()
                self.OfflineToolsBasesList.set_view()

                files_path = os.path.join(base_path, "**/*.olp").replace("\\", "/")
                files_paths = (
                    path.replace("\\", "/")
                    for path in glob.iglob(files_path, recursive=True)
                )

                for file_path in files_paths:
                    with open(file_path, "r") as file:
                        olp_file_content = file.readlines()

                    for line in olp_file_content:
                        self.OfflineToolsBasesList.update_data(line)

                self.OfflineToolsBasesList.set_view()
        except (IndexError, ValueError):
            self.show_critical_message_box()
