import sys
from PyQt6.QtWidgets import QWidget, QGridLayout, QComboBox, QLabel, QPushButton, QLineEdit, QFileDialog, QApplication
import pathlib
import os
import shutil


class Window(QWidget):

    def __init__(self):
        super().__init__()
        # Set window title

        self.setWindowTitle("Sorter")

        self.layout = QGridLayout()
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(20)

        # Set named widgets
        self.combobox = QComboBox()
        self.combobox.placeholderText()
        self.folder_label = QLabel("Select folder to be sorted")
        self.sort_label = QLabel("")
        self.new_folder_label = QLabel("")
        self.error_label = QLabel("")
        self.folder_select_button = (QPushButton("Select Folder"))
        self.sort_button = QPushButton("Sort")
        self.new_folder_name = QLineEdit("")
        # Set program variables
        self.old_folder = ''
        self.file_list = []
        self.extension = ''
        self.new_folder = ''
        # Add widgets
        self.layout.addWidget(self.folder_select_button, 1, 0)
        self.layout.addWidget(self.new_folder_name, 1, 1)
        self.layout.addWidget(self.combobox, 1, 2)
        self.layout.addWidget(self.sort_button, 1, 3)
        self.layout.addWidget(self.folder_label, 2, 0)
        self.layout.addWidget(self.new_folder_label, 2, 1)
        self.layout.addWidget(self.sort_label, 2, 2)
        self.layout.addWidget(self.error_label, 3, 1)

        self.new_folder_name.returnPressed.connect(self.change_folder_label)

        # Set button click events
        self.folder_select_button.clicked.connect(self.pick_folder)
        self.combobox.currentTextChanged.connect(self.text_changed)
        self.sort_button.clicked.connect(self.sort_files)
        # Set layout
        self.setLayout(self.layout)
        self.SortValidation = None
        self.FolderValidation = None
        self.TextChangedValidation = None
        self.ExtensionValidation = None

    def change_folder_label(self):
        if self.old_folder == '':
            self.error_label.setText("Choose a folder to be sorted")
            return
        else:
            self.new_folder_label.setText(str("{}\\{}".format(self.old_folder, self.new_folder_name.text())))

    # Get folder selection
    def pick_folder(self):
        self.combobox.clear()
        self.file_list.clear()
        try:
            self.old_folder = str(pathlib.PureWindowsPath(QFileDialog().
                                                          getExistingDirectory(None,
                                                                               "Select Folder",
                                                                               "C:\\",
                                                                               QFileDialog.Option.DontUseNativeDialog)))
            if self.old_folder.lower() == 'c:\\' or 'c:\\windows' in self.old_folder.lower():
                self.error_label.setText("Cannot sort system root folders")
                return
            else:
                self.folder_label.setText(self.old_folder)
                self.get_extensions()
        except self.FolderValidation:
            return

    # Get list of extensions in chosen folder
    def get_extensions(self):
        try:
            dir_list = os.listdir(self.old_folder)
            for x in dir_list:
                if os.path.isfile("{}\\{}".format(self.old_folder, x)):
                    a, b = os.path.splitext(x)
                    if b not in self.file_list:
                        self.file_list.append(b)
                else:
                    self.sort_label.setText("No files found in folder")
            for y in self.file_list:
                self.combobox.addItem(y)
            self.new_folder_label.setText("Enter the new folder name")
        except self.ExtensionValidation:
            return

    def text_changed(self, text):
        self.error_label.setText("")
        try:
            self.extension = text
            self.sort_label.setText("Files with {} extension will be sorted".format(text))
        except self.TextChangedValidation:
            return

    # Sort files into folders
    def sort_files(self):
        self.error_label.setText("")
        # Get new folder name
        try:
            self.new_folder = str("{}\\{}".format(self.old_folder, self.new_folder_name.text()))
            # Loop through all filenames in the folder
            for filename in os.listdir(self.old_folder):
                # If the file name ends with the chosen extension
                if filename.endswith(self.extension):
                    # If the new folder doesn't already exist, create it
                    if not os.path.exists(self.new_folder):
                        os.makedirs(self.new_folder)
                        shutil.move("{}\\{}".format(self.old_folder, filename),
                                    "{}\\{}".format(self.new_folder, filename))

                    # Or else, just move the files into the new folder
                    else:
                        shutil.move("{}\\{}".format(self.old_folder, filename),
                                    "{}\\{}".format(self.new_folder, filename))
            self.error_label.setText("Task Completed")
            self.combobox.clear()
            self.file_list.clear()
            self.get_extensions()
        except self.SortValidation:
            self.error_label.setText("Task Failed")
            return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
