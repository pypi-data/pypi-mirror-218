"""
QVSED - Qt-Based Volatile Small Editor
A cross-platform simple and volatile text editor by Arsalan Kazmi
See README.md or "Get Help" inside QVSED for more info
"""

import os
import shutil
import configparser
import importlib.util
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget,
    QFileDialog, QPlainTextEdit, QLineEdit, QAction, QShortcut
)
from PyQt5.QtGui import QKeySequence, QFont
from PyQt5.uic import loadUi


class QVSEDApp:
    def __init__(self):
        self.app = QApplication([])
        self.window = QVSEDWindow()

    def run(self):
        self.window.show()
        self.app.exec()


class QVSEDWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_ui_file()
        self.set_up_actions()
        self.set_up_shortcuts()
        self.set_up_event_handlers()
        self.load_config()
        self.set_up_fonts()

    def echo_area_update(self, message):
        echo_area = self.findChild(QLineEdit, "echoArea")
        echo_area.setText(message)

    def load_ui_file(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        ui_file = os.path.join(current_dir, 'qvsed.ui')
        loadUi(ui_file, self)

    def generate_config(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        config_default = os.path.join(current_dir, 'config_default.py')
        
        if os.name == 'nt': # Windows
            user_config_dir = os.path.join(os.environ['APPDATA'], 'QVSED')
        else: # *nix
            user_config_dir = os.path.expanduser("~") + "/.config/QVSED"
        
        if not os.path.exists(user_config_dir):
            os.makedirs(user_config_dir)
        user_config_file = os.path.join(user_config_dir, 'config.py')
        
        shutil.copyfile(config_default, user_config_file)

        # Update the first line of config.py
        with open(user_config_file, "r+") as config_file:
            lines = config_file.readlines()
            if lines:
                lines[0] = "# This is QVSED's config file, you can change its options here.\n"
                config_file.seek(0)
                config_file.writelines(lines)
                config_file.truncate()
                
        self.echo_area_update(f"Config generated at {user_config_file}.")

    def load_config(self):
        if os.name == 'nt': # Windows
            user_config_dir = os.path.join(os.environ['APPDATA'], 'QVSED')
        else: # *nix
            user_config_dir = os.path.expanduser("~") + "/.config/QVSED"
        
        user_config_file = os.path.join(user_config_dir, 'config.py')

        if not os.path.isfile(user_config_file):
            self.generate_config()
        
        spec = importlib.util.spec_from_file_location("qvsed_config", user_config_file)
        qvsed_config = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(qvsed_config)

        self.font_family = qvsed_config.font_family
        self.font_size = qvsed_config.font_size

    def set_up_fonts(self):
        font = QFont()
        font.setFamilies(self.font_family)
        font.setPointSize(self.font_size)
        QApplication.instance().setFont(font)
        self.update_widget_fonts(self)

    def set_up_actions(self):
        self.clear_action = QAction("Clear Text", self)
        self.save_action = QAction("Save File", self)
        self.open_action = QAction("Open File", self)
        self.help_action = QAction("Get Help", self)
        self.quit_action = QAction("Quit QVSED", self)

    def set_up_shortcuts(self):
        self.clear_shortcut = QShortcut(QKeySequence("Ctrl+N"), self)
        self.save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        self.open_shortcut = QShortcut(QKeySequence("Ctrl+F"), self)
        self.help_shortcut = QShortcut(QKeySequence("Ctrl+H"), self)
        self.quit_shortcut = QShortcut(QKeySequence("Alt+Q"), self)
        self.fullscreen_shortcut = QShortcut(QKeySequence("Alt+F"), self)

    def set_up_event_handlers(self):
        self.clear_shortcut.activated.connect(self.clear_text_area)
        self.save_shortcut.activated.connect(self.save_text_contents)
        self.open_shortcut.activated.connect(self.load_from_file)
        self.help_shortcut.activated.connect(self.show_help)
        self.quit_shortcut.activated.connect(self.quit_app)
        self.fullscreen_shortcut.activated.connect(self.toggle_fullscreen)

        self.findChild(QPushButton, "clearButton").clicked.connect(self.clear_text_area)
        self.findChild(QPushButton, "saveButton").clicked.connect(self.save_text_contents)
        self.findChild(QPushButton, "openButton").clicked.connect(self.load_from_file)
        self.findChild(QPushButton, "helpButton").clicked.connect(self.show_help)
        self.findChild(QPushButton, "quitButton").clicked.connect(self.quit_app)
        self.findChild(QPushButton, "fullscreenButton").clicked.connect(self.toggle_fullscreen)

    def clear_text_area(self):
        text_area = self.findChild(QPlainTextEdit, "textArea")

        if text_area.toPlainText() == "":
            self.echo_area_update("Text Area is already blank.")
            return

        text_area.clear()

        self.echo_area_update("Text Area has been cleared.")

    def save_text_contents(self):
        text_area = self.findChild(QPlainTextEdit, "textArea")

        if text_area.toPlainText() == "":
            self.echo_area_update("Text Area is blank, will not save.")
            return

        file_path, _ = QFileDialog.getSaveFileName(self, "Save File")

        if file_path:
            try:
                with open(file_path, 'w') as file:
                    file.write(text_area.toPlainText())
                file_name = os.path.basename(file_path)
                self.echo_area_update(f"Saved file {file_name}.")
            except Exception as e:
                self.echo_area_update(f"Error saving file: {str(e)}")

    def load_from_file(self):
        text_area = self.findChild(QPlainTextEdit, "textArea")

        file_path, _ = QFileDialog.getOpenFileName(self, "Open File")

        if file_path:
            try:
                with open(file_path, 'r') as file:
                    text_area.setPlainText(file.read())
                file_name = os.path.basename(file_path)
                self.echo_area_update(f"Opened file {file_name}.")
            except Exception as e:
                self.echo_area_update(f"Error opening file: {str(e)}")

    def show_help(self):
        text_area = self.findChild(QPlainTextEdit, "textArea")

        help_message = """QVSED - Qt-based Volatile Small Editor
========================================
QVSED is a stateless, volatile text editor with a minimalist approach, focusing solely on text editing without file metadata or prompts for potentially destructive actions.

This is the Text Area, where the actual editing takes place. Type anything you want into here, and edit as you please.
Down there, below the Text Area is the Echo Area, where messages and errors will be displayed.
On the left of the QVSED window is the Action Deck, containing commands to clear the Text area, open or save a file, display this help text, toggle in and out of full screen mode or quit QVSED.

I hope you enjoy using QVSED! I enjoyed writing it, and it's a nice little venture into my first Qt project.

- Arsalan Kazmi <sonicspeed848@gmail.com>, That1M8Head on GitHub"""

        self.echo_area_update("Help message shown in Text Area.")

        text_area.setPlainText(help_message)

    def quit_app(self):
        QApplication.quit()

    def toggle_fullscreen(self):
        if self.isFullScreen():
            self.showNormal()
        else:
            self.showFullScreen()

    def update_widget_fonts(self, widget):
        if widget is None:
            return

        widget.setFont(QApplication.instance().font())

        for child_widget in widget.findChildren(QWidget):
            self.update_widget_fonts(child_widget)

def main():
    app = QVSEDApp()
    app.run()

if __name__ == "__main__":
    main()
