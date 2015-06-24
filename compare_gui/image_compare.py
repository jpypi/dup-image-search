#!/usr/bin/python
"""
    image_compare.py

    Takes an input file that contains, line by line, a list of:

        filepath1,filepath2

    Where filepath1 and filepath2 point to valid image files that may be
    considered to be similar.  The user decides whether they are similar
    and responds YES or NO, then the next images are shown, until there are
    none left to evaluate.

    Appends each answer to a results file:

        filepath1,filepath2,[YES|NO]

    Needs pyside:

        sudo -E pip install pyside

    PySide needs a Qt install.  On MacOSX do:

        # homebrew install
        ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

        # install Qt
        brew install qt

    :author: Brandon Arrendondo
    :license: MIT
"""
import sys
import argparse

from PySide.QtGui import QApplication
from PySide.QtGui import QMainWindow
from PySide.QtGui import QBoxLayout
from PySide.QtGui import QWidget
from PySide.QtGui import QPushButton
from PySide.QtGui import QAction
from PySide.QtGui import QMessageBox
from PySide.QtGui import QLabel
from PySide.QtGui import QPixmap
from PySide.QtCore import Qt


class MainUI(QMainWindow):

    def __init__(self, filepath):
        super(MainUI, self).__init__()

        self.title = "Image Verification GUI"
        self.file_handle = open(filepath, "r")
        self.init_ui()

    def init_ui(self):
        # geometry is x offset, y offset, x width, y width
        self.setGeometry(150, 150, 640, 300)
        self.setWindowTitle(self.title)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        exitAction = QAction('E&xit', self)
        exitAction.setStatusTip('Exit the application.')
        exitAction.triggered.connect(self.handle_exit)
        file_menu.addAction(exitAction)

        main_layout_container = QWidget()
        main_layout = QBoxLayout(QBoxLayout.TopToBottom)

        image_layout = QBoxLayout(QBoxLayout.LeftToRight)
        image_layout.addStretch(1)
        self.image1 = QLabel()
        self.image1.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(self.image1)

        image_layout.addWidget(QLabel("vs."))

        self.image2 = QLabel()
        self.image2.setAlignment(Qt.AlignCenter)
        image_layout.addWidget(self.image2)
        image_layout.addStretch(1)

        main_layout.addLayout(image_layout)
        main_layout.addStretch(1)

        button_layout = QBoxLayout(QBoxLayout.LeftToRight)
        button_layout.addStretch(1)
        self.yes_button = QPushButton("Yes")
        button_layout.addWidget(self.yes_button)
        self.yes_button.clicked.connect(self.handle_yes_pressed)

        self.no_button = QPushButton("No")
        button_layout.addWidget(self.no_button)
        self.no_button.clicked.connect(self.handle_no_pressed)
        button_layout.addStretch(1)
        main_layout.addLayout(button_layout)

        main_layout_container.setLayout(main_layout)

        self.image1_filepath = ""
        self.image2_filepath = ""

        self.load_more_images()
        self.setCentralWidget(main_layout_container)

    def handle_exit(self):
        self.close()

    def load_more_images(self):
        line = self.file_handle.readline()
        if(line):
            line_arr = line.strip().split(",")
            assert(len(line_arr) == 2)

            self.image1_filepath = line_arr[0].strip()
            self.image2_filepath = line_arr[1].strip()

            self.image1.setPixmap(QPixmap(self.image1_filepath).scaledToHeight(192))
            self.image2.setPixmap(QPixmap(self.image2_filepath).scaledToHeight(192))

        else:
            ret = QMessageBox.information(self, "Image Verification UI",
                                          "Ran out of images to compare.",
                                          QMessageBox.Ok)
            self.close()

    def handle_yes_pressed(self):
        with open("user_results.txt", "a") as f:
            f.write("{0}, {1}, {2}\n".format(
                self.image1_filepath, self.image2_filepath, "YES"))

        self.load_more_images()

    def handle_no_pressed(self):
        with open("user_results.txt", "a") as f:
            f.write("{0}, {1}, {2}\n".format(
                self.image1_filepath, self.image2_filepath, "NO"))

        self.load_more_images()


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("filepath")
    args = parser.parse_args()

    app = QApplication(sys.argv)
    ex = MainUI(args.filepath)
    ex.show()

    # Qt application main loop
    app.exec_()
    sys.exit()


if __name__ == "__main__":
    main(sys.argv[1:])
