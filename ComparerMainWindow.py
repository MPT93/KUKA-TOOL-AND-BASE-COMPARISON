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
from BaseToolListWidget import BaseToolListWidget, Base, Tool
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

        self.CompareButton = QPushButton("Compare")
        self.CompareButton.clicked.connect(self.compare)
        self.CompareButton.setCheckable(True)
        LeftLayout.addWidget(self.CompareButton)

        SaveExistingOlpData = QPushButton("Save existing olp data")
        SaveExistingOlpData.clicked.connect(self.save_existing_olp_bases_and_tools)
        LeftLayout.addWidget(SaveExistingOlpData)

        CreateReport = QPushButton("Create report")
        CreateReport.clicked.connect(self.create_report)
        LeftLayout.addWidget(CreateReport)

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
            self.reset_comparing()

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
            self.reset_comparing()

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

    def compare(self):

        if self.CompareButton.isChecked():
            for index in range(self.RobotToolsBasesList.count()):
                if (
                    self.RobotToolsBasesList.item(index).text()
                    != self.OfflineToolsBasesList.item(index).text()
                ):
                    self.RobotToolsBasesList.item(index).setBackground(Qt.red)
                    self.OfflineToolsBasesList.item(index).setBackground(Qt.red)
        else:
            for index in range(self.RobotToolsBasesList.count()):
                if (
                    self.RobotToolsBasesList.item(index).text()
                    != self.OfflineToolsBasesList.item(index).text()
                ):
                    self.RobotToolsBasesList.item(index).setBackground(Qt.white)
                    self.OfflineToolsBasesList.item(index).setBackground(Qt.white)

    def reset_comparing(self):
        self.CompareButton.setChecked(False)
        self.compare()

    def save_existing_olp_bases_and_tools(self):

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save offline data under...", "", "*.txt"
        )

        if file_path:
            if self.OfflineToolsBasesList.check_if_not_default_frame_exists():
                with open(file_path, "w") as file:

                    for base in self.OfflineToolsBasesList.bases_table:
                        if not base.check_if_default():
                            ComparerMainWindow.write_krl_frame_data_into_file(
                                file,
                                base.get_base_name_in_krl_syntax(),
                                base.get_base_data_in_krl_syntax(),
                                base.get_base_typ_in_krl_syntax(),
                            )

                    for tool in self.OfflineToolsBasesList.tools_table:
                        if not tool.check_if_default():
                            ComparerMainWindow.write_krl_frame_data_into_file(
                                file,
                                tool.get_tool_name_in_krl_syntax(),
                                tool.get_tool_data_in_krl_syntax(),
                                tool.get_tool_typ_in_krl_syntax(),
                            )

    def create_report(self):

        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save report under...", "", "*.txt"
        )

        if file_path:
            if (
                self.OfflineToolsBasesList.check_if_not_default_frame_exists()
                or self.RobotToolsBasesList.check_if_not_default_frame_exists()
            ):
                with open(file_path, "w") as file:
                    file.write(
                        "Differences between robot bases and olp bases (robot base - olp base):\n"
                    )
                    for robot_base, olp_base in zip(
                        self.RobotToolsBasesList.bases_table,
                        self.OfflineToolsBasesList.bases_table,
                    ):
                        if (
                            not robot_base.check_if_default()
                            or not olp_base.check_if_default()
                        ):
                            frames_equal, delta = Base.compare_coordinates(
                                robot_base, olp_base
                            )
                            if not frames_equal:
                                file.write(f"Base[{robot_base.number}] differences in:\n")
                                file.write(f"X={delta[0]}, Y={delta[1]}, Z={delta[2]}, A={delta[3]}, B={delta[4]}, C={delta[5]}\n")

                    file.write(
                        "\nDifferences between robot tools and olp tools (robot tool - olp tool):\n"
                    )

                    for robot_tool, olp_tool in zip(
                        self.RobotToolsBasesList.tools_table,
                        self.OfflineToolsBasesList.tools_table,
                    ):
                        if (
                            not robot_tool.check_if_default()
                            or not olp_tool.check_if_default()
                        ):
                            frames_equal, delta = Tool.compare_coordinates(
                                robot_tool, olp_tool
                            )
                            if not frames_equal:
                                file.write(f"Tool[{robot_tool.number}] differences in:\n")
                                file.write(f"X={delta[0]}, Y={delta[1]}, Z={delta[2]}, A={delta[3]}, B={delta[4]}, C={delta[5]}\n")

    @staticmethod
    def write_krl_frame_data_into_file(file, frame_name, frame_data, frame_typ):
        file.write("{}\n".format(frame_name))
        file.write("{}\n".format(frame_data))
        file.write("{}\n".format(frame_typ))
